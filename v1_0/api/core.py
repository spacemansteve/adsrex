from ..user_roles import anonymous_user, authenticated_user, bumblebee_user
import time

def test_resources():
    
    # /v1/resources doesn't exist (but I think it should exist)
    r = anonymous_user.get('/resources')
    assert r.status_code == 404
    
    # the response is organized from the perspective of the ADS developer/ API maintainer
    # but API users probably expect to see something like:
    # {
    # '/v1': {
    #    'endpoints': [
    #       '/search/query'
    #        ...
    #     ]
    #  },
    # '/v2': {
    #    'endpoints': [
    #       '/search/newquery',
    #       ...
    #     ]
    #  }
    # }
    #
    # If we run two versions of the API alongside, I don't see 
    # how the current structure can communicate two different 
    # 'bases'
    
    # hack to get to the resources
    url = '/'.join(anonymous_user.get_config('API_URL').split('/')[0:-1])
    r = anonymous_user.get( url + '/resources')
    resources = r.json()
    
    # check for presence of services in ['adsws.api']['endpoints']
    for endpoint in [
            "/citation_helper/resources", # is this necessary?
            "/recommender/resources",
            "/graphics/resources",
            "/biblib/resources",
            "/biblib/libraries",
            "/search/resources",
            "/export/resources",
            "/search/bigquery",
            "/export/endnote",
            "/search/status",
            "/export/aastex",
            "/export/bibtex",
            "/search/query",
            "/search/qtree",
            "/search/tvrh",
            "/orcid/exchangeOAuthCode",
            "/vault/configuration",
            "/oauth/authorize",
            "/vault/user-data",
            "/orcid/resources",
            "/oauth/invalid/",
            "/oauth/errors/",
            "/oauth/token",
            "/vault/query",
            "/oauth/ping/", # why is it duplicated in the response?
            "/oauth/ping/",
            "/oauth/info/",
            "/vis/author-network",
            "/vis/paper-network",
            "/vis/word-cloud",
            "/vis/resources",
            "/citation_helper/",
            "/protected",
            "/metrics/",
            "/status",
            "/biblib/permissions/<string:library>",
            "/biblib/libraries/<string:library>",
            "/biblib/documents/<string:library>",
            "/biblib/transfer/<string:library>",
            "/vault/execute_query/<queryid>",
            "/vault/configuration/<key>",
            "/vault/query2svg/<queryid>",
            "/vault/query/<queryid>",
            "/orcid/<orcid_id>/orcid-profile",
            "/orcid/<orcid_id>/orcid-works",
            "/recommender/<string:bibcode>",
            "/graphics/<string:bibcode>",
            "/metrics/<string:bibcode>",
            "/user/<string:identifier>"
        ]:
        assert endpoint in resources['adsws.api']['endpoints']
        
    
    #... and in adsws.accounts
    for endpoint in [
            "/oauth/authorize",
            "/oauth/invalid/",
            "/oauth/errors/",
            "/oauth/token",
            "/oauth/ping/",
            "/oauth/ping/",
            "/oauth/info/",
            "/user/delete",
            "/change-password",
            "/change-email",
            "/bootstrap",
            "/protected",
            "/register",
            "/status",
            "/logout",
            "/token",
            "/csrf",
            "/user",
            "/reset-password/<string:token>",
            "/verify/<string:token>"
        ]:
        assert endpoint in resources['adsws.accounts']['endpoints']
        

    # ... and in adsws.feedback
    for endpoint in [
            "/oauth/authorize",
            "/oauth/invalid/",
            "/oauth/errors/",
            "/oauth/token",
            "/oauth/ping/",
            "/oauth/ping/",
            "/oauth/info/",
            "/slack"
        ]:
        assert endpoint in resources['adsws.feedback']['endpoints']

def test_limits():
    # Check the response contains Headers
    # and the limits are there
    r = authenticated_user.get('/search/query', params={'q': 'title:"%s"' % time.time()})
    print r.headers
    assert r.headers['x-ratelimit-limit'] == '5000'
    
    old_limit = int(r.headers['x-ratelimit-remaining'])
    r = authenticated_user.get('/search/query', params={'q': 'title:"%s"' % time.time()})
    assert r.headers['x-ratelimit-remaining'] == str(old_limit-1)
    assert 'x-ratelimit-reset' in r.headers
    
    
def test_bootstrap():
    r = authenticated_user.get('/accounts/bootstrap')
    a = r.json()
    
    r = anonymous_user.get('/accounts/bootstrap')
    b = r.json()
    
    # currently fails, it returns 'anonymous' for the
    # authenticated user
    assert a['username'] != b['username']
    assert a['access_token'] != b['access_token']
    
    # repeating the bootstrap request should give you the
    # same access token
    for x in xrange(5):
        r = anonymous_user.get('/accounts/bootstrap')
        assert r.json()['access_token'] == b['access_token']
        
    for x in xrange(5):
        r = authenticated_user.get('/accounts/bootstrap')
        assert r.json()['access_token'] == a['access_token']
        
        
def test_crossx_headers():
    # XXX: this should be improved (but in general, the microservices
    # should test for headers that they require (e.g. Orcid-Authorization
    # is tested in orcid)
    for endpoint in [
                     '/accounts/bootstrap'
                     ]:
        r = bumblebee_user.options(endpoint)
        
        # the value of this header will differ between staging and production
        assert 'access-control-allow-origin' in r.headers
        assert 'ui.adsabs.harvard.edu' in r.headers['access-control-allow-origin']
        assert 'access-control-allow-headers' in r.headers
        assert r.headers['access-control-allow-headers']
    
            
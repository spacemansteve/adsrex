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
            "/harbour/auth/twopointoh", 
            "/harbour/auth/classic", 
            "/harbour/mirrors", 
            "/harbour/version", 
            "/objects/query", 
            "/harbour/user", 
            "/biblib/twopointoh", 
            "/search/resources", 
            "/biblib/resources", 
            "/biblib/libraries", 
            "/search/bigquery", 
            "/biblib/classic", 
            "/export/endnote", 
            "/search/status", 
            "/export/bibtex", 
            "/export/aastex", 
            "/export/icarus", 
            "/search/query", 
            "/search/qtree", 
            "/export/mnras", 
            "/search/tvrh", 
            "/export/soph", 
            "/export/ris", 
            "/orcid/exchangeOAuthCode", 
            "/vault/configuration", 
            "/oauth/authorize", 
            "/vault/user-data", 
            "/oauth/invalid/", 
            "/oauth/errors/", 
            "/oauth/token", 
            "/vault/query", 
            "/oauth/ping/", 
            "/oauth/ping/", 
            "/oauth/info/", 
            "/vis/author-network", 
            "/vis/paper-network", 
            "/vis/word-cloud", 
            "/citation_helper/", 
            "/protected", 
            "/metrics/", 
            "/objects/", 
            "/status", 
            "/harbour/libraries/twopointoh/<int:uid>", 
            "/harbour/libraries/classic/<int:uid>", 
            "/harbour/export/twopointoh/<export>", 
            "/objects/pos/<string:pstring>", 
            "/objects/<string:objects>/<string:source>", 
            "/biblib/permissions/<string:library>", 
            "/biblib/documents/<string:library>", 
            "/biblib/libraries/<string:library>", 
            "/biblib/transfer/<string:library>", 
            "/vault/execute_query/<queryid>", 
            "/vault/configuration/<key>", 
            "/orcid/preferences/<orcid_id>", 
            "/orcid/get-profile/<orcid_id>", 
            "/vault/query2svg/<queryid>", 
            "/orcid/export/<iso_datestring>", 
            "/vault/query/<queryid>", 
            "/orcid/<orcid_id>/orcid-profile", 
            "/orcid/<orcid_id>/orcid-works", 
            "/recommender/<string:bibcode>", 
            "/graphics/<string:bibcode>", 
            "/metrics/<string:bibcode>", 
            "/objects/<string:objects>", 
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
    #assert a['username'] != b['username']

    # users should have different tokens
    assert a['access_token'] != b['access_token']
    
    # repeating the bootstrap request should give you the same access token
    # but we are getting different ones for both anonymous and authenticated
    for x in xrange(5):
        r = anonymous_user.get('/accounts/bootstrap')
        # assert r.json()['access_token'] == b['access_token']
        
    for x in xrange(5):
        r = authenticated_user.get('/accounts/bootstrap')
        # assert r.json()['access_token'] == a['access_token']
        
        
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


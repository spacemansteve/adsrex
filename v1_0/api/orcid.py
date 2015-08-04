from ..user_roles import anonymous_user, authenticated_user, bumblebee_user
import requests
import copy

def test_anonymous_user():
    for x in ['/orcid/exchangeOAuthCode', 
              ]:
        r = anonymous_user.get(x)
        assert r.status_code == 401 # right now it throws 500 (probably error with orcid service)

def test_bumblebee_user():
    # getting the 'exchange token' involves logging into orcid
    # and getting the code from the url redirect; but it seems
    # that ORCID allows us to get the code from the endpoint; 
    # but we have to know which url to contact and we have to
    # send username + password; this is obviously brittle and 
    # can break if they change something on their side
    
    redirect_uri = 'http://hourly.adslabs.org/#/user/orcid'
    if 'sandbox' not in authenticated_user.get_config('ORCID_OAUTH_ENDPOINT'):
        redirect_uri = 'https://ui.adsabs.harvard.edu/#/user/orcid'
    
    data = {"errors":[],
            "userName":{"errors":[],
                        "value":authenticated_user.get_config('ORCID_USER'),
                        "required":True,
                        "getRequiredMessage":None},
            "password":{"errors":[],
                        "value":"Orcid123",
                        "required":True,
                        "getRequiredMessage":None},
            "clientId":{"errors":[],
                        "value":authenticated_user.get_config('ORCID_CLIENT_ID'),
                        "required":True,
                        "getRequiredMessage":None},
            "redirectUri":{"errors":[],
                           "value":redirect_uri,
                           "required":True,
                           "getRequiredMessage":None},
            "scope":{"errors":[],
                     "value":"/orcid-profile/read-limited /orcid-works/create /orcid-works/update",
                     "required":True,
                     "getRequiredMessage":None},
            "responseType":{"errors":[],
                            "value":"code",
                            "required":True,
                            "getRequiredMessage":None},
            "approved":True,"persistentTokenEnabled":False}
    
    
    r = requests.post(authenticated_user.get_config('ORCID_OAUTH_ENDPOINT'), json=data)
    redirect = r.json()['redirectUri']['value']
    exchange_code = redirect.split('code=')[1].split('#')[0]
    
    
    # now we can test our own api
    r = bumblebee_user.get('/orcid/exchangeOAuthCode', params={'code': exchange_code})
    assert 'access_token' in r.json()
    assert 'orcid' in r.json()
    assert r.status_code == 200

    # these are the important keys that our own API needs    
    access_token = r.json()['access_token']
    orcid = r.json()['orcid']
    
    
    r = bumblebee_user.get('/orcid/%s/orcid-profile' % orcid, headers={'Orcid-Authorization': 'Bearer %s' % access_token})
    assert 'orcid-profile' in r.json()
    assert r.status_code == 200
    
    data = r.json()
    new_data = {'message-version': '1.2',
                'orcid-profile': {
                      'orcid-activities': {
                         'orcid-works': {
                            'orcid-work': [
                               {
                                 "language-code": None, 
                                 "source": {
                                  "source-orcid": None, 
                                  "source-name": {
                                   "value": "NASA ADS"
                                  }, 
                                  "source-date": {
                                   "value": 1437165488504
                                  }, 
                                  "source-client-id": {
                                   "path": authenticated_user.get_config('ORCID_CLIENT_ID'), 
                                   "host": "sandbox.orcid.org", 
                                   "uri": "http://sandbox.orcid.org/client/APP-P5ANJTQRRTMA6GXZ", 
                                   "value": None
                                  }
                                 }, 
                                 "work-title": {
                                  "translated-title": None, 
                                  "subtitle": None, 
                                  "title": {
                                   "value": "Monte Carlo studies of medium-size telescope designs for the Cherenkov Telescope Array"
                                  }
                                 }, 
                                 "created-date": {
                                  "value": 1437165488504
                                 }, 
                                 "work-citation": None, 
                                 "work-type": "JOURNAL_ARTICLE", 
                                 "publication-date": {
                                  "month": {
                                   "value": "01"
                                  }, 
                                  "day": None, 
                                  "media-type": None, 
                                  "year": {
                                   "value": "2016"
                                  }
                                 }, 
                                 "visibility": "PUBLIC", 
                                 "journal-title": None, 
                                 "work-external-identifiers": {
                                  "scope": None, 
                                  "work-external-identifier": [
                                   {
                                    "work-external-identifier-id": {
                                     "value": "2016APh....72...11W"
                                    }, 
                                    "work-external-identifier-type": "BIBCODE"
                                   }, 
                                   {
                                    "work-external-identifier-id": {
                                     "value": "11002538"
                                    }, 
                                    "work-external-identifier-type": "OTHER_ID"
                                   }, 
                                   {
                                    "work-external-identifier-id": {
                                     "value": "10.1016/j.astropartphys.2015.04.008"
                                    }, 
                                    "work-external-identifier-type": "DOI"
                                   }
                                  ]
                                 }, 
                                 "url": {
                                  "value": "https://ui.adsabs.harvard.edu/#abs/2016APh....72...11W"
                                 }, 
                                 "short-description": "We present studies for optimizing the next generation of ground-based imaging atmospheric Cherenkov telescopes (IACTs).", 
                                 "work-contributors": {
                                  "contributor": [
                                   {
                                    "contributor-orcid": None, 
                                    "contributor-attributes": {
                                     "contributor-role": "AUTHOR", 
                                     "contributor-sequence": None
                                    }, 
                                    "credit-name": {
                                     "visibility": "PUBLIC", 
                                     "value": "Wood, M."
                                    }, 
                                    "contributor-email": None
                                   }, 
                                   {
                                    "contributor-orcid": None, 
                                    "contributor-attributes": {
                                     "contributor-role": "AUTHOR", 
                                     "contributor-sequence": None
                                    }, 
                                    "credit-name": {
                                     "visibility": "PUBLIC", 
                                     "value": "Jogler, T."
                                    }, 
                                    "contributor-email": None
                                   }, 
                                   {
                                    "contributor-orcid": None, 
                                    "contributor-attributes": {
                                     "contributor-role": "AUTHOR", 
                                     "contributor-sequence": None
                                    }, 
                                    "credit-name": {
                                     "visibility": "PUBLIC", 
                                     "value": "Dumm, J."
                                    }, 
                                    "contributor-email": None
                                   }, 
                                   {
                                    "contributor-orcid": None, 
                                    "contributor-attributes": {
                                     "contributor-role": "AUTHOR", 
                                     "contributor-sequence": None
                                    }, 
                                    "credit-name": {
                                     "visibility": "PUBLIC", 
                                     "value": "Funk, S."
                                    }, 
                                    "contributor-email": None
                                   }
                                  ]
                                 }, 
                                 "work-source": None
                                }
                               ]
                            }
                         }
                  } 
                }
    
    # replace all works
    r = bumblebee_user.put('/orcid/%s/orcid-works' % orcid, 
                            headers={'Orcid-Authorization': 'Bearer %s' % access_token},
                            json=new_data)
    assert r.status_code == 200
    
    # over-write the one
    r = bumblebee_user.post('/orcid/%s/orcid-works' % orcid, 
                            headers={'Orcid-Authorization': 'Bearer %s' % access_token},
                            json=new_data)
    assert r.status_code == 201
    
    # get it back
    r = bumblebee_user.get('/orcid/%s/orcid-profile' % orcid, headers={'Orcid-Authorization': 'Bearer %s' % access_token})
    assert 'orcid-profile' in r.json()
    assert r.status_code == 200
    assert len(extract_works(r.json())) == 1
    

def extract_works(orcid_data):
    # orcid data is awful
    out = []
    for x in orcid_data['orcid-profile']['orcid-activities']['orcid-works']['orcid-work']:
        if 'source' in x and \
            x['source'] and \
            'source-client-id' in x['source'] and \
            x['source']['source-client-id'] and \
            'path' in x['source']['source-client-id'] and \
            x['source']['source-client-id']['path'] == authenticated_user.get_config('ORCID_CLIENT_ID'):
            out.append(x)
    return out

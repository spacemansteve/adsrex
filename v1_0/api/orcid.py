from ..user_roles import anonymous_user, authenticated_user, bumblebee_user

def test_anonymous_user():
    for x in ['/orcid/exchangeOAuthCode', 
              ]:
        r = anonymous_user.get(x)
        assert r.status_code == 401 # right now it throws 500 (probably error with orcid service)

def xtest_bumblebee_user():
    for x in ['/orcid/exchangeOAuthCode', 
              ]:
        r = anonymous_user.get(x)
        assert r.status_code == 200
                
def test_orcid_user():
    #1. get orcid token (?) - we can't do that, we have to use a testing token
    #2. retrive profile
    #3. update data
    pass


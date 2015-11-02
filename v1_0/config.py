"""
Configuration file
"""
# encoding: utf-8

# The main endpoint including the version, ie. https://api.adsabs.harvard.edu/v1 
API_BASE = 'http://adsws-staging.elasticbeanstalk.com'
API_VERSION = 'v1'

# OAuth access token for a dedicated user account; we have to create this
# account and give it the normal oauth access rights (and occassionally reset
# it), for now you can replace it with your own

# e.g. access token to tester@ads (on staging)
AUTHENTICATED_USER_EMAIL = 'tester@ads'
# This token is OK to commit, only for the test cluster - not important
AUTHENTICATED_USER_ACCESS_TOKEN = 'Jh5ehrzFtEl2OCoF1DEMCU1ubJlASqlyfKgwGoQ4'

# Those values are necessary only to test 'getting of the access token'
# Orcid service does this inside browser, redirects the user to the correct
# URL and receives the access token etc.

# The same value as in the orcid-microservice config
ORCID_OAUTH_ENDPOINT = 'https://sandbox.orcid.org/oauth/custom/login.json'
# The same value as in orcid-microservice 
ORCID_CLIENT_ID = ''
# A test account that exists inside ORCID
ORCID_USER = ''
# The password in plain text
ORCID_PASS = ''


# Override config with local_config values
try:
    from local_config import *
except Exception as error:
    print 'Unexpected exception: {}'.format(error)

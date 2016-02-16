# encoding: utf-8
"""
Functional tests for the orcid-service
"""

import unittest
import requests
from base import TestBase


class TestOrcidService(TestBase):
    """
    Base class for testing the myADS service
    """
    def test_get_exchange_oauth_unauthorised_user(self):
        """
        Test that an unauthorised user cannot access the orcid/exchangeOAuthCode
        endpoint
        """
        for end_point in ['/orcid/exchangeOAuthCode']:
            r = self.anonymous_user.get(end_point)

            self.assertEqual(
                401,
                r.status_code,
                msg='We expect 401 response for an unauthorised user, '
                    'but get: {}, {}'.format(r.status_code, r.text)
            )

    def helper_extract_works(self, orcid_data):
        """
        Orcid data is awful: collect the relevant entries related to a given
        client ID

        :param orcid_data: ORCID data to bootstrap
        :type orcid_data: dict
        :return: list of entries
        """
        out = []
        for x in orcid_data['orcid-profile']['orcid-activities']['orcid-works']['orcid-work']:
            if 'source' in x and \
                x['source'] and \
                'source-client-id' in x['source'] and \
                x['source']['source-client-id'] and \
                'path' in x['source']['source-client-id'] and \
                x['source']['source-client-id']['path'] == self.authenticated_user.get_config('ORCID_CLIENT_ID'):

                out.append(x)
        return out

    @unittest.skip('Skip until the orcid-login has been fixed, see ticket: adsabs/adsrex/issues#5')
    def test_orcid_workflow(self):
        """
        Test that the ORCID workflow behaves as we expect it to.

        1. Authenticate with ORCID
        2. GET ORCID profile information
        3. Add a selection of work to the ORCID profile
        4. Overwrite the documents we just added

        Getting the 'exchange token' involves logging into orcid and getting the
        code from the url redirect; but it seems that ORCID allows us to get the
        code from the endpoint; but we have to know which url to contact and we
        have to send username + password; this is obviously brittle and can
        break if they change something on their side
        """
        redirect_uri = 'http://hourly.adslabs.org/#/user/orcid'
        if 'sandbox' not in self.authenticated_user.get_config('ORCID_OAUTH_ENDPOINT'):
            redirect_uri = 'https://ui.adsabs.harvard.edu/#/user/orcid'

        data = {
            'errors': [],
            'userName': {
                'errors': [],
                'value': self.authenticated_user.get_config('ORCID_USER'),
                'required': True,
                'getRequiredMessage': None
            },
            'password': {
                'errors': [],
                'value': 'Orcid123',
                'required': True,
                'getRequiredMessage': None
            },
            'clientId': {
                'errors': [],
                'value': self.authenticated_user.get_config('ORCID_CLIENT_ID'),
                'required': True,
                'getRequiredMessage': None
            },
            'redirectUri': {
                'errors': [],
                'value': redirect_uri,
                'required': True,
                'getRequiredMessage': None
            },
            'scope': {
                'errors': [],
                'value': '/orcid-profile/read-limited /orcid-works/create /orcid-works/update',
                'required': True,
                'getRequiredMessage': None
            },
            'responseType': {
                'errors': [],
                'value': 'code',
                'required': True,
                'getRequiredMessage': None
            },
            'approved': True,
            'persistentTokenEnabled': False
        }

        r = requests.post(
            self.authenticated_user.get_config('ORCID_OAUTH_ENDPOINT'),
            json=data
        )

        try:
            redirect = r.json()['redirectUri']['value']
        except Exception as error:
            self.fail('Something is wrong with the setup of the test: {}, {}'
                      .format(error, r.text))
        exchange_code = redirect.split('code=')[1].split('#')[0]

        # now we can test our own api
        r = self.bumblebee_user.get(
            '/orcid/exchangeOAuthCode',
            params={'code': exchange_code}
        )

        self.assertEqual(
            200,
            r.status_code,
            msg='Expected a 200 response, but get: {}, {}'
                .format(r.status_code, r.json())
        )
        self.assertIn(
            'access_token',
            r.json(),
            msg='Expected "access_token" in response, but it is not: {}'
                .format(r.json())
        )
        self.assertIn(
            'orcid',
            r.json(),
            msg='Expected "orcid" in response, but it is not: {}'
                .format(r.json())
        )

        # these are the important keys that our own API needs
        access_token = r.json()['access_token']
        orcid = r.json()['orcid']

        r = self.bumblebee_user.get(
            '/orcid/{}/orcid-profile'.format(orcid),
            headers={'Orcid-Authorization': 'Bearer {}'.format(access_token)}
        )

        self.assertEqual(
            200,
            r.status_code,
            msg='Expected a 200 response, but get: {}, {}'
                .format(r.status_code, r.json())
        )
        self.assertIn(
            'orcid-profile',
            r.json(),
            msg='Expected "orcid-profile" in the response, '
                'but it is not: {}, {}'.format(r.status_code, r.json())
        )

        new_data = {'message-version': '1.2',
                    'orcid-profile': {
                          'orcid-activities': {
                             'orcid-works': {
                                'orcid-work': [
                                   {
                                     'language-code': None,
                                     'source': {
                                      'source-orcid': None,
                                      'source-name': {
                                       'value': 'NASA ADS'
                                      },
                                      'source-date': {
                                       'value': 1437165488504
                                      },
                                      'source-client-id': {
                                       'path': self.authenticated_user.get_config('ORCID_CLIENT_ID'),
                                       'host': 'sandbox.orcid.org',
                                       'uri': 'http://sandbox.orcid.org/client/APP-P5ANJTQRRTMA6GXZ',
                                       'value': None
                                      }
                                     },
                                     'work-title': {
                                      'translated-title': None,
                                      'subtitle': None,
                                      'title': {
                                       'value': 'Monte Carlo studies of medium-size telescope designs for the '
                                                'Cherenkov Telescope Array'
                                      }
                                     },
                                     'created-date': {
                                      'value': 1437165488504
                                     },
                                     'work-citation': None,
                                     'work-type': 'JOURNAL_ARTICLE',
                                     'publication-date': {
                                      'month': {
                                       'value': '01'
                                      },
                                      'day': None,
                                      'media-type': None,
                                      'year': {
                                       'value': '2016'
                                      }
                                     },
                                     'visibility': 'PUBLIC',
                                     'journal-title': None,
                                     'work-external-identifiers': {
                                      'scope': None,
                                      'work-external-identifier': [
                                       {
                                        'work-external-identifier-id': {
                                         'value': '2016APh....72...11W'
                                        },
                                        'work-external-identifier-type': 'BIBCODE'
                                       },
                                       {
                                        'work-external-identifier-id': {
                                         'value': '11002538'
                                        },
                                        'work-external-identifier-type': 'OTHER_ID'
                                       },
                                       {
                                        'work-external-identifier-id': {
                                         'value': '10.1016/j.astropartphys.2015.04.008'
                                        },
                                        'work-external-identifier-type': 'DOI'
                                       }
                                      ]
                                     },
                                     'url': {
                                      'value': 'https://ui.adsabs.harvard.edu/#abs/2016APh....72...11W'
                                     },
                                     'short-description': 'We present studies for optimizing the next generation of'
                                                          ' ground-based imaging atmospheric Cherenkov telescopes '
                                                          '(IACTs).',
                                     'work-contributors': {
                                      'contributor': [
                                       {
                                        'contributor-orcid': None,
                                        'contributor-attributes': {
                                         'contributor-role': 'AUTHOR',
                                         'contributor-sequence': None
                                        },
                                        'credit-name': {
                                         'visibility': 'PUBLIC',
                                         'value': 'Wood, M.'
                                        },
                                        'contributor-email': None
                                       },
                                       {
                                        'contributor-orcid': None,
                                        'contributor-attributes': {
                                         'contributor-role': 'AUTHOR',
                                         'contributor-sequence': None
                                        },
                                        'credit-name': {
                                         'visibility': 'PUBLIC',
                                         'value': 'Jogler, T.'
                                        },
                                        'contributor-email': None
                                       },
                                       {
                                        'contributor-orcid': None,
                                        'contributor-attributes': {
                                         'contributor-role': 'AUTHOR',
                                         'contributor-sequence': None
                                        },
                                        'credit-name': {
                                         'visibility': 'PUBLIC',
                                         'value': 'Dumm, J.'
                                        },
                                        'contributor-email': None
                                       },
                                       {
                                        'contributor-orcid': None,
                                        'contributor-attributes': {
                                         'contributor-role': 'AUTHOR',
                                         'contributor-sequence': None
                                        },
                                        'credit-name': {
                                         'visibility': 'PUBLIC',
                                         'value': 'Funk, S.'
                                        },
                                        'contributor-email': None
                                       }
                                      ]
                                     },
                                     'work-source': None
                                    }
                                   ]
                                }
                             }
                      }
                    }

        # replace all works
        r = self.bumblebee_user.put(
            '/orcid/{}/orcid-works'.format(orcid),
            headers={'Orcid-Authorization': 'Bearer {}'.format(access_token)},
            json=new_data
        )

        self.assertEqual(
            200,
            r.status_code,
            msg='Expected a 200 response, but get: {}, {}'
                .format(r.status_code, r.json())
        )

        # over-write the one
        r = self.bumblebee_user.post(
            '/orcid/{}/orcid-works'.format(orcid),
            headers={'Orcid-Authorization': 'Bearer {}'.format(access_token)},
            json=new_data
        )

        self.assertEqual(
            201,
            r.status_code,
            msg='Expected a 201 response, but get: {}, {}'
                .format(r.status_code, r.json())
        )

        # get it back
        r = self.bumblebee_user.get(
            '/orcid/{}/orcid-profile'.format(orcid),
            headers={'Orcid-Authorization': 'Bearer {}'.format(access_token)}
        )

        self.assertEqual(
            200,
            r.status_code,
            msg='Expected a 200 response, but get: {}, {}'
                .format(r.status_code, r.json())
        )
        self.assertIn(
            'orcid-profile',
            r.json(),
            msg='Expected "orcid-profile" in the response, '
                'but it is not: {}, {}'.format(r.status_code, r.json())
        )
        self.assertEqual(
            1,
            len(self.helper_extract_works(r.json())),
            msg='Length of extract_works should be 1, but is: {}, {}'
                .format(len(self.helper_extract_works(r.json())), r.json())
        )

    def test_crossx_headers(self):
        """
        Test the cross-site origin (CORS) headers and they contain what we
        expect them to
        """
        for endpoint in [
            '/orcid/0000-0001-9886-2511/orcid-works',
            '/orcid/0000-0001-9886-2511/orcid-profile'
        ]:
            r = self.bumblebee_user.options(endpoint)

            self.assertIn('access-control-allow-origin', r.headers)
            self.assertIn('access-control-allow-headers', r.headers)

            self.assertIn(
                'ui.adsabs.harvard.edu',
                r.headers['access-control-allow-origin']
            )
            self.assertIn(
                'Orcid-Authorization',
                r.headers['access-control-allow-headers']
            )

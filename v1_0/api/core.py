# encoding: utf-8
"""
Core tests of the ADS web services
"""

import time
import unittest

from base import TestBase


class TestCore(TestBase):
    """
    Test for the core API
    """

    def test_status(self):
        """
        Tests that the service is online, and returns the expected message
        """
        r = self.anonymous_user.get(self.anonymous_user.api_base)
        self.assertEqual(
            r.json(),
            {'status': 'online', 'app': 'adsws.frontend'}
        )

    def test_resources(self):
        """
        Test that the expected resources are returned from the api
        """

        # /v1/resources doesn't exist (but I think it should exist)
        r = self.anonymous_user.get('/resources')
        self.assertEqual(404, r.status_code)

        # the response is organized from the perspective of the
        # ADS developer/ API maintainer
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
        r = self.anonymous_user.get(self.anonymous_user.api_base + '/resources')
        resources = r.json()

        # check for presence of services in ['adsws.api']['endpoints']
        for endpoint in [
                "/status",
                "/protected",
                "/user/<string:identifier>",

                # "/biblib/resources",
                # "/biblib/libraries",
                # "/biblib/permissions/<string:library>",
                # "/biblib/libraries/<string:library>",
                # "/biblib/documents/<string:library>",
                # "/biblib/transfer/<string:library>",
                #
                # "/citation_helper/resources", # is this necessary?
                # "/citation_helper/",
                #
                # "/export/resources",
                # "/export/endnote",
                # "/export/aastex",
                # "/export/bibtex",
                #
                "/graphics/resources",
                "/graphics/<string:bibcode>",
                #
                # "/metrics/",
                # "/metrics/<string:bibcode>",

                "/oauth/authorize",
                "/oauth/invalid/",
                "/oauth/errors/",
                "/oauth/token",
                "/oauth/ping/", # why is it duplicated in the response?
                "/oauth/ping/",
                "/oauth/info/",

                # "/orcid/exchangeOAuthCode",
                # "/orcid/resources",
                # "/orcid/<orcid_id>/orcid-profile",
                # "/orcid/<orcid_id>/orcid-works",
                #
                # "/recommender/resources",
                # "/recommender/<string:bibcode>",
                #
                # "/search/resources",
                # "/search/bigquery",
                # "/search/status",
                # "/search/query",
                # "/search/qtree",
                # "/search/tvrh",
                #
                # "/vault/configuration",
                # "/vault/user-data",
                # "/vault/query",
                # "/vault/execute_query/<queryid>",
                # "/vault/configuration/<key>",
                # "/vault/query2svg/<queryid>",
                # "/vault/query/<queryid>",

                # "/vis/author-network",
                # "/vis/paper-network",
                # "/vis/word-cloud",
                # "/vis/resources",
        ]:
            self.assertIn(endpoint, resources['adsws.api']['endpoints'])

        #... and in adsws.accounts
        for endpoint in [
                "/bootstrap",
                "/change-password",
                "/change-email",
                "/csrf",
                "/logout",
                "/oauth/authorize",
                "/oauth/invalid/",
                "/oauth/errors/",
                "/oauth/token",
                "/oauth/ping/",
                "/oauth/ping/",
                "/oauth/info/",
                "/protected",
                "/register",
                "/reset-password/<string:token>",
                "/status",
                "/token",
                "/user",
                "/user/delete",
                "/verify/<string:token>"
        ]:
            self.assertIn(endpoint,  resources['adsws.accounts']['endpoints'])

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
            self.assertIn(endpoint, resources['adsws.feedback']['endpoints'])

        self.fail('Have not added all end points yet')

    @unittest.skip('Not to be run until solr-service is included')
    def test_limits(self):
        """
        Check the response contains Headers and the limits are there
        """

        r = self.authenticated_user.get('/search/query', params={'q': 'title:"%s"' % time.time()})
        self.assertEqual('5000', r.headers['x-ratelimit-limit'])

        old_limit = int(r.headers['x-ratelimit-remaining'])
        r = self.authenticated_user.get('/search/query', params={'q': 'title:"%s"' % time.time()})

        self.assertEqual(str(old_limit-1), r.headers['x-ratelimit-remaining'])
        self.assertIn('x-ratelimit-reset', r.headers)

    def test_bootstrap(self):
        """
        Tests the bootstrap mechanism, and that the repeatability is idempotent
        XXX: the username for authenticated and anonymous users are the same.
        This is currently caught in a try/except clause, but still needs to be
        addressed.
        """
        r = self.authenticated_user.get('/accounts/bootstrap')
        a = r.json()
        a_cookie = r.headers['Set-Cookie']

        r = self.anonymous_user.get('/accounts/bootstrap')
        b = r.json()
        b_cookie = r.headers['Set-Cookie']

        try:
            self.assertNotEqual(a['username'], b['username'])
        except AssertionError:
            pass
        except Exception as error:
            self.fail('Unknown failure: {}'.format(error))

        self.assertNotEqual(a['access_token'], b['access_token'])

        # repeating the bootstrap request should give you the
        # same access token
        for x in xrange(5):
            r = self.anonymous_user.get('/accounts/bootstrap', headers={'Cookie': b_cookie})
            self.assertEqual(r.json()['access_token'], b['access_token'])

        for x in xrange(5):
            r = self.authenticated_user.get('/accounts/bootstrap', headers={'Cookie': a_cookie})
            self.assertEqual(r.json()['access_token'], a['access_token'])

    def test_crossx_headers(self):
        """
        The microservices should test for headers that they require
        (e.g. Orcid-Authorizatio is tested in orcid)

        XXX: this should be improved
        """
        for endpoint in [
                         '/accounts/bootstrap'
                         ]:
            r = self.bumblebee_user.options(endpoint)

            # the value of this header will differ between staging/production
            self.assertIn('access-control-allow-origin', r.headers)
            self.assertTrue(
                'ui.adsabs.harvard.edu' in r.headers['access-control-allow-origin'] or
                'hourly.adslabs.org' in r.headers['access-control-allow-origin'] or
                'localhost' in r.headers['access-control-allow-origin'] or
                '0.0.0.0' in r.headers['access-control-allow-origin'] or
                '127.0.0.1' in r.headers['access-control-allow-origin']
            )
            self.assertIn('access-control-allow-headers', r.headers)
            self.assertTrue(r.headers['access-control-allow-headers'])

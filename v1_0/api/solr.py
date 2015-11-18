"""
Integration tests for the Recommender service

'solr-service' is synonymous with 'search' when looking at the end points on the API
"""

import time
from base import TestBase


class TestSolr(TestBase):
    """
    Tests for the Solr Service
    """
    def test_limits(self):
        """
        Check the response contains Headers and the limits are there
        """

        r = self.authenticated_user.get('/search/query', params={'q': 'title:"{}"'.format(time.time())})
        self.assertEqual('5000', r.headers['x-ratelimit-limit'])

        old_limit = int(r.headers['x-ratelimit-remaining'])
        r = self.authenticated_user.get('/search/query', params={'q': 'title:"{}"'.format(time.time())})

        self.assertEqual(str(old_limit-1), r.headers['x-ratelimit-remaining'])
        self.assertIn('x-ratelimit-reset', r.headers)

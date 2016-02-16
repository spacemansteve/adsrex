# encoding: utf-8
"""
Functional tests for the Citation Helper service
"""

from base import TestBase


class TestCitationHelper(TestBase):
    """
    Base class for testing the graphics service
    """
    def setUp(self):
        """
        Generic setup. Updated to include a test bibcode.
        """
        super(TestCitationHelper, self).setUp()
        self.test_bibcodes = ['1980ApJS...44..169S', '1980ApJS...44..193S']

    def test_anonymous_user_existing_bibcode(self):
        """
        Test an unauthenticated user has no access to the citation helper for a
        GET request for all the bibcodes sent
        """
        # Request all metrics for two existing bibcodes
        r = self.anonymous_user.post(
            '/citation_helper', json={'bibcodes': self.test_bibcodes}
        )
        self.assertEqual(
            r.status_code,
            401,
            msg='We expect a 401 unauthorized error, but get: {}, {}'
                .format(r.status_code, r.json())
        )
        
    def helper_authenticated_user_get_request(self, user=None):
        """
        Test that an authenaticated user has access to the GET end point for a
        list of bibcodes and that the response contains the expected content.
        :param user: the user to run the test on
        :type user: object
        """
        r = user.post('/citation_helper', json={'bibcodes': self.test_bibcodes})
        self.assertEqual(
            r.status_code,
            200,
            msg='We should get a 200 response for a request including two '
                'bibcodes, but instead we get: {}, {}'
                .format(r.status_code, r.json())
        )

        self.assertIsInstance(
            r.json(),
            list,
            msg='Response content should be of type list, but are type: {}, {}'
                .format(type(r.json()), r.json())
        )
        # and all list items should be dictionaries
        expected_attr = ['title', 'bibcode', 'score', 'author']
        for item in r.json():
            self.assertIsInstance(
                item,
                dict,
                msg='All list items should be dictionaries, '
                    'but not this: "{}" is type {}'.format(item, type(item))
            )

            actual_attr = item.keys()
            self.assertListEqual(
                actual_attr,
                expected_attr,
                msg='There are mising attributes, expected {} != actual {}'
                    .format(expected_attr, actual_attr)
            )

    def test_authenticated_user_get_request(self):
        """
        Test that all types of authenticated users can access the citation
        helper GET end point, and get the expected content in the response
        """
        self.helper_authenticated_user_get_request(user=self.authenticated_user)
        self.helper_authenticated_user_get_request(user=self.bumblebee_user)

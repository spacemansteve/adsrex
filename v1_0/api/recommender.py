# encoding: utf-8
"""
Functional tests for the Recommender service
"""

from base import TestBase


class TestRecommender(TestBase):
    """
    Base class for testing the graphics service
    """
    def setUp(self):
        """
        Generic setup. Updated to include a test bibcode.
        """
        super(TestRecommender, self).setUp()
        self.test_bibcode = '2010MNRAS.409.1719J'

    def test_anonymous_user_existing_bibcode(self):
        """
        Test an unauthenticated user has no access to the recommender for an
        existing bibcode
        """
        r = self.anonymous_user.get('/recommender/{}'.format(self.test_bibcode))
        self.assertEqual(
            r.status_code,
            401,
            msg='Should get 401 when trying to get graphics for an '
                'existing bibcode, but get: {}, {}'
                .format(r.status_code, r.json())
        )

    def test_anonymous_user_non_existent_bibcode(self):
        """
        Test an unauthenticated user has no access to the recommender even for a
        non-existent bibcode
        """
        r = self.anonymous_user.get('/recommender/foo')
        self.assertEqual(
            r.status_code,
            401,
            msg='Should get 401 when trying to get graphics for a '
                'non-existient bibcode, but get: {}, {}'
                .format(r.status_code, r.json())
        )

    def help_authenticated_user_get(self, user=None):
        """
        Test that authenticated user can access the get end point for a given
        bibcode
        :param user: the user to run the test on
        :type user: object
        """
        r = user.get('/recommender/{}'.format(self.test_bibcode))
        self.assertEqual(
            r.status_code,
            200,
            msg='We should get 200 for an existing bibcode "{}", '
                'but get: {}, {}'
                .format(self.test_bibcode, r.status_code, r.text)
        )

        data = r.json()
        self.assertIn(
            'paper',
            data,
            msg='Keyword: "paper" not in data: {}'.format(data)
        )
        self.assertEqual(
            data['paper'],
            self.test_bibcode,
            msg='Response data structure should contain the bibcode, '
                'but does not: {}'.format(data)
        )

        self.assertIn(
            'recommendations',
            data,
            msg='Response data should have "recommendations" attribute, '
                'but does not: {}, {}'.format(data.keys(), data)
        )

        self.assertIsInstance(
            data['recommendations'],
            list,
            msg='Recommendation should be in a list, but are type: {}, {}'
                .format(type(data['recommendations']), data['recommendations'])
        )

        expected_attr = ['title', 'bibcode', 'author']
        for item in data['recommendations']:

            self.assertIsInstance(
                item,
                dict,
                msg='Items should be a dict but are type: {}, {}'
                    .format(type(item), item)
            )

            actual_attr = item.keys()
            self.assertEqual(
                actual_attr.sort(),
                expected_attr.sort(),
                msg='Expected "{}" != Actual "{}"'
                    .format(expected_attr, actual_attr)
            )

    def test_authenticated_user_get(self):
        """
        Authenaticated users should be able to use the get end point, and the
        response should be as we expect
        """
        self.help_authenticated_user_get(user=self.authenticated_user)
        self.help_authenticated_user_get(user=self.bumblebee_user)

    def test_authenticated_user_non_existent_bibcode(self):
        """
        Test that an authenticated user can use the get end point for a
        non-existent bibcode, but that the response tells us the bibcode does
        not exist
        """
        r = self.authenticated_user.get('/recommender/foobar')
        self.assertEqual(
            r.status_code,
            200,
            msg='Non-existent bibcode should return 200, but returns: {}, {}'
                .format(r.status_code, r.text)
        )
        self.assertIn(
            'Error',
            r.json(),
            msg='Non-existent bibcode should return an Error attribute, '
                'but does not: {} [status: {}]'
                .format(r.json(), r.status_code)
        )

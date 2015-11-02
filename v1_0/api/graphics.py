"""
Integration tests for the Graphics service
"""

from base import TestBase


class TestGraphics(TestBase):
    """
    Base class for testing the graphics service
    """
    def setUp(self):
        """
        Generic setup. Updated to include a test bibcode.
        """
        super(TestGraphics, self).setUp()
        self.test_bibcode = '1995ApJ...447L..37W'

    def test_unauthenticated_get_graphics(self):
        """
        Tests the get end point of graphics
        """
        r = self.anonymous_user.get('/graphics/{}'.format(self.test_bibcode))
        self.assertEqual(
            401,
            r.status_code,
            msg='This user should receive a 401, not {}'.format(r.status_code)
        )

        r = self.anonymous_user.get('graphics/foo')
        self.assertEqual(
            401,
            r.status_code,
            msg='This is a non-existing bibcode, it should return a 401 not {}'.format(r.status_code)
        )

    def test_authenticated_user(self):
        """

        :return:
        """
    def helper_test_authenticated_user_get(self, user):
        """
        Check that getting graphics from GET end point works as expected.

        :param user: the user to run the test on
        :type user: object
        """
        url = '/graphics/{}'.format(self.test_bibcode)

        r = user.get(url)
        self.assertEqual(r.status_code, 200)

        # Now test what was sent back
        data = r.json()
        self.assertEqual(
            data['bibcode'],
            self.test_bibcode,
            msg='The data structure sent back has a "bibcode" entry, which should contain the request bibcode'
        )

        self.assertFalse(
            data['eprint'],
            msg='eprint attribrudge should be False, but is: {}'.format(data['eprint'])
        )

        self.assertIsInstance(
            data['figures'],
            list,
            msg='The attribute "figures" should be a list: type is {}'.format(type(data['figures']))
        )
        #
        self.assertTrue(
            len(data['figures']) > 0,
            msg='The list of figures should not be empty: length = {}'.format(len(data['figures']))
        )

        expected_attr = [u'images', u'figure_caption', u'figure_label', u'figure_id']
        self.assertListEqual(
            data['figures'][0].keys(),
            expected_attr,
            msg='A figure in the list of figures should have expected attributes. Expected {} got {}'
                .format(expected_attr, data['figures'][0].keys())
        )
        #
        self.assertIsInstance(
            data['figures'][0]['images'],
            list,
            msg='The attribute "images" refers to a list but has type: {}'.format(type(data['figures'][0]['images']))
        )

        #
        self.assertTrue(
            len(data['figures'][0]['images']) > 0,
            msg='The list of images should not be empty, but has length: {}'.format(len(data['figures'][0]['images']))
        )

        im_attr = [u'image_id', u'format', u'thumbnail', u'highres']
        for im in data['figures'][0]['images']:
            self.assertIsInstance(
                im,
                dict,
                msg='Should be a dictionary, but is: {}'.format(type(im))
            )
            self.assertListEqual(
                im.keys(),
                im_attr,
                msg='Expected attributes {} != {}'.format(im_attr, im.keys())
            )

    def test_authenticated_user_get(self):
        """
        Tests the graphics GET end point for all types of authenticated users. They should all receive the same
        response, otherwise something is wrong.
        """
        self.helper_test_authenticated_user_get(user=self.authenticated_user)
        self.helper_test_authenticated_user_get(user=self.bumblebee_user)

    def helper_test_authenticated_user_non_existent_bibcode(self, user):
        """
        Check that the graphics GET end point works as expected if there is no corresponding bibcode. This is a helper
        function that allows it to be run on a give user.
        :param user: the user to run the test on
        :type user: object
        """
        url = '/graphics/foo'
        r = user.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertIn(
            'Error',
            r.json(),
            msg='The data structure sent back should have an "Error" attribute, but does not: {}'.format(r.json())
        )

    def test_authenticated_user_non_existent_bibcode(self):
        """
        A non-existing bibcode should still return a 200
        """
        self.helper_test_authenticated_user_non_existent_bibcode(user=self.anonymous_user)
        self.helper_test_authenticated_user_non_existent_bibcode(user=self.bumblebee_user)

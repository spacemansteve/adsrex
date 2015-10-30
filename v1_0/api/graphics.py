from ..user_roles import anonymous_user, authenticated_user, bumblebee_user
from unittest import TestCase
    
bibcode = '1995ApJ...447L..37W'
    
class GraphicsServiceTest(TestCase):
    def test_anonymous_user(self):
        # Try to get graphics info for an existing bibcode
        r = anonymous_user.get('/graphics/%s'%bibcode)
        # We should get a 401 back
        self.assertEqual(r.status_code, 401)
        # The same for a non-existing bibcode
        r = anonymous_user.get('/graphics/foo')
        # We should get a 401 back
        self.assertEqual(r.status_code, 401)
    
    def test_authenticated_user(self, user=authenticated_user):
        # Get graphics for an existing bibcode
        r = user.get('/graphics/%s'%bibcode)
        # We should get a 200 back
        self.assertEqual(r.status_code, 200)
        # Now we'll test the contents of what was sent back
        data = r.json()
        # The data structure sent back has a 'bibcode' entry,
        # which should contain the request bibcode
        self.assertEqual(data['bibcode'], bibcode)
        # and the 'eprint' attribute should say False
        self.assertFalse(data['eprint'])
        # The attribute 'figures' should be a list
        self.assertIsInstance(data['figures'], list)
        # The list of figures should not be empty
        self.assertTrue(len(data['figures']) > 0)
        # A figure in the list of figures should have expected attributes
        expected_attr = [u'images', u'figure_caption', u'figure_label', u'figure_id']
        self.assertListEqual(data['figures'][0].keys(), expected_attr)
        # The attribute 'images' refers to a list
        self.assertIsInstance(data['figures'][0]['images'], list)
        # The list of images should not be empty
        self.assertTrue(len(data['figures'][0]['images']) > 0)
        # The list of images should contain dictionaries
        # with expected attributes
        im_attr = [u'image_id', u'format', u'thumbnail', u'highres']
        for im in data['figures'][0]['images']:
            self.assertIsInstance(im, dict)
            self.assertListEqual(im.keys(), im_attr)
        # A non-existing bibcode should still return a 200
        r = user.get('/graphics/foo')
        self.assertEqual(r.status_code, 200)
        # But the data structure sent back should have an 'Error' attribute
        self.assertIn('Error', r.json())
    
    def test_bumblebee_user(self):
        self.test_authenticated_user(user=bumblebee_user)

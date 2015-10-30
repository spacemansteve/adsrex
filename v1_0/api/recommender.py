from ..user_roles import anonymous_user, authenticated_user, bumblebee_user
from unittest import TestCase
    
bibcode = '2010MNRAS.409.1719J'
    
class RecommenderServiceTest(TestCase):
    def test_anonymous_user(self):
        # Try to get graphics info for an existing bibcode
        r = anonymous_user.get('/recommender/%s'%bibcode)
        # We should get a 401 back
        self.assertEqual(r.status_code, 401)
        # The same for a non-existing bibcode
        r = anonymous_user.get('/recommender/foo')
        # We should get a 401 back
        self.assertEqual(r.status_code, 401)
    
    def test_authenticated_user(self, user=authenticated_user):
        # Get graphics for an existing bibcode
        r = user.get('/recommender/%s'%bibcode)
        # We should get a 200 back
        self.assertEqual(r.status_code, 200)
        # Now we'll test the contents of what was sent back
        data = r.json()
        # The data structure should contain the request bibcode
        self.assertEqual(data['paper'], bibcode)
        # and it should have a 'recommendations' attribute
        self.assertIn('recommendations', data)
        # The recommendations should be in a list
        self.assertIsInstance(data['recommendations'], list)
        # the elements of which are dictionaries, with attributes 'title',
        # 'bibcode' and 'author'
        expected_attr = ['title', 'bibcode', 'author']
        for item in data['recommendations']:
            self.assertIsInstance(item, dict)
            self.assertListEqual(item.keys(), expected_attr)
        # Offering a non-existing bibcode to the Recommender should return
        # a 200 status with 'Error' as key in the returned data structure
        r = user.get('/recommender/foo')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Error', r.json())
    
    def test_bumblebee_user(self):
        self.test_authenticated_user(user=bumblebee_user)
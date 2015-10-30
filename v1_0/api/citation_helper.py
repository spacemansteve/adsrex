from ..user_roles import anonymous_user, authenticated_user, bumblebee_user
from unittest import TestCase
    
bibcodes = ["1980ApJS...44..169S","1980ApJS...44..193S"]

class CitationHelperServiceTest(TestCase):    
    def test_anonymous_user(self):
        # Request all metrics for two existing bibcodes
        r = anonymous_user.post('/citation_helper', json={'bibcodes': bibcodes})
        # We should get a 401 status
        self.assertEqual(r.status_code, 401)
        
    def test_authenticated_user(self, user=authenticated_user):
        # Request all metrics for two existing bibcodes
        r = user.post('/citation_helper', json={'bibcodes': bibcodes})
        # We should get a 200 status
        self.assertEqual(r.status_code, 200)
        # The results should be in a list
        self.assertIsInstance(r.json(), list)
        # and all list items should be dictionaries
        expected_attr = ['title', 'bibcode', 'score', 'author']
        for item in r.json():
            self.assertIsInstance(item, dict)
            self.assertListEqual(item.keys(), expected_attr)
    
    def test_bumblebee_user(self):
        self.test_authenticated_user(user=bumblebee_user)

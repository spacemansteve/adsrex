from ..user_roles import anonymous_user, authenticated_user, bumblebee_user
from unittest import TestCase
    
# We will do all tests for the famous author A. Accomazzi
params = {}
params['q'] = 'author:"Accomazzi,A"'

class AuthorNetworkTest(TestCase):
    def test_anonymous_user(self):
        # Get the author network
        r = anonymous_user.post('/vis/author-network', params=params)
        # We should get a 401 back
        self.assertEqual(r.status_code, 401)

    def check_author_network(self, user=authenticated_user):
        ## Examine the paper network
        # Retrieve results for our query in 'params'
        r = user.post('/vis/author-network', params=params)
        # We should get a 200 back
        self.assertEqual(r.status_code, 200)
        # Now we'll test the contents of what was sent back
        data = r.json()
        # We are sent back a dictionary
        self.assertIsInstance(data, dict)
        # This dictionary has two keys: 'msg' and 'data'
        self.assertIn('msg', data)
        self.assertIn('data', data)
        # Check the attributes of the 'data' entry
        expected_attr = [u'bibcode_dict', u'root', u'link_data']
        self.assertItemsEqual(expected_attr, data['data'].keys())
        # We expect the 'bibcode_dict' to be a dictionary of dictionaries
        bib_attr = ['read_count','title','citation_count','authors']
        for bibcode, bibinfo in data['data']['bibcode_dict'].items():
            # Extremely basic bibcode format check
            self.assertEqual(len(bibcode), 19)
            # Value should be a dictionary with expected keys
            self.assertIsInstance(bibinfo, dict)
            self.assertItemsEqual(bib_attr, bibinfo.keys())
        # The 'root' entry should have two attributes: 'name' and 'children'
        self.assertIn('name', data['data']['root'])
        self.assertIn('children', data['data']['root'])
        # The 'children' entry should be a list of dictionaries
        self.assertIsInstance(data['data']['root']['children'], list)
        # Only check that the first entry has the expected attributes
        self.assertIn('name', data['data']['root']['children'][0])
        self.assertIn('children', data['data']['root']['children'][0])
        # The 'link_data' entry is a lists of lists
        self.assertIsInstance(data['data']['link_data'], list)
        for item in data['data']['link_data']:
            # Each item is a list
            self.assertIsInstance(item, list)
            # and specifically a list of numbers
            self.assertTrue(all(isinstance(int(x), int) for x in item))

    def test_authenticated_user(self):
        self.check_author_network()

    def test_bumblebee_user(self):
        self.check_author_network(user=bumblebee_user)

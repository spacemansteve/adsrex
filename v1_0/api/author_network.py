from ..user_roles import anonymous_user, authenticated_user, bumblebee_user
from unittest import TestCase
    
# We will do all tests for a single bibcode query
params = {}
params['bibcodes'] = ['2012ASPC..461..763H']

class AuthorNetworkTest(TestCase):
    def test_anonymous_user(self):
        # Get the author network
        r = anonymous_user.post('/vis/author-network', json=params)
        # We should get a 401 back
        self.assertEqual(r.status_code, 401)

    def check_author_network(self, user=authenticated_user):
        ## Examine the paper network
        # Retrieve results for our query in 'params'
        r = user.post('/vis/author-network', json=params)
        # We should get a 200 back
        self.assertEqual(r.status_code, 200)
        # Now we'll test the contents of what was sent back
        j = r.json()
        # We are sent back a dictionary
        self.assertIsInstance(j, dict)
        # This dictionary has two keys: 'msg' and 'data'
        self.assertIn('msg', j)
        self.assertIn('data', j)
        # Check the attributes of the 'data' entry, top level is just full graph
        data = j['data']
        expected_attrs = [u'fullGraph']
        self.assertItemsEqual(expected_attrs, j['data'].keys())
        fullGraph = j['data']['fullGraph']
        # fullGraph is a dict with nodes and links
        self.assertIsInstance(fullGraph, dict)
        self.assertIn('nodes', fullGraph)
        self.assertIn('links', fullGraph)
        nodes = fullGraph['nodes']
        self.assertIsInstance(nodes, list)
        links = fullGraph['links']
        self.assertIsInstance(links, list)


    def test_authenticated_user(self):
        self.check_author_network()

    def test_bumblebee_user(self):
        self.check_author_network(user=bumblebee_user)

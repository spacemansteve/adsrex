from ..user_roles import anonymous_user, authenticated_user, bumblebee_user
from unittest import TestCase
    
# We will do all tests using a single bibcode query
params = {}
params['bibcodes'] = ['2012ASPC..461..763H']

class PaperNetworkTest(TestCase):
    def test_anonymous_user(self):
        # Try to get the paper network
        r = anonymous_user.post('/vis/paper-network', json=params)
        # We should get a 401 back
        self.assertEqual(r.status_code, 401)

    def check_paper_network(self, user=authenticated_user):
        ## Examine the paper network
        # Retrieve results for our query in 'params'
        r = user.post('/vis/paper-network', json=params)
        # We should get a 200 back
        self.assertEqual(r.status_code, 200)
        # Now we'll test the contents of what was sent back
        pdata = r.json()
        # We are sent back a dictionary
        self.assertIsInstance(pdata, dict)
        # This dictionary has two keys: 'msg' and 'data'
        self.assertIn('msg', pdata)
        self.assertIn('data', pdata)
        # The 'data' attribute has a 'fullGraph' dict
        self.assertIn('fullGraph', pdata['data'])
        # the full graph has a nodes and a links
        fullGraph = pdata['data']['fullGraph']
        self.assertIsInstance(fullGraph, dict)
        self.assertIn('nodes', fullGraph)
        self.assertIn('links', fullGraph)
        # nodes and links hold arrays
        nodes = fullGraph['nodes']
        links = fullGraph['links']
        self.assertIsInstance(nodes, list)
        self.assertIsInstance(links, list)


    def test_authenticated_user(self):
        self.check_paper_network()

    def test_bumblebee_user(self):
        self.check_paper_network(user=bumblebee_user)

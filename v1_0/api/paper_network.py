from ..user_roles import anonymous_user, authenticated_user, bumblebee_user
from unittest import TestCase
    
# We will do all tests for the famous author A. Accomazzi
params = {}
params['q'] = 'author:"Accomazzi,A"'

class PaperNetworkTest(TestCase):
    def test_anonymous_user(self):
        # Try to get the paper network
        r = anonymous_user.get('/vis/paper-network', params=params)
        # We should get a 401 back
        self.assertEqual(r.status_code, 401)

    def check_paper_network(self, user=authenticated_user):
        ## Examine the paper network
        # Retrieve results for our query in 'params'
        r = user.get('/vis/paper-network', params=params)
        # We should get a 200 back
        self.assertEqual(r.status_code, 200)
        # Now we'll test the contents of what was sent back
        pdata = r.json()
        # We are sent back a dictionary
        self.assertIsInstance(pdata, dict)
        # This dictionary has two keys: 'msg' and 'data'
        self.assertIn('msg', pdata)
        self.assertIn('data', pdata)
        # The 'data' attribute has two keys: 'summaryGraph', 'fullGraph'
        self.assertIn('summaryGraph', pdata['data'])
        self.assertIn('fullGraph', pdata['data'])
        # Both graphs have the same attributes
        expected_attr = [u'directed', u'graph', u'nodes', u'links', u'multigraph']
        self.assertItemsEqual(expected_attr, pdata['data']['summaryGraph'].keys())
        self.assertItemsEqual(expected_attr, pdata['data']['fullGraph'].keys())
        # The 'nodes' and 'links' attributes are lists of dictionaries in both graphs
        # Check the summaryGraph
        # First examine the nodes
        graph = pdata['data']['summaryGraph']
        self.assertIsInstance(graph['nodes'], list)
        expected_attr = [u'paper_count', u'node_label', u'total_citations', u'node_name', u'top_common_references', u'total_reads', u'stable_index', u'id']
        for item in graph['nodes']:
            self.assertIsInstance(item, dict)
            self.assertItemsEqual(expected_attr, item.keys())
        # Now examine the links
        self.assertIsInstance(graph['links'], list)
        expected_attr = [u'source', u'target', u'weight']
        for item in graph['links']:
            self.assertIsInstance(item, dict)
            self.assertItemsEqual(expected_attr, item.keys())
        # Now check the fullGraph
        # First examine the nodes
        graph = pdata['data']['fullGraph']
        self.assertIsInstance(graph['nodes'], list)
        expected_attr = [u'read_count', u'group', u'title', u'first_author', u'citation_count', u'node_name', u'id', u'nodeWeight']
        for item in graph['nodes']:
            self.assertIsInstance(item, dict)
            self.assertItemsEqual(expected_attr, item.keys())
        # Now examine the links
        self.assertIsInstance(graph['links'], list)
        expected_attr = [u'source', u'weight', u'overlap', u'target']
        for item in graph['links']:
            self.assertIsInstance(item, dict)
            self.assertItemsEqual(expected_attr, item.keys())

    def test_authenticated_user(self):
        self.check_paper_network()

    def test_bumblebee_user(self):
        self.check_paper_network(user=bumblebee_user)
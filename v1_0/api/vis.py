"""
Integration tests for the visualisation services service
"""

from base import TestBase


class TestPaperNetwork(TestBase):
    """
    Base class for testing the paper-network end point of the visualisation services
    """
    def setUp(self):
        """
        Generic setup. Updated to include a test bibcode.
        """
        super(TestPaperNetwork, self).setUp()
        self.test_params = dict(q='author:"^Accomazzi, A."')

    def test_get_reqest_unauthorized_user(self):
        """
        Show that you cannot get a paper-network for an unauthorized user
        """
        r = self.anonymous_user.get('/vis/paper-network', params=self.test_params)
        # We should get a 401 back
        self.assertEqual(
            r.status_code,
            401,
            msg='We should get a 401 for unauthozied access, but get: {}, {}'
                .format(r.status_code, r.json())
        )

    def helper_check_paper_network(self, user=None):
        """
        Tests the get end point of the paper-network for the visualisation services for an authorized user.
        :param user: the user to run the test on
        :type user: object
        """
        r = user.get('/vis/paper-network', params=self.test_params)

        self.assertEqual(
            r.status_code,
            200,
            msg='We should get 200 for our params, but get: {}, {}'
                .format(r.status_code, r.json())
        )

        pdata = r.json()
        self.assertIsInstance(
            pdata,
            dict,
            msg='Response should be of type dict, but is of type: {}, {}'
                .format(type(pdata), pdata)
        )

        expected_attr = ['msg', 'data']
        actual_attr = pdata.keys()
        self.assertEqual(
            expected_attr.sort(),
            actual_attr.sort(),
            msg='Response should contain keywords: {} but does not: {}'.format(expected_attr, actual_attr)
        )

        expected_attr = ['summaryGraph', 'fullGraph']
        actual_attr = pdata['data'].keys()
        self.assertEqual(
            expected_attr.sort(),
            actual_attr.sort(),
            msg='Data keywould should contain {}, but does not: {}'.format(expected_attr, actual_attr)
        )

        expected_attr = [u'directed', u'graph', u'nodes', u'links', u'multigraph']
        actual_attr = pdata['data']['summaryGraph'].keys()
        self.assertEqual(
            expected_attr,
            actual_attr,
            msg='Both graphs should have the same attributes {}, but do not: {}'.format(expected_attr, actual_attr)
        )
        actual_attr = pdata['data']['fullGraph'].keys()
        self.assertEqual(
            expected_attr,
            actual_attr,
            msg='Both graphs should have the same attributes {}, but do not: {}'.format(expected_attr, actual_attr)
        )

        graph = pdata['data']['summaryGraph']
        self.assertIsInstance(
            graph['nodes'],
            list,
            msg='Nodes should be type list, but is type: {}, {}'.format(type(graph['nodes']), graph['nodes'])
        )

        expected_attr = [u'paper_count', u'node_label', u'total_citations', u'node_name',
                         u'top_common_references', u'total_reads', u'stable_index', u'id']
        for item in graph['nodes']:
            self.assertIsInstance(
                item,
                dict,
                msg='Content of nodes list should be dict, but is: {}, {}'.format(type(item), item)
            )
            actual_attr = item.keys()
            self.assertEqual(
                expected_attr.sort(),
                actual_attr.sort(),
                msg='We expect the following attributes {} but do not get them: {}'.format(expected_attr, actual_attr)
            )

        self.assertIsInstance(
            graph['links'],
            list,
            msg='Links should be type list, but is type: {}, {}'.format(type(graph['links']), graph['links'])
        )

        expected_attr = [u'source', u'target', u'weight']
        for item in graph['links']:
            self.assertIsInstance(
                item,
                dict,
                msg='Content of links should be a dict, but is: {}, {}'.format(type(item), item)
            )
            actual_attr = item.keys()
            self.assertItemsEqual(
                expected_attr.sort(),
                actual_attr.sort(),
                msg='We expect the following attributes {} but do not get them {}'.format(expected_attr, actual_attr)
            )

        graph = pdata['data']['fullGraph']
        self.assertIsInstance(
            graph['nodes'],
            list,
            msg='Nodes should be type list, but is type: {}, {}'.format(type(graph['nodes']), graph['nodes'])
        )

        expected_attr = [u'read_count', u'group', u'title', u'first_author',
                         u'citation_count', u'node_name', u'id', u'nodeWeight']
        for item in graph['nodes']:
            self.assertIsInstance(
                item,
                dict,
                msg='Content of nodes list should be dict, but is: {}, {}'.format(type(item), item)
            )
            actual_attr = item.keys()
            self.assertItemsEqual(
                expected_attr,
                actual_attr,
                msg='We expect the following attributes {} but do not get them {}'.format(expected_attr, actual_attr)
            )

        self.assertIsInstance(
            graph['links'],
            list,
            msg='Links should be type list, but is type: {}, {}'.format(type(graph['links']), graph['links'])
        )

        expected_attr = [u'source', u'weight', u'overlap', u'target']
        for item in graph['links']:
            self.assertIsInstance(
                item,
                dict,
                msg='Content of links list should be dict, but is: {}, {}'.format(type(item), item)
            )
            actual_attr = item.keys()
            self.assertItemsEqual(
                expected_attr,
                actual_attr,
                msg='We expect the following attributes {} but do not get them {}'.format(expected_attr, actual_attr)
            )

    def test_get_request_authorized_user(self):
        self.helper_check_paper_network(user=self.authenticated_user)
        self.helper_check_paper_network(user=self.bumblebee_user)

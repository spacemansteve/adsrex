"""
Integration tests for the visualisation services service
"""

import json
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
        self.test_params = dict(query=['{"q": "author:\\"Elliott, J.\\""}'])

    def test_get_request_unauthorized_user(self):
        """
        Show that you cannot get a paper-network for an unauthorized user
        """
        r = self.anonymous_user.post('/vis/paper-network', params=self.test_params)
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
        r = user.post('/vis/paper-network', data=json.dumps(self.test_params), headers={'Content-Type': 'application/json'})

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
            self.assertEqual(
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
        """
        Tests the get end point of the paper-network for the visualisation services for a set of authorized users.
        """
        self.helper_check_paper_network(user=self.authenticated_user)
        self.helper_check_paper_network(user=self.bumblebee_user)


class TestAuthorNetwork(TestBase):
    """
    Base class for testing the paper-network end point of the visualisation services
    """
    def setUp(self):
        """
        Generic setup. Updated to include a test bibcode.
        """
        super(TestAuthorNetwork, self).setUp()
        self.test_params = dict(query=['{"q": "author:\\"Elliott, J.\\""}'])

    def test_get_request_unauthorized_user(self):
        """
        Show that you cannot get an author-network for an unauthorized user
        """
        r = self.anonymous_user.post('/vis/author-network', params=self.test_params)
        self.assertEqual(
            r.status_code,
            401,
            msg='We should get a 401 for an unauthorized user, but get: {}, {}'.format(r.status_code, r.json())
        )

    def helper_check_author_network(self, user=None):
        """
        Tests the get end point of the author-network for the visualisation services for an authorized user.
        :param user: the user to run the test on
        :type user: object
        """
        r = user.post('/vis/author-network', data=json.dumps(self.test_params), headers={'Content-Type': 'application/json'})

        self.assertEqual(
            r.status_code,
            200,
            msg='Response should be a 200 for get request of authorized user, but get: {}, {}'
                .format(r.status_code, r.json())
        )

        data = r.json()
        self.assertIsInstance(
            data,
            dict,
            msg='Response should be type dict, but is type: {}, {}'.format(type(data), data)
        )

        expected_keys = ['msg', 'data']
        actual_keys = data.keys()
        self.assertEqual(
            expected_keys.sort(),
            actual_keys.sort(),
            msg='We expect the following keys in data: {}, but have: {}'.format(expected_keys, actual_keys)
        )

        expected_attr = [u'bibcode_dict', u'root', u'link_data']
        actual_attr = data['data'].keys()
        self.assertEqual(
            expected_attr.sort(),
            actual_attr.sort(),
            msg='We expect the following attributes {} but have: {}'.format(expected_attr, actual_attr)
        )

        expected_attr = ['read_count', 'title', 'citation_count', 'authors']
        for bibcode, bibinfo in data['data']['bibcode_dict'].items():
            self.assertEqual(
                len(bibcode),
                19,
                msg='Bibcodes should have 19 characters, but it has: {} [bibcode]'.format(len(bibcode), bibcode)
            )
            self.assertIsInstance(
                bibinfo,
                dict,
                msg='Bibcode information should be type dict, but is type: {}, {}'.format(type(bibinfo), bibinfo)
            )

            actual_attr = bibinfo.keys()
            self.assertEqual(
                expected_attr.sort(),
                actual_attr.sort(),
                msg='BibInfo should have attributes {}, but has: {}'.format(expected_attr, actual_attr)
            )

        expected_attr = ['name', 'children']
        actual_attr = data['data']['root'].keys()
        self.assertEqual(
            expected_attr.sort(),
            actual_attr.sort(),
            msg='Root entry should have attributes {}, but has: {}'.format(expected_attr, actual_attr)
        )

        children = data['data']['root']['children']
        self.assertIsInstance(
            children,
            list,
            msg='Children of root should be type list, but is type: {}, {}'.format(type(children), children)
        )
        expected_attr = ['name', 'children']
        actual_attr = children[0].keys()
        self.assertEqual(
            expected_attr.sort(),
            actual_attr.sort(),
            msg='First entry should have attributes {}, but has {}'.format(expected_attr, actual_attr)
        )

        link_data = data['data']['link_data']
        self.assertIsInstance(
            link_data,
            list,
            msg='link_data should be type list, but is type: {}, {}'.format(type(link_data), link_data)
        )
        for item in link_data:
            self.assertIsInstance(
                item,
                list,
                msg='Each item of link_data should be a list, but this is type: {}, {}'.format(type(item), item)
            )
            self.assertTrue(
                all(isinstance(int(x), int) for x in item),
                msg='Each item of link_data should contain a list of numbers, but does not: {}'.format(item)
            )

    def test_get_request_authorized_user(self):
        """
        Tests the get end point of the paper-network for the visualisation services for a set of authorized users.
        """
        self.helper_check_author_network(user=self.authenticated_user)
        self.helper_check_author_network(user=self.bumblebee_user)

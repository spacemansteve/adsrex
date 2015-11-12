"""
Integration tests for the myADS services
"""

from base import TestBase


class TestMetrics(TestBase):
    """
    Base class for testing the myADS service
    """
    def setUp(self):
        """
        Generic setup. Updated to include a test bibcode.
        """
        super(TestMetrics, self).setUp()
        self.test_bibcodes = ['1994GPC.....9...69H', '1993CoPhC..74..239H']

    def test_get_request_anonymous_user(self):
        """
        Tests an anonymous user cannot access any of the end points:
          - configuration
          - user-data
          - query
        if they are an unauthorized user
        """
        for x in ['/vault/configuration',
                  '/vault/user-data',
                  '/vault/query/sfsfs-sfsdfsdf-sfsdf-sfsdf']:
            r = self.anonymous_user.get(x)
            self.assertEqual(
                401,
                r.status_code,
                msg='We expect a 401 from an unauthorized user, but get: {}, {}'.format(r.status_code, r.json())
            )
            assert r.status_code == 401

    def test_get_request_anonymous_user_query2svg(self):
        """
        A user does not need to be authorized to access the query2svg end point
        """
        r = self.anonymous_user.get('/vault/query2svg/113dc6ef2e612ffe1a0de9a16e7f494e')
        self.assertEqual(
            200,
            r.status_code,
            msg='We expect a 200 for an unauthorized user, but get: {}, {}'.format(r.status_code, r.json())
        )

    def test_get_configuration_authenticated_user(self):
        """
        Test an authenticated user can access the configuration end point, that holds the bumblebee config
        """
        r = self.authenticated_user.get('/vault/configuration')
        self.assertEqual(
            200,
            r.status_code,
            msg='We expect a 200 for an authorized user, but get: {}, {}'.format(r.status_code, r.json())
        )
        self.assertIsInstance(
            r.json(),
            dict,
            msg='Expect the response to be type dict, but is type: {}, {}'.format(type(r.json()), r.json())
        )
        self.assertIn(
            'link_servers',
            r.json(),
            msg='Expect to find "link_servers" in the response, but do not: {}'.format(r.json())
        )

    def test_get_configuration_link_servers_authenticated_user(self):
        """
        Test that an authenticated user can access a keyword via the configuration end point
        """
        r = self.authenticated_user.get('/vault/configuration/link_servers')
        self.assertEqual(
            200,
            r.status_code,
            msg='We expect a 200 for an authorized user, but get: {}, {}'.format(r.status_code, r.json())
        )
        self.assertIsInstance(
            r.json(),
            dict,
            msg='Expect the response to be type dict, but is type: {}, {}'.format(type(r.json()), r.json())
        )

    def test_user_data_work_flow_authenticated_user(self):
        """
        Test that an authenticated user can save key-values via the user-data end point, and then retrieve them
        afterwards using the user-data end point
        """
        r1 = self.authenticated_user.post('/vault/user-data', json={'link_server': 'foo'})
        self.assertEqual(
            200,
            r1.status_code,
            msg='We expect a 200 for an authorized user, but get: {}, {}'.format(r1.status_code, r1.json())
        )
        self.assertEqual(
            'foo',
            r1.json().get('link_server', 'notfoo'),
            msg='Did not find expected key "foo", contains keys: {}'.format(r1.json())
        )

        r2 = self.authenticated_user.get('/vault/user-data')
        self.assertEqual(
            200,
            r2.status_code,
            msg='We expect a 200 for an authorized user, but get: {}, {}'.format(r2.status_code, r2.json())
        )
        self.assertIsInstance(
            r2.json(),
            dict,
            msg='Expect the response to be type dict, but is type: {}, {}'.format(type(r2.json()), r2.json())
        )
        self.assertEqual(
            'foo',
            r2.json().get('link_server', 'notfoo'),
            msg='Did not find expected key "foo", contains keys: {}'.format(r2.json())
        )

    def test_post_query_authenticated_user(self):
        """
        Test that an authenticated user can save queries via the query end point, and then execute them in a vanilla
        style
        # XXX: (rchyla)
        # i'm using my own access token, once we switch to a dedicated account
        # made only for testing, the qid will change too
        """
        # POST the query to be saved
        r1 = self.authenticated_user.post('/vault/query', json={'q': '*:*'})
        self.assertEqual(
            200,
            r1.status_code,
            msg='We expect a 200 for an authorized user, but get: {}, {}'.format(r1.status_code, r1.json())
        )
        self.assertIsInstance(
            r1.json(),
            dict,
            msg='Expect the response to be type dict, but is type: {}, {}'.format(type(r1.json()), r1.json())
        )

        query_id = r1.json()['qid']

        # GET the query that was saved
        r2 = self.authenticated_user.get('/vault/query/{}'.format(query_id))
        self.assertEqual(
            200,
            r2.status_code,
            msg='We expect a 200 for an authorized user, but get: {}, {}'.format(r2.status_code, r2.json())
        )
        self.assertIn(
            'numfound',
            r2.json(),
            msg='Expected to find "numfound" in response, but did not: {}'.format(r2.json())
        )

        # GET/execute the query that was saved in a vanilla style
        r3 = self.authenticated_user.get('/vault/execute_query/{}'.format(query_id))
        self.assertEqual(
            200,
            r3.status_code,
            msg='We expect a 200 for an authorized user, but get: {}, {}'.format(r3.status_code, r3.json())
        )
        self.assertEqual(
            r3.json()['responseHeader']['params']['q'],
            '*:*',
            msg='Expected return query to be "*:*" but is {}'.format(r3.json()['responseHeader']['params']['q'])
        )
        self.assertEqual(
            r3.json()['responseHeader']['params']['fl'],
            'id',
            msg='Expected return field to be "recid" but is {}'.format(r3.json()['responseHeader']['params']['fl'])
        )
        self.assertTrue(
            r3.json()['response'],
            msg='Expected "response" keyword to be True, but is: {}'.format(r3.json()['response'])
        )

        # GET/execute the query that was saved with extra parameters
        r4 = self.authenticated_user.get('/vault/execute_query/{}?fl=recid'.format(query_id))
        self.assertEqual(
            200,
            r4.status_code,
            msg='We expect a 200 for an authorized user, but get: {}, {}'.format(r4.status_code, r4.json())
        )
        self.assertEqual(
            r4.json()['responseHeader']['params']['q'],
            '*:*',
            msg='Expected return query to be "*:*" but is {}'.format(r4.json()['responseHeader']['params']['q'])
        )
        self.assertEqual(
            r4.json()['responseHeader']['params']['fl'],
            'recid',
            msg='Expected return field to be "recid" but is {}'.format(r4.json()['responseHeader']['params']['fl'])
        )
        self.assertTrue(
            r4.json()['response'],
            msg='Expected "response" keyword to be True, but is: {}'.format(r4.json()['response'])
        )

        # GET/create svg of query that was saved
        # 113dc6ef2e612ffe1a0de9a16e7f494e
        r5 = self.authenticated_user.get('/vault/query2svg/{}'.format(query_id))
        self.assertEqual(
            200,
            r5.status_code,
            msg='We expect a 200 for an authorized user, but get: {}, {}'.format(r5.status_code, r5.json())
        )
        self.assertIn('svg', r5.text, msg='Expected "svg" in the response, but it is not: {}'.format(r5.text))
        self.assertEqual(
            r5.headers.get('Content-Type'),
            'image/svg+xml',
            msg='Expected "image/svg+xml" to be in the response header, it is not: {}'.format(r5.headers.keys())
        )

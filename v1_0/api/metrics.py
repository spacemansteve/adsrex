# encoding: utf-8
"""
Functional tests for the Graphics service
"""

from base import TestBase


class TestMetrics(TestBase):
    """
    Base class for testing the graphics service
    """
    def setUp(self):
        """
        Generic setup. Updated to include a test bibcode.
        """
        super(TestMetrics, self).setUp()
        self.test_bibcodes = ['1993CoPhC..74..239H', '1994GPC.....9...69H']

    def test_anonymous_user(self):
        """
        Test unauthenticated user cannot request all metrics for two existing
        bibcodes
        """
        r = self.anonymous_user.post(
            '/metrics',
            json={'bibcodes': self.test_bibcodes}
        )
        self.assertEqual(
            r.status_code,
            401,
            msg='We should get a 401 status but got: {}, {}'
                .format(r.status_code, r.json())
        )

    def helper_authenticated_user_posts_metrics(self, user):
        """
        Test that authenticated users can post to the metrics end point, and
        receive the expected response based on the bibcodes they sent.
        :param user: the user to run the test on
        :type user: object
        """
        # Request all metrics for two existing bibcodes
        r = user.post('/metrics', json={'bibcodes': self.test_bibcodes})

        self.assertEqual(
            r.status_code,
            200,
            msg='We should get a 200 but got: {}'.format(r.status_code)
        )

        self.assertIsInstance(
            r.json(),
            dict,
            msg='The results should be in a dictionary but it is: {}'
                .format(type(r.json()))
        )

        expected_attr = [u'basic stats', u'citation stats refereed',
                         u'histograms', u'citation stats', u'time series',
                         u'basic stats refereed', u'indicators refereed',
                         u'skipped bibcodes', u'indicators']
        actual_attr = r.json().keys()
        self.assertEqual(
            expected_attr.sort(),
            actual_attr.sort(),
            msg='Did not get expected attribtues. Expected "{}" is not same '
                'as actual "{}"'
                .format(expected_attr, actual_attr)
        )

        expected_hists = [u'downloads', u'citations', u'reads', u'publications']
        actual_hists = r.json()['histograms'].keys()
        self.assertListEqual(
            expected_hists,
            actual_hists,
            msg='Should have retrieved all histograms, but did not. '
                'Expected "{}" != actual "{}"'
                .format(expected_hists, actual_hists)
        )

        # All histograms should have the expected constituents
        histdict = {
            'downloads': [
                u'refereed downloads',
                u'all downloads normalized',
                u'all downloads',
                u'refereed downloads normalized'
            ],
            'reads': [
                u'refereed reads',
                u'all reads normalized',
                u'all reads',
                u'refereed reads normalized'
            ],
            'publications': [
                u'refereed publications',
                u'all publications',
                u'refereed publications normalized',
                u'all publications normalized'
            ],
            'citations': [
                u'refereed to nonrefereed',
                u'nonrefereed to nonrefereed',
                u'nonrefereed to nonrefereed normalized',
                u'nonrefereed to refereed',
                u'refereed to refereed normalized',
                u'refereed to nonrefereed normalized',
                u'refereed to refereed',
                u'nonrefereed to refereed normalized'
            ]
        }

        for hist in expected_hists:
            actual_hist = r.json()['histograms'][hist].keys()
            expected_hist = histdict[hist]
            self.assertItemsEqual(
                expected_hist,
                actual_hist,
                msg='All histograms should have expected consitutents. '
                    'They do not match. Expected "{}" != Actual "{}"'
                    .format(expected_hist, actual_hist)
            )
        # All histogram constituents should be dictionaries
        for hist in expected_hists:
            for hh in histdict[hist]:

                histogram = r.json()['histograms'][hist][hh]
                self.assertIsInstance(
                    histogram,
                    dict,
                    msg='All histogram consituents should be dictionaries, '
                        'but is type: {}'.format(type(histogram))
                )

        expected_stats = {
            'indicators': [
                u'g',
                u'read10',
                u'm',
                u'i10',
                u'riq',
                u'h',
                u'i100',
                u'tori'
            ],
            'indicators refereed': [
                u'g',
                u'read10',
                u'm',
                u'i10',
                u'riq',
                u'h',
                u'i100',
                u'tori'
            ],
            'basic stats': [
                u'median number of downloads',
                u'average number of reads',
                u'normalized paper count',
                u'recent number of reads',
                u'number of papers',
                u'recent number of downloads',
                u'total number of reads',
                u'median number of reads',
                u'total number of downloads',
                u'average number of downloads'
            ],
            'basic stats refereed': [
                u'median number of downloads',
                u'average number of reads',
                u'normalized paper count',
                u'recent number of reads', u'number '
                u'of papers',
                u'recent number of downloads',
                u'total number of reads',
                u'median number of reads',
                u'total number of downloads',
                u'average number of downloads'
            ],
            'citation stats': [
                u'normalized number of citations',
                u'average number of refereed citations',
                u'median number of citations',
                u'median number of refereed '
                u'citations',
                u'number of citing papers',
                u'average number of citations',
                u'total number of refereed citations',
                u'normalized number of refereed citations',
                u'number of self-citations',
                u'total number of citations'
            ],
            'citation stats refereed': [
                u'normalized number of citations',
                u'average number of refereed citations',
                u'median number of citations',
                u'median number of refereed citations',
                u'number of citing papers',
                u'average number of citations',
                u'total number of refereed citations',
                u'normalized number of refereed citations',
                u'number of self-citations',
                u'total number of citations'
            ],
            'time series': [
                u'g',
                u'h',
                u'tori',
                u'i10',
                u'read10',
                u'i100'
            ]
        }
        for entry in expected_stats:
            expected_stat = expected_stats[entry]
            actual_stat = r.json()[entry].keys()
            self.assertItemsEqual(
                expected_stat,
                actual_stat,
                msg='Did not get all indicators. '
                    'Expected "{}" != Actual "{}" for entry "{}"'
                    .format(expected_stat, actual_stat, entry)
            )

        expected_bibcodes = []
        actual_bibcodes = r.json()['skipped bibcodes']
        self.assertListEqual(
            expected_bibcodes,
            actual_bibcodes,
            msg='There should be no skipped bibcodes. '
                'Expected "{} is not actual "{}"'
                .format(expected_bibcodes, actual_bibcodes)
        )

    def test_authenticated_user(self):
        """
        Test all authenticated users can post to the metrics end point
        """
        self.helper_authenticated_user_posts_metrics(user=self.authenticated_user)
        self.helper_authenticated_user_posts_metrics(user=self.bumblebee_user)

    def test_empty_list_403(self):
        """
        Tests that posting an empty list responds with a 403.
        """
        r = self.authenticated_user.post('/metrics', json={'bibcodes': []})
        self.assertEqual(
            r.status_code,
            403,
            msg='An empty list should return 403, but returns: {}'
                .format(r.status_code)
        )

    def test_get_for_single_bibcode(self):
        """
        Tests that you can obtain metrics for a single bibcode via the GET end
        point
        """
        r = self.authenticated_user.get(
            '/metrics/{}'.format(self.test_bibcodes[0])
        )
        self.assertEqual(
            r.status_code,
            200,
            msg='We should get a 200, but get: {}, {}'
                .format(r.status_code, r.json())
        )

    def test_post_single_bibcode(self):
        """
        Tests that you can post a single bibcode to the metrics POST end point
        """
        r = self.authenticated_user.post(
            '/metrics', json={'bibcodes': self.test_bibcodes[:1]}
        )
        self.assertEqual(
            r.status_code,
            200,
            msg='We should get a 200 status, but get: {}'.format(r.status_code)
        )

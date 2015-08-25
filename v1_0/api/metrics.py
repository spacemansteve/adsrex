from ..user_roles import anonymous_user, authenticated_user, bumblebee_user
from unittest import TestCase
    
bibcodes = ['1993CoPhC..74..239H','1994GPC.....9...69H']

class MetricsServiceTest(TestCase):    
    def test_anonymous_user(self):
        # Request all metrics for two existing bibcodes
        r = anonymous_user.post('/metrics', json={'bibcodes': bibcodes})
        # We should get a 401 status
        self.assertEqual(r.status_code, 401)
        
    def test_authenticated_user(self, user=authenticated_user):
        # Request all metrics for two existing bibcodes
        r = user.post('/metrics', json={'bibcodes': bibcodes})
        # We should get a 200 status
        self.assertEqual(r.status_code, 200)
        # The results should be in a dictionary
        self.assertIsInstance(r.json(), dict)
        # Check if we get the expected attributes
        expected_attr = [u'basic stats', u'citation stats refereed',
                         u'histograms', u'citation stats', u'time series',
                         u'basic stats refereed', u'indicators refereed',
                         u'skipped bibcodes', u'indicators']
        self.assertItemsEqual(r.json().keys(), expected_attr)
        # Check if we retrieved all histograms
        expected_hists = [u'downloads', u'citations', u'reads', u'publications']
        self.assertListEqual(r.json()['histograms'].keys(), expected_hists)
        # All histograms should have the expected constituents
        histdict = {
            'downloads': [u'refereed downloads', u'all downloads normalized',
                          u'all downloads', u'refereed downloads normalized'],
            'reads': [u'refereed reads', u'all reads normalized', 
                      u'all reads', u'refereed reads normalized'],
            'publications': [u'refereed publications', u'all publications',
                             u'refereed publications normalized',
                             u'all publications normalized'],
            'citations': [u'refereed to nonrefereed', u'nonrefereed to nonrefereed',
                          u'nonrefereed to nonrefereed normalized', u'nonrefereed to refereed',
                          u'refereed to refereed normalized', u'refereed to nonrefereed normalized',
                          u'refereed to refereed', u'nonrefereed to refereed normalized']
                   }
        for hist in expected_hists:
            self.assertItemsEqual(r.json()['histograms'][hist].keys(), histdict[hist])
        # All histogram constituents should be dictionaries
        for hist in expected_hists:
            for hh in histdict[hist]:
                self.assertIsInstance(r.json()['histograms'][hist][hh], dict)
        # Did we get all expected indicators?
        expected_stats = {
            'indicators': [u'g', u'read10', u'm', u'i10', u'riq', u'h', u'i100', u'tori'],
            'indicators refereed': [u'g', u'read10', u'm', u'i10', u'riq', u'h', u'i100', u'tori'],
            'basic stats': [u'median number of downloads', u'average number of reads',
                            u'normalized paper count', u'recent number of reads', u'number of papers',
                            u'recent number of downloads', u'total number of reads',
                            u'median number of reads', u'total number of downloads',
                            u'average number of downloads'],
            'basic stats refereed': [u'median number of downloads', u'average number of reads',
                            u'normalized paper count', u'recent number of reads', u'number of papers',
                            u'recent number of downloads', u'total number of reads',
                            u'median number of reads', u'total number of downloads',
                            u'average number of downloads'],
            'citation stats': [u'normalized number of citations', u'average number of refereed citations',
                               u'median number of citations', u'median number of refereed citations',
                               u'number of citing papers', u'average number of citations',
                               u'total number of refereed citations',
                               u'normalized number of refereed citations',
                               u'number of self-citations', u'total number of citations'],
            'citation stats refereed': [u'normalized number of citations',
                               u'average number of refereed citations',
                               u'median number of citations', u'median number of refereed citations',
                               u'number of citing papers', u'average number of citations',
                               u'total number of refereed citations',
                               u'normalized number of refereed citations',
                               u'number of self-citations', u'total number of citations'],
            'time series': [u'g', u'h', u'tori', u'i10', u'read10', u'i100']        
        }
        for entry in expected_stats:
            self.assertItemsEqual(r.json()[entry].keys(), expected_stats[entry])
        # There should be no skipped bibcodes
        self.assertListEqual(r.json()['skipped bibcodes'], [])
        # Sending an empty list of bibcodes to the service should give a 403
        r = user.post('/metrics', json={'bibcodes': []})
        self.assertEqual(r.status_code, 403)
        # Test getting metrics for just one bibcode via GET
        r = user.get('/metrics/%s' % bibcodes[0])
        # We should get a 200
        self.assertEqual(r.status_code, 200)
        # And posting just one bibcode should work too
        r = user.post('/metrics', json={'bibcodes': bibcodes[:1]})
        # We should get a 200 status
        self.assertEqual(r.status_code, 200)
    
    def test_bumblebee_user(self):
        self.test_authenticated_user(user=bumblebee_user)

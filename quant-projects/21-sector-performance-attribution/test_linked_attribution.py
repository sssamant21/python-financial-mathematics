"""Synthetic regression tests for two-period linking."""
import copy
import math
import unittest
from attribution import attribute
from linked_attribution import link_two_periods

def sample():
    return (attribute(('A','B'),(.6,.4),(.5,.5),(.1,.02),(.08,.03)),
            attribute(('A','B'),(.55,.45),(.5,.5),(-.06,.04),(-.04,.02)))

class LinkingTests(unittest.TestCase):
    def test_compound_reconciliation(self):
        a,b=sample()
        r=link_two_periods(a,b)
        expected=(1+a['portfolio_return'])*(1+b['portfolio_return'])-(1+a['benchmark_return'])*(1+b['benchmark_return'])
        self.assertAlmostEqual(sum(r['linked_effects'].values()),expected)
    def test_component_scales(self):
        a,b=sample()
        r=link_two_periods(a,b)
        for k in ('allocation','selection','interaction'):
            self.assertAlmostEqual(r['linked_effects'][k],a['effects'][k]*(1+b['portfolio_return'])+b['effects'][k]*(1+a['benchmark_return']))
    def test_zero_active(self):
        a=attribute(('A',),(1,),(1,),(.04,),(.04,))
        self.assertAlmostEqual(link_two_periods(a,a)['active_total'],0)
    def test_flat_second(self):
        a,_=sample()
        z=attribute(('A',),(1,),(1,),(0,),(0,))
        self.assertAlmostEqual(link_two_periods(a,z)['active_total'],a['active_return'])
    def test_flat_first(self):
        _,b=sample()
        z=attribute(('A',),(1,),(1,),(0,),(0,))
        self.assertAlmostEqual(link_two_periods(z,b)['active_total'],b['active_return'])
    def test_total_loss(self):
        a=attribute(('A',),(1,),(1,),(-1,),(-.5,))
        b,_=sample()
        self.assertTrue(math.isfinite(link_two_periods(a,b)['active_total']))
    def test_bad_reconciliation(self):
        a,b=sample()
        a=copy.deepcopy(a)
        a['effects']['allocation']+=.01
        with self.assertRaises(ValueError): link_two_periods(a,b)
    def test_nonfinite(self):
        a,b=sample()
        a=copy.deepcopy(a)
        a['portfolio_return']=math.nan
        with self.assertRaises(ValueError): link_two_periods(a,b)
    def test_repeatable_no_mutation(self):
        a,b=sample()
        before=copy.deepcopy((a,b))
        self.assertEqual(link_two_periods(a,b),link_two_periods(a,b))
        self.assertEqual((a,b),before)

if __name__ == '__main__':
    unittest.main()

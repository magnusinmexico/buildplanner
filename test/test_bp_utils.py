import sys
import unittest
from pathlib import Path

PROJECT_DIR = Path(str(Path(__file__).parents[1])+"/buildplanner")
sys.path.append(str(PROJECT_DIR))

from bp.bp_utils import * 

class TestBPMath(unittest.TestCase):

    def test_vround(self):

        vect = [1.0003,0.0032312,1.0003213]
        s = str(vround(vect,2))
        self.assertEqual(s,"(1.0, 0.0, 1.0)")

    def test_sround(self):
        
        s = str(sround(1.2345,2))
        self.assertEqual(s,"1.2")

    def test_svround(self):

        vect = [1.0003,0.0032312,1.0003213]
        s = str(svround(vect,2))
        self.assertEqual(s,"(1.0, 0.0032, 1.0)")

    def test_list_contains_numbers(self):

        l1 = ["a","b",3,1.2]
        l2 = [1,1.2,1,5.500,2.3e-6]

        self.assertEqual(list_contains_numbers(l1),False)
        self.assertEqual(list_contains_numbers(l2),True)

if __name__ == '__main__':
    unittest.main()

import sys
import unittest
from pathlib import Path

PROJECT_DIR = Path(str(Path(__file__).parents[1])+"/buildplanner")
sys.path.append(str(PROJECT_DIR))

import bp_debug # Import to activate type check as first bp import

from bp import BPDataStockPieces

class TestBPDataStockPieces(unittest.TestCase):
    
    def test_init(self):

        bp_data_stock_pieces = BPDataStockPieces(1000)
        s1 = str(bp_data_stock_pieces)
        self.assertEqual(s1,"{1000.0: 1}")

        bp_data_stock_pieces = BPDataStockPieces(1000.0)
        s2 = str(bp_data_stock_pieces)
        self.assertEqual(s2,"{1000.0: 1}")

        bp_data_stock_pieces = BPDataStockPieces({3600:2,4200:5})
        s3 = str(bp_data_stock_pieces)
        self.assertEqual(s3,"{4200.0: 5, 3600.0: 2}")

        bp_data_stock_pieces = BPDataStockPieces([3600,4200,3600,3600,3600,4200,1200,1200,0,0])
        s4 = str(bp_data_stock_pieces)
        self.assertEqual(s4,"{4200.0: 2, 3600.0: 4, 1200.0: 2, 0.0: 2}")

        bp_data_stock_pieces = BPDataStockPieces([3600,4200,3600,3600.0,3600,4200,1200.0,1200,0.0,0])
        s5 = str(bp_data_stock_pieces)
        self.assertEqual(s5,"{4200.0: 2, 3600.0: 4, 1200.0: 2, 0.0: 2}")

        bp_data_stock_pieces = BPDataStockPieces([{4200.0: 2}, {3600.0: 4}, {1200.0: 2}, {0.0: 2}])
        s6 = str(bp_data_stock_pieces)
        self.assertEqual(s6,"{4200.0: 2, 3600.0: 4, 1200.0: 2, 0.0: 2}")

        with self.assertRaises(Exception) as e:
            bp_data_stock_pieces = BPDataStockPieces(["3600",4200,3600,3600.0,3600,4200,1200.0,1200,0.0,0])
        self.assertEqual(str(e.exception),"Parameter 'stock_pieces' must be either a dict[float,int], a list[float], an int, or a float.")

        with self.assertRaises(Exception) as e:
            bp_data_stock_pieces = BPDataStockPieces("Text")
        self.assertEqual(str(e.exception),"Parameter 'stock_pieces' must be either a dict[float,int], a list[float], an int, or a float.")

        bp_data_stock_pieces_a = BPDataStockPieces({3600:2,4200:5})
        bp_data_stock_pieces_b = BPDataStockPieces(bp_data_stock_pieces_a)
        s7 = str(bp_data_stock_pieces_a)
        s8 = str(bp_data_stock_pieces_b)
        self.assertEqual(s7,"{4200.0: 5, 3600.0: 2}")
        self.assertEqual(s8,"{4200.0: 5, 3600.0: 2}")
        self.assertIsNot(bp_data_stock_pieces_a,bp_data_stock_pieces_b)


    def test_modify(self):

        bp_data_stock_pieces_a = BPDataStockPieces([{2400.0:2},{4200.0:8}])
        bp_data_stock_pieces_a[4200.0] = 2
        s1 = str(bp_data_stock_pieces_a)
        self.assertEqual(s1,"{4200.0: 2, 2400.0: 2}")


    def test_copy(self):

        bp_data_stock_pieces_a = BPDataStockPieces([{2400.0:2},{4200.0:8}])
        bp_data_stock_pieces_b = bp_data_stock_pieces_a.copy()
        s1 = str(bp_data_stock_pieces_a)
        s2 = str(bp_data_stock_pieces_b)
        self.assertEqual(s1,"{4200.0: 8, 2400.0: 2}")
        self.assertEqual(s2,"{4200.0: 8, 2400.0: 2}")

        bp_data_stock_pieces_b[4200.0] = 2
        s3 = str(bp_data_stock_pieces_a)
        s4 = str(bp_data_stock_pieces_b)
        self.assertEqual(s3,"{4200.0: 8, 2400.0: 2}")
        self.assertEqual(s4,"{4200.0: 2, 2400.0: 2}")

        self.assertIsNot(bp_data_stock_pieces_a,bp_data_stock_pieces_b)

    def test_clean(self):
        
        bp_data_stock_pieces_a = BPDataStockPieces([{2400.0:2},{4200.0:8}])
        bp_data_stock_pieces_a.clean(4000.0)
        s1 = str(bp_data_stock_pieces_a)
        self.assertEqual(s1,"{4200.0: 8}")

        bp_data_stock_pieces_b = BPDataStockPieces([{2400.0:2},{4200.0:0}])
        bp_data_stock_pieces_b.clean()
        s2= str(bp_data_stock_pieces_b)
        self.assertEqual(s2,"{2400.0: 2}")

    def test_key_value_item(self):

        bp_data_stock_pieces = BPDataStockPieces({3600:2,4200:4,1200:10})
        s1 = str(bp_data_stock_pieces)
        self.assertEqual(s1,"{4200.0: 4, 3600.0: 2, 1200.0: 10}")

        s2 = str(bp_data_stock_pieces.keys())
        self.assertEqual(s2,"[4200.0, 3600.0, 1200.0]")

        s3 = str(bp_data_stock_pieces.values())
        self.assertEqual(s3,"[4, 2, 10]")

        s4 = str(bp_data_stock_pieces.items())
        self.assertEqual(s4,"dict_items([(4200.0, 4), (3600.0, 2), (1200.0, 10)])")

    def test_casting(self):
    
        bp_data_stock_pieces = BPDataStockPieces({3600:2,4200:4,1200:10})
        s1 = str(list(bp_data_stock_pieces))
        self.assertEqual(s1,"[4200.0, 4200.0, 4200.0, 4200.0, 3600.0, 3600.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0, 1200.0]")

        s2 = str(dict(bp_data_stock_pieces))
        self.assertEqual(s2,"{4200.0: 4, 3600.0: 2, 1200.0: 10}")

    def test_append(self):
        
        bp_data_stock_pieces = BPDataStockPieces({3600:2,4200:4})
        bp_data_stock_pieces.append(1200.0)

        s1 = str(bp_data_stock_pieces)
        self.assertEqual(s1,"{4200.0: 4, 3600.0: 2, 1200.0: 1}")

    def test_add(self):

        bp_data_stock_pieces_a = BPDataStockPieces({3600:2,4200:4})
        bp_data_stock_pieces_b = BPDataStockPieces({3600:1,4200:2,1200:2})

        bp_data_stock_pieces_c = bp_data_stock_pieces_a + bp_data_stock_pieces_b
        s1 = str(bp_data_stock_pieces_c)
        self.assertEqual(s1,"{4200.0: 6, 3600.0: 3, 1200.0: 2}")

        bp_data_stock_pieces_a += bp_data_stock_pieces_b
        s2 = str(bp_data_stock_pieces_a)
        self.assertEqual(s2,"{4200.0: 6, 3600.0: 3, 1200.0: 2}")

    def test_sub(self):

        bp_data_stock_pieces_a = BPDataStockPieces({3600:2,4200:4})
        bp_data_stock_pieces_b = BPDataStockPieces({3600:1,4200:2,1200:2})

        bp_data_stock_pieces_c = bp_data_stock_pieces_a - bp_data_stock_pieces_b
        s1 = str(bp_data_stock_pieces_c)
        self.assertEqual(s1,"{4200.0: 2, 3600.0: 1}")

        bp_data_stock_pieces_a -= bp_data_stock_pieces_b
        s2 = str(bp_data_stock_pieces_a)
        self.assertEqual(s2,"{4200.0: 2, 3600.0: 1}")

        bp_data_stock_pieces_a -= BPDataStockPieces({4200.0:10,1000.0:2})
        s3 = str(bp_data_stock_pieces_a)
        self.assertEqual(s3,"{4200.0: 0, 3600.0: 1}")

    def test_hash(self):

        bp_data_stock_pieces_a = BPDataStockPieces({3600:2,4200:4})
        bp_data_stock_pieces_b = BPDataStockPieces({3600:2,4200:4})
        bp_data_stock_pieces_c = bp_data_stock_pieces_a.copy()
        bp_data_stock_pieces_c.append(3600.0)
        i1 = hash(bp_data_stock_pieces_a)
        i2 = hash(bp_data_stock_pieces_b)
        i3 = hash(bp_data_stock_pieces_c)
        self.assertIsNot(bp_data_stock_pieces_a,bp_data_stock_pieces_b)
        self.assertEqual(i1,i2)
        self.assertNotEqual(i2,i3)
        self.assertIsInstance(i1,int)

    def test_len(self):

        bp_data_stock_pieces = BPDataStockPieces({3600:2,4200:4})
        i1 = len(bp_data_stock_pieces)
        self.assertEqual(i1,6)

    def test_min_max(self):

        bp_data_stock_pieces = BPDataStockPieces({3600:2,4200:4})
        i1 = min(bp_data_stock_pieces)
        self.assertEqual(i1,3600.0)
        i2 = max(bp_data_stock_pieces)
        self.assertEqual(i2,4200.0)

if __name__ == '__main__':
    unittest.main()


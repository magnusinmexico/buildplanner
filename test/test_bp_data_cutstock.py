import sys
import unittest
from pathlib import Path

PROJECT_DIR = Path(str(Path(__file__).parents[1])+"/buildplanner")
sys.path.append(str(PROJECT_DIR))

from bp import BPDataCutStock, BPDataStockPieces

class TestBPDataCutStock(unittest.TestCase):

    def test_init(self):

        bp_data_cut_stock = BPDataCutStock(2400.0,5.0,BPDataStockPieces([600,600,1000]))
        s1 = str(bp_data_cut_stock)
        self.assertEqual(s1,"{'stock_length': 2400.0, 'cut_width': 5.0, 'number_of_cuts': 3, 'stock_pieces': {1000.0: 1, 600.0: 2}, 'remaining_stock': 185.0, 'is_valid': True}")
    
    def test_invalid(self):
    
        bp_data_cut_stock = BPDataCutStock(1200.0,5.0,BPDataStockPieces([600,600,1000]))
        s1 = str(bp_data_cut_stock)
        self.assertEqual(s1,"{'stock_length': 1200.0, 'cut_width': 5.0, 'number_of_cuts': 2, 'stock_pieces': {1000.0: 1, 600.0: 2}, 'remaining_stock': 0.0, 'is_valid': False}")

    def test_copy(self):

        bp_data_cut_stock_a = BPDataCutStock(2400.0,5.0,BPDataStockPieces([600,600,1000]))
        bp_data_cut_stock_b = bp_data_cut_stock_a.copy()
        s1 = str(bp_data_cut_stock_b)
        self.assertIsNot(bp_data_cut_stock_a,bp_data_cut_stock_b)
        self.assertEqual(s1,"{'stock_length': 2400.0, 'cut_width': 5.0, 'number_of_cuts': 3, 'stock_pieces': {1000.0: 1, 600.0: 2}, 'remaining_stock': 185.0, 'is_valid': True}")# => False

    def test_hash(self):

        bp_data_cut_stock_a = BPDataCutStock(2400.0,5.0,BPDataStockPieces([600,600,1000]))
        bp_data_cut_stock_b = bp_data_cut_stock_a.copy()
        self.assertIsNot(bp_data_cut_stock_a,bp_data_cut_stock_b)
        i1 = hash(bp_data_cut_stock_a)
        i2 = hash(bp_data_cut_stock_b)
        self.assertEqual(i1,i2)

    def test_iter(self):

        bp_data_cut_stock = BPDataCutStock(2400.0,5.0,BPDataStockPieces([600,600,1000]))
        s1 = ""
        for key, value in bp_data_cut_stock.items():
            s1 += f"Key: {key}, Value: {value}\n"
        self.assertEqual(s1,"Key: stock_length, Value: 2400.0\nKey: cut_width, Value: 5.0\nKey: number_of_cuts, Value: 3\nKey: stock_pieces, Value: {1000.0: 1, 600.0: 2}\nKey: remaining_stock, Value: 185.0\nKey: is_valid, Value: True\n")

    def test_no_cuts(self):

        bp_data_cut_stock = BPDataCutStock(2400.0,5.0,BPDataStockPieces(2400.0))
        s1 = str(bp_data_cut_stock)
        self.assertEqual(s1,"{'stock_length': 2400.0, 'cut_width': 5.0, 'number_of_cuts': 0, 'stock_pieces': {2400.0: 1}, 'remaining_stock': 0.0, 'is_valid': True}")
        

if __name__ == '__main__':
    unittest.main()

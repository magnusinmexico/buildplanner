import sys
import unittest
import hashlib
from pathlib import Path

PROJECT_DIR = Path(str(Path(__file__).parents[1])+"/buildplanner")
sys.path.append(str(PROJECT_DIR))

import bp_debug # Import to activate type check - must be before other bp imports

from bp import BPDataCutStock, BPDataStockPieces, BPDataCutterResult

class TestBPDataCutStock(unittest.TestCase):

    def test_init(self):

        bp_data_stock_info = BPDataCutterResult(precision=4, length_unit="MILLIMETERS")
        s1 = str(bp_data_stock_info)
        self.assertEqual(hashlib.md5(s1.encode()).hexdigest(), "f96ceeda2b7cffe063248e67725636e9")

    def test_init_fail(self):

        with self.assertRaises(Exception) as e:
            bp_data_stock_info = BPDataCutterResult(precision=4, length_unit="SQM")
        self.assertEqual(str(e.exception), "SQM is an invalid length_unit value. Must be one of NONE,MILLIMETERS,CENTIMETERS,METERS,KILOMETERS,INCHES,FEET,MILES,YARDS,NANOMETERS,MICROMETERS")

    def test_cut_stock_list(self):

        bp_data_stock_info = BPDataCutterResult(precision=1, original_length_unit="MILLIMETERS", length_unit="MILLIMETERS")
        bp_data_cut_stock = BPDataCutStock(2400.0,5.0,BPDataStockPieces([600,600,1000]))
        bp_data_stock_info.append(bp_data_cut_stock)
        bp_data_stock_info.append(BPDataCutStock(2400.0,5.0,BPDataStockPieces([500,800,900]))).append(BPDataCutStock(3600.0,5.0,BPDataStockPieces([1500,800,900])))
        s1 = str(bp_data_stock_info.used_stock)
        self.assertEqual(hashlib.md5(s1.encode()).hexdigest(), "44dfb4066049646741b17ce5f9a61752")
        s2 = str(bp_data_stock_info.cut_stock_list)
        self.assertEqual(hashlib.md5(s2.encode()).hexdigest(), "f7440d822498dfed0ccf0a377c399b7b")
    
    def test_print(self):

        bp_data_stock_info = BPDataCutterResult(precision=1, original_length_unit="NONE", length_unit="KILOMETERS")

        bp_data_cut_stock = BPDataCutStock(2.400,0.005,BPDataStockPieces([0.600,0.600,1.000]))
        bp_data_stock_info.append(bp_data_cut_stock).append(bp_data_cut_stock)

        bp_data_stock_info.available_stock = BPDataStockPieces({3.6:2,2.4:8})

        with self.assertRaises(Exception) as e:
            bad_bp_data_cut_stock = BPDataCutStock(1.200,0.005,BPDataStockPieces([0.600,0.600,1.000]))
            bp_data_stock_info.append(bad_bp_data_cut_stock)
        self.assertEqual(str(e.exception),"The BPDataCutStock object is not valid:\n{'stock_length': 1.2, 'cut_width': 0.005, 'number_of_cuts': 2, 'stock_pieces': {1.0: 1, 0.6: 2}, 'remaining_stock': 0.0, 'is_valid': False}")
        
        bp_data_stock_info.append(BPDataCutStock(2.4,0.005,BPDataStockPieces([1.1975,1.1975]))).append(BPDataCutStock(3.600,0.005,BPDataStockPieces([1.500,0.800,0.900])))
        
        with self.assertRaises(Exception) as e:
            bp_data_stock_info.remaining_demand = 1.0

        self.assertEqual(str(e.exception),"On line 55 in test_print located in file: 'test_bp_data_cutterresult.py' Code: bp_data_stock_info.remaining_demand = 1.0'_BPDataCutterResult__remaining_demand' should be of type BPDataStockPieces, not float as given.")
        
        bp_data_stock_info.remaining_demand = BPDataStockPieces([4.200,4.200,4.800])

        bp_data_stock_info.append(BPDataCutStock(2.400,0.005,BPDataStockPieces([1.197,1.197])))
        bp_data_stock_info.append(BPDataCutStock(2.400,0.005,BPDataStockPieces([1.195,1.194])))

        s1 = str(bp_data_stock_info)

        self.assertEqual(hashlib.md5(s1.encode()).hexdigest(),"6fbad5d2697c3cfe3b3e155c13e5cfb9")
      

if __name__ == '__main__':
    unittest.main()
import sys
import os
import unittest
import hashlib
from pathlib import Path

PROJECT_DIR = Path(str(Path(__file__).parents[1])+"/buildplanner")
sys.path.append(str(PROJECT_DIR))

import bp_debug # Import to activate type check as first bp import

from bp import *

class TestBPCutter(unittest.TestCase):

    def test_init(self):
        stock = BPDataStockPieces({})
        demand = BPDataStockPieces({})
        bp_oc = BPCutter(stock,demand)
        self.assertEqual(str(type(bp_oc)),"<class 'bp.bp_cutter.BPCutter'>")

    def test_empty_stock(self):
        stock = BPDataStockPieces({})
        demand = BPDataStockPieces([1000,2000])
        bp_oc = BPCutter(stock,demand)
        bp_oc.cut()
        str_txt = str(bp_oc.result)
        str_svg = bp_oc.result.to_svg()
        str_html = bp_oc.result.to_html()
        self.assertIsInstance(str_txt,str)
        self.assertIsInstance(str_svg,str)
        self.assertIsInstance(str_html,str)
        self.assertEqual(str(bp_oc.result.remaining_demand),"{2000.0: 1, 1000.0: 1}")

    def test_empty_demand(self):
        stock = BPDataStockPieces([1000,3000])
        demand = BPDataStockPieces({})
        bp_oc = BPCutter(stock,demand)
        bp_oc.cut()
        str_txt = str(bp_oc.result)
        str_svg = bp_oc.result.to_svg()
        str_html = bp_oc.result.to_html()
        self.assertIsInstance(str_txt,str)
        self.assertIsInstance(str_svg,str)
        self.assertIsInstance(str_html,str)
        self.assertEqual(str(bp_oc.result.remaining_stock),"{3000.0: 1, 1000.0: 1}")

    def test_remaining(self):
        stock = BPDataStockPieces([500,1000,2000])
        demand = BPDataStockPieces([1000,2000,3000])
        bp_oc = BPCutter(stock,demand)
        bp_oc.cut()
        str_raw = str(bp_oc.result)
        str_svg = bp_oc.result.to_svg()
        str_html = bp_oc.result.to_html()
        self.assertIsInstance(str_raw,str)
        self.assertIsInstance(str_svg,str)
        self.assertIsInstance(str_html,str)
        self.assertEqual(str(bp_oc.result.remaining_demand),"{3000.0: 1}")
        self.assertEqual(str(bp_oc.result.remaining_stock),"{500.0: 1}")

    def test_text_output(self):
        stock = BPDataStockPieces({4200:10,3600:10})
        demand = BPDataStockPieces({4200:5,3600:5,1200:10,600:10})
        cut_width = 5.0
        bp_oc = BPCutter(stock,demand,cut_width,length_unit="MILLIMETERS",original_length_unit="MILLIMETERS",precision=1)
        bp_oc.cut()
        str_txt= str(bp_oc.result)
        self.assertEqual(len(str_txt),1347)
        self.assertEqual(hashlib.md5(str_txt.encode()).hexdigest(), "516d205b547a7aa51d4fbbeb9a0ccba9")
        self.assertEqual(str(bp_oc.result.method),"Greedy Cut")
        test_output_file_path = Path(str(Path(__file__).parent)+"/.test_output")
        if not os.path.exists(test_output_file_path):
            os.makedirs(test_output_file_path)
        test_output_file = Path(str(test_output_file_path)+"/text_output.txt")
        with open(test_output_file, 'w') as test_file:
            test_file.write(str_txt)

    def test_svg_output(self):
        stock = BPDataStockPieces({4200:10,3600:10})
        demand = BPDataStockPieces({4200:5,3600:5,1200:10,600:10,300:100})
        cut_width = 5.0
        bp_oc = BPCutter(stock,demand,cut_width,length_unit="METERS",original_length_unit="MILLIMETERS",precision=0)
        bp_oc.cut()
        str_svg = bp_oc.result.to_svg(svg_width=800.0)
        self.assertEqual(hashlib.md5(str_svg.encode()).hexdigest(), "f141060c55d8949bf7fe343a3e4a0026")
        self.assertEqual(str(bp_oc.result.method),"Greedy Cut")
        test_output_file_path = Path(str(Path(__file__).parent)+"/.test_output")
        if not os.path.exists(test_output_file_path):
            os.makedirs(test_output_file_path)
        test_output_file = Path(str(test_output_file_path)+"/svg_output.svg")
        with open(test_output_file, 'w') as test_file:
            test_file.write(str_svg)

    def test_html_output(self):
        stock = BPDataStockPieces({4.2:10,3.6:50,3:10})
        demand = BPDataStockPieces({4.2:5,3.6:2,1.2:10,0.4:5,0.6:10,0.21:5,0.5:25,0.1:13,0.9:10})
        cut_width = 0.005
        bp_oc = BPCutter(stock,demand,cut_width,length_unit="MILLIMETERS",original_length_unit="NONE",precision=1,method=BPCutter.METHOD.EXPERIMENTAL)
        bp_oc.cut()
        str_html = bp_oc.result.to_html()
        self.assertEqual(hashlib.md5(str_html.encode()).hexdigest(), "4b34cfb933d9e738f57b306adb5917aa")
        self.assertEqual(str(bp_oc.result.method),"Experimental")
        test_output_file_path = Path(str(Path(__file__).parent)+"/.test_output")
        if not os.path.exists(test_output_file_path):
            os.makedirs(test_output_file_path)
        test_output_file = Path(str(test_output_file_path)+"/svg_output.html")
        with open(test_output_file, 'w') as test_file:
            test_file.write(str_html)

    def test_iteration(self):
        stock = BPDataStockPieces({4200:10,3600:10})
        demand = BPDataStockPieces({4200:5,3600:2,1200:10,400:5,600:10,210:50,50:30})
        cut_width = 5.0
        s = ""
        bp_oc = BPCutter(stock,demand,cut_width,length_unit="KILOMETERS",precision=1)
        for step in bp_oc.cut_iter():
            pass
        s = str(step) # Only check last step
        self.assertEqual(hashlib.md5(s.encode()).hexdigest(), "214bba9582c9fca44cb47bdfd0f1696e",s)


if __name__ == "__main__":
    unittest.main()
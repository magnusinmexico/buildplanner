import os
import sys
import unittest
import hashlib
from pathlib import Path

PROJECT_DIR = Path(str(Path(__file__).parents[1])+"/buildplanner")
sys.path.append(str(PROJECT_DIR))

import bp_debug # Import to activate type check as first bp import

from bp.bp_svg import svg_icon, svg_logo

class TestBPLog(unittest.TestCase):

    def save_to_file(self, name : str, str_svg : str):
        test_output_file_path = Path(str(Path(__file__).parent)+"/.test_output")
        if not os.path.exists(test_output_file_path):
            os.makedirs(test_output_file_path)
        test_output_file = Path(str(test_output_file_path)+f"/{name}.svg")
        with open(test_output_file, 'w') as test_file:
            test_file.write(str_svg)


    def test_svg_icon(self):
        str_svg_icon = svg_icon(head=True, encode=False)
        self.assertEqual(hashlib.md5(str_svg_icon.encode()).hexdigest(), "66aad0b93343d9f63c01400fca383c9a")
        self.save_to_file("svg_icon",str_svg_icon)

    def test_svg_icon_black(self):
        str_svg_icon = svg_icon(head=True, encode=False, color=(0,0,0))
        self.assertEqual(hashlib.md5(str_svg_icon.encode()).hexdigest(), "be156be6adc2f5dc174827a61163bb97")
        self.save_to_file("svg_icon_black",str_svg_icon)
        
    def test_svg_icon_inline(self):
        str_svg_icon = svg_icon()
        self.assertEqual(hashlib.md5(str_svg_icon.encode()).hexdigest(), "fe1571e4f046d4712efc93d3edd2c9a2")

    def test_svg_logo(self):
        str_svg_icon = svg_logo(head=True)
        self.assertEqual(hashlib.md5(str_svg_icon.encode()).hexdigest(), "14f4be9765d6ae372eda1bfcbdabaffe")
        self.save_to_file("svg_logo",str_svg_icon)

    def test_svg_logo_black_grey(self):
        str_svg_icon = svg_logo(head=True,color=(0,0,0),color_text=(128,128,128))
        self.assertEqual(hashlib.md5(str_svg_icon.encode()).hexdigest(), "8c7790c5ff8b7d4e7485fd745ffe5f99")
        self.save_to_file("svg_logo_black_grey",str_svg_icon)
        
if __name__ == '__main__':
    unittest.main()
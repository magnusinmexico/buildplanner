import sys
import unittest
from pathlib import Path

PROJECT_DIR = Path(str(Path(__file__).parents[1])+"/buildplanner")
sys.path.append(str(PROJECT_DIR))

import bp_debug # Import to activate type check as first bp import

from bp import BPLog
from bp import type_check_class

@type_check_class
class DummyClass:

    x : int

    log : BPLog

    def __init__(self):
        self.x = 1
        self.log = BPLog()

    def get_log(self):
        log = list(self.log)
        self.log.clear()
        return  log
    
    def do_something(self):
        self.log.info("I have done something!")

class TestBPLog(unittest.TestCase):

    def test_init(self):
        BPLog.set_severity(BPLog.SEVERITY.DEBUG)
        BPLog.clear()
        log = BPLog()
        self.assertIsInstance(log,BPLog)
        s1 = str(log.dump())
        s2 = str(log)
        s3 = BPLog.to_str()
        self.assertEqual(s1,"[('TestBPLog', 4, \"BPLog activated for class 'TestBPLog'\")]")
        self.assertEqual(s2,"DEBUG : TestBPLog : BPLog activated for class 'TestBPLog'\n")
        self.assertEqual(s3,"DEBUG : TestBPLog : BPLog activated for class 'TestBPLog'\n")

    def test_another_class(self):
        BPLog.set_severity(BPLog.SEVERITY.DEBUG)
        BPLog.clear()
        log = BPLog()
        dummy = DummyClass()
        dummy.x = 0
        s1 = str(BPLog.dump())
        self.assertEqual(s1,"[('TestBPLog', 4, \"BPLog activated for class 'TestBPLog'\"), ('DummyClass', 4, \"BPLog activated for class 'DummyClass'\")]")
        log.error("Error")
        log.warning("Warning")
        log.info("Info")
        log.debug("Debug")
        s2 = str(log)
        self.assertEqual(s2, "DEBUG : TestBPLog : BPLog activated for class 'TestBPLog'\nERROR : TestBPLog : Error\nWARNING : TestBPLog : Warning\nINFO : TestBPLog : Info\nDEBUG : TestBPLog : Debug\n")
        with self.assertRaises(Exception) as e:
            dummy.log.debug("This should not work")
        self.assertEqual(str(e.exception),"TestBPLog is not allowed to call BPLog for DummyClass")
        s3 = str(dummy.get_log())
        self.assertEqual(s3,"[('DummyClass', 4, \"BPLog activated for class 'DummyClass'\")]")
        s4 = str(dummy.get_log())
        self.assertEqual(s4,"[]")
        s5 = BPLog.to_str()
        self.assertEqual(s5, "DEBUG : TestBPLog : BPLog activated for class 'TestBPLog'\nERROR : TestBPLog : Error\nWARNING : TestBPLog : Warning\nINFO : TestBPLog : Info\nDEBUG : TestBPLog : Debug\n")
        dummy.do_something()
        log.clear()
        s6 = BPLog.to_str()
        self.assertEqual(s6,"INFO : DummyClass : I have done something!\n")

if __name__ == '__main__':
    unittest.main()
import sys
import unittest
from pathlib import Path
from dataclasses import dataclass

PROJECT_DIR = Path(str(Path(__file__).parents[1])+"/buildplanner")
sys.path.append(str(PROJECT_DIR))

import bp_debug # Import to activate type check as first bp import
from bp.bp_type_check import type_check_func, type_check_class

class Dummy:

    name : str

    def __init__(self,name : str = "No Name"):
        self.name = name
        pass

    def __repr__(self):
        return f"I am the Dummy class, with name '{self.name}' doing absolutely nothing!"
    
    def do_nothing(i:int,b:bool,f:float,s:str,l:list,d:dict):
        pass


class AnotherClass:
    pass

@type_check_class
@dataclass(unsafe_hash=True)
class DataClass:
    i : int
    b : bool
    f : float
    s : str
    l : list
    d : dict
    o : Dummy
    n = 1 # no type 
    __p :str = "private"

    def __init__(self,i:int,b:bool,f:float,s:str,l:list,d:dict,o:Dummy,n):
        self.i = i
        self.b = b
        self.f = f
        self.s = s
        self.l = l
        self.d = d
        self.o = o
        self.n = n

    def fun(self,i:int,b:bool,f:float,s:str,l:list,d:dict,o:Dummy,n) -> str:
        return str(i)+str(b)+str(f)+str(l)+str(d)+str(o)+str(n)

@type_check_func
def the_fun(i:int,b:bool,f:float,s:str,l:list,d:dict,o:'Dummy',n) -> str:
    return str(i)+str(b)+str(f)+str(l)+str(d)+str(o)+str(n)

class TestbpTypeCheck(unittest.TestCase):

    def test_init(self):
        dc = DataClass(1,True,1.0,"Test",[1,2,3],{"a":1,"b":2,"c":3},Dummy(),"Whatever")
        self.assertIsInstance(dc,DataClass)
        with self.assertRaises(Exception):
            dc = DataClass(1.0,True,1.0,"Test",[1,2,3],{"a":1,"b":2,"c":3},Dummy(),"Whatever")
        s = str(dc)
        self.assertEqual(s,"DataClass(i=1, b=True, f=1.0, s='Test', l=[1, 2, 3], d={'a': 1, 'b': 2, 'c': 3}, o=I am the Dummy class, with name 'No Name' doing absolutely nothing!, _DataClass__p='private')")

    def test_set(self):
        dc = DataClass(1,True,1.0,"Test",[1,2,3],{"a":1,"b":2,"c":3},Dummy(),"Whatever")
        dc.i = 100
        dc.b = False
        dc.f = 100.0
        dc.s = "String"
        dc.l = ["a","b","c"]
        dc.d = {1:1.0,2:2.0,3:3.0}
        dc.o = Dummy("The Dummy")
        dc.n = 1
        s = str(dc)
        self.assertEqual(s,"DataClass(i=100, b=False, f=100.0, s='String', l=['a', 'b', 'c'], d={1: 1.0, 2: 2.0, 3: 3.0}, o=I am the Dummy class, with name 'The Dummy' doing absolutely nothing!, _DataClass__p='private')")
        with self.assertRaises(Exception):
            dc.i = 1.0
        with self.assertRaises(Exception):
            dc.b = "Test"
        with self.assertRaises(Exception):
            dc.f = 42
        with self.assertRaises(Exception):
            dc.s = 100
        with self.assertRaises(Exception):
            dc.l = {"a":1,"b":2,"c":3}
        with self.assertRaises(Exception):
            dc.d = [1,2,3,4,5]
        a = AnotherClass()
        self.assertIsInstance(a,AnotherClass)
        with self.assertRaises(Exception):
            dc.o = a
        with self.assertRaises(Exception):
            dc.q = "Hej"

    def test_get(self):
        dummy = Dummy()
        dc = DataClass(1,True,1.0,"Test",[1,2,3],{"a":1,"b":2,"c":3},dummy,"Whatever")
        self.assertEqual(dc.i,1)
        self.assertEqual(dc.b,True)
        self.assertEqual(dc.f,1.0)
        self.assertEqual(dc.s,"Test")
        self.assertEqual(dc.l,[1,2,3])
        self.assertEqual(dc.d,{"a":1,"b":2,"c":3})
        self.assertEqual(dc.o,dummy)
        self.assertEqual(dc.n,"Whatever")
        with self.assertRaises(Exception) as e:
            print(self.__p)
        self.assertEqual(str(e.exception),"'TestbpTypeCheck' object has no attribute '_TestbpTypeCheck__p'")

    def test_fun(self):
        dummy = Dummy()
        dc = DataClass(1,True,1.0,"Test",[1,2,3],{"a":1,"b":2,"c":3},dummy,"Whatever")
        s = dc.fun(1,True,1.0,"Test",[1,2,3],{"a":1,"b":2,"c":3},dummy,"Whatever")
        self.assertEqual(s,"1True1.0[1, 2, 3]{'a': 1, 'b': 2, 'c': 3}I am the Dummy class, with name 'No Name' doing absolutely nothing!Whatever")
        with self.assertRaises(Exception) as e:
            dc.fun(1.0,True,1.0,"Test",[1,2,3],{"a":1,"b":2,"c":3},dummy,"Whatever")
        self.assertEqual(str(e.exception),"On line 122 in test_fun located in file: 'test_bp_type_check.py' Code: dc.fun(1.0,True,1.0,\"Test\",[1,2,3],{\"a\":1,\"b\":2,\"c\":3},dummy,\"Whatever\")Argument 'i' should be of type int but was float")
        s = dc.fun(1,True,1.0,"Test",[1,2,3],{"a":1,"b":2,"c":3},dummy,100)
        self.assertEqual(s,"1True1.0[1, 2, 3]{'a': 1, 'b': 2, 'c': 3}I am the Dummy class, with name 'No Name' doing absolutely nothing!100")

    def test_type_check_fun(self):
        dummy = Dummy()
        s = the_fun(1,True,1.0,"Test",[1,2,3],{"a":1,"b":2,"c":3},dummy,"Whatever")
        self.assertEqual(s,"1True1.0[1, 2, 3]{'a': 1, 'b': 2, 'c': 3}I am the Dummy class, with name 'No Name' doing absolutely nothing!Whatever")
        with self.assertRaises(Exception) as e:
            s = the_fun(1,True,1.0,"Test",[1,2,3],{"a":1,"b":2,"c":3},1,"Whatever")
        self.assertEqual(str(e.exception),"On line 132 in test_type_check_fun located in file: 'test_bp_type_check.py' Code: s = the_fun(1,True,1.0,\"Test\",[1,2,3],{\"a\":1,\"b\":2,\"c\":3},1,\"Whatever\")Argument 'o' should be of type Dummy but was int")
        
    def test_with_parameter(self):

        @type_check_class
        class TestParam:
            __x : int
            def __init__(self):
                self.__x = 1
            @property
            def x(self):
                return self.__x
            @x.setter
            def x(self,value):
                self.__x = value
        
        testParam = TestParam()
        self.assertEqual(testParam.x,1)
        testParam.x = 2
        self.assertEqual(testParam.x,2)

    def test_with_parameter_fail(self):

        @type_check_class
        class TestParam:
            __x : int
            def __init__(self):
                self.__x = 1
            @property
            def x(self):
                return self.__x
            @x.setter
            def x(self,value):
                self.__x = value

        testParam = TestParam()

        with self.assertRaises(Exception) as e:
            testParam.x = "X"
        
        self.assertEqual(str(e.exception),"On line 171 in test_with_parameter_fail located in file: 'test_bp_type_check.py' Code: testParam.x = \"X\"'_TestParam__x' should be of type int, not str as given.")

if __name__ == '__main__':
    unittest.main()

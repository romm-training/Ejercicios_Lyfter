import unittest, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from entregable1 import addition, substraction, multiplication, division

class TestMathOperations(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(addition(1,5),6)
        self.assertEqual(addition(-1,-6),-7)
        self.assertEqual(addition(0,0),0)

    def test_substraction(self):
        self.assertEqual(substraction(30,15),15)
        self.assertEqual(substraction(-5,10),-15)
        self.assertEqual(substraction(0,1),-1)

    def test_multiplication(self):
        self.assertEqual(multiplication(5,4),20)
        self.assertEqual(multiplication(-7,-8),56)
        self.assertEqual(multiplication(0,4),0)

    def test_division(self):
        self.assertEqual(division(25,5),5)
        self.assertEqual(division(-8,-2),4)
        with self.assertRaises(ValueError):
            division(35,0)

if __name__ == "__main__":
    unittest.main()
import unittest, sys, os
from unittest import TestCase

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from business.category_biz import Category_Biz

class Test_Category_Biz(TestCase):
    
    def test_category_validations(self):
        values = {
            "category_type": "Gasto",
            "category_name": "Comida",
            "category_color": "#808040"
        }

        result = Category_Biz().category_validations(values)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()

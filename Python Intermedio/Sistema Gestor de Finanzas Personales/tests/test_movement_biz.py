import unittest, sys, os
from unittest import TestCase

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from business.movement_biz import Movement_Biz

class Test_Movement_Biz(TestCase):
    def test_is_valid_amount_integer(self):
        result = Movement_Biz().is_valid_amount(15)
        self.assertEqual(result, True)

    def test_is_valid_amount_float(self):
        result = Movement_Biz().is_valid_amount(25.85)
        self.assertEqual(result, True)

    def test_is_valid_amount_zero(self):
        result = Movement_Biz().is_valid_amount(0)
        self.assertEqual(result, True)

    def test_is_valid_amount_negative(self):
        result = Movement_Biz().is_valid_amount(-15)
        self.assertEqual(result, True)

    def test_is_valid_amount_string(self):
        result = Movement_Biz().is_valid_amount("ABC")
        self.assertEqual(result, False)

    def test_is_valid_amount_boolean(self):
            result = Movement_Biz().is_valid_amount(True)
            self.assertEqual(result, False)

    def test_movement_validations_ok(self):
        values = {
            "movement_date": "20/08/2026",
            "movement_type": "Gasto",
            "movement_category": "Comida",
            "movement_description": "Prueba 1",
            "movement_amount": 15
        }

        result = Movement_Biz().movement_validations(values)
        self.assertEqual(result, [])

    def test_movement_validations_future_date(self):
        values = {
            "movement_date": "20/08/2030",
            "movement_type": "Gasto",
            "movement_category": "Comida",
            "movement_description": "Prueba 1",
            "movement_amount": 15
        }

        result = Movement_Biz().movement_validations(values)
        self.assertEqual(result, ["La fecha del movimiento no puede ser una fecha futura."])

    def test_movement_validations_type_do_not_exist(self):
        values = {
            "movement_date": "20/08/2026",
            "movement_type": "NINGUNO",
            "movement_category": "Comida",
            "movement_description": "Prueba 1",
            "movement_amount": 15
        }

        result = Movement_Biz().movement_validations(values)
        self.assertEqual(result, ["El tipo de movimiento es inválido."])

    def test_movement_validations_category_default_value(self):
        values = {
            "movement_date": "20/08/2026",
            "movement_type": "Gasto",
            "movement_category": "--Seleccione--",
            "movement_description": "Prueba 1",
            "movement_amount": 15
        }

        result = Movement_Biz().movement_validations(values)
        self.assertEqual(result, ['Debe seleccionar una categoría.', 'Debe seleccionar una categoría válida.'])

    def test_movement_validations_category_does_not_exist(self):
        values = {
            "movement_date": "20/08/2026",
            "movement_type": "Gasto",
            "movement_category": "Ninguna",
            "movement_description": "Prueba 1",
            "movement_amount": 15
        }

        result = Movement_Biz().movement_validations(values)
        self.assertEqual(result, ["Debe seleccionar una categoría válida."])

    def test_movement_validations_no_description(self):
        values = {
            "movement_date": "20/08/2026",
            "movement_type": "Gasto",
            "movement_category": "Comida",
            "movement_description": "",
            "movement_amount": 15
        }

        result = Movement_Biz().movement_validations(values)
        self.assertEqual(result, ["Debe ingresar una descripción."])

    def test_movement_validations_amount_zero(self):
        values = {
            "movement_date": "20/08/2026",
            "movement_type": "Gasto",
            "movement_category": "Comida",
            "movement_description": "Prueba 1",
            "movement_amount": 0
        }

        result = Movement_Biz().movement_validations(values)
        self.assertEqual(result, [])

    def test_movement_validations_amount_negative(self):
        values = {
            "movement_date": "20/08/2026",
            "movement_type": "Gasto",
            "movement_category": "Comida",
            "movement_description": "Prueba 1",
            "movement_amount": -15
        }

        result = Movement_Biz().movement_validations(values)
        self.assertEqual(result, [])

    def test_movement_validations_amount_string(self):
        values = {
            "movement_date": "20/08/2026",
            "movement_type": "Gasto",
            "movement_category": "Comida",
            "movement_description": "Prueba 1",
            "movement_amount": ""
        }

        result = Movement_Biz().movement_validations(values)
        self.assertEqual(result, ["Debe ingresar un monto valido."])

if __name__ == "__main__":
    unittest.main()

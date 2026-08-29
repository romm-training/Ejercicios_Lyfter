import unittest, sys, os
from unittest import TestCase
from unittest.mock import patch, mock_open

def read_lines(path):
    with open(path, 'r') as f:
        return f.readlines()

class TestReadLines(TestCase):
    def test_read_lines_ok(self):
        # Simular contenido del archivo
        contenido = "Linea1\nLinea2\nLinea3\n"
        with patch("builtins.open", mock_open(read_data=contenido)):
            resultado = read_lines("fake_path.txt")
            self.assertEqual(resultado, ["Linea1\n","Linea2\n","Linea3\n"])

    def test_read_lines_file_not_found(self):
        # Simular que open lanza FileNotFoundError
        with patch("builtins.open",side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                read_lines("no_file_exists.txt")

if __name__ == "__main__":
    unittest.main()
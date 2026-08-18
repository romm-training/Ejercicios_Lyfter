import pytest, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from entregable2_6 import sort_string_alphabetically

def test_sort_string_alphabetically_normal():
    input_str = "unitaria-prueba-una-es-esto"

    result = sort_string_alphabetically(input_str)

    assert result == "es-esto-prueba-una-unitaria"

def test_sort_string_alphabetically_uppercase_only():
    input_str = "UNITARIA-PRUEBA-UNA-ESTO-ES"

    result = sort_string_alphabetically(input_str)

    assert result == "ES-ESTO-PRUEBA-UNA-UNITARIA"

def test_sort_string_alphabetically_including_numbers():
    input_str = "unitaria-1-prueba-es-la-numero"

    result = sort_string_alphabetically(input_str)

    assert result == "1-es-la-numero-prueba-unitaria"
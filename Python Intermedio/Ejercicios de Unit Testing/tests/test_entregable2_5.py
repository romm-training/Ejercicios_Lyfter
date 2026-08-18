import pytest, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from entregable2_5 import count_uppercase_lowercase

def test_count_uppercase_lowercase_normal(capsys):
    input_str = "Esto es una Prueba"

    count_uppercase_lowercase(input_str)

    result = capsys.readouterr()

    assert result.out == "Hay 2 mayusculas y 13 minusculas\n"

def test_count_uppercase_lowercase_lowercase_only(capsys):
    input_str = "esto es una prueba"

    count_uppercase_lowercase(input_str)

    result = capsys.readouterr()

    assert result.out == "Hay 0 mayusculas y 15 minusculas\n"

def test_count_uppercase_lowercase_uppercase_only(capsys):
    input_str = "ESTO ES UNA PRUEBA"

    count_uppercase_lowercase(input_str)

    result = capsys.readouterr()

    assert result.out == "Hay 15 mayusculas y 0 minusculas\n"
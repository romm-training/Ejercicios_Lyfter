import sys, os, pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from entregable2_4 import reverse_a_string

def test_reverse_string_normal():
    input_str = "Prueba de inversion de cadenas de caracteres"

    result = reverse_a_string(input_str)

    assert result == "seretcarac ed sanedac ed noisrevni ed abeurP"

def test_reverse_string_special_chars():
    input_str = "$^&*()![]{}"

    result = reverse_a_string(input_str)

    assert result == "}{][!)(*&^$"

def test_reverse_string_whitespaces():
    input_str = "$ ^ & * ( ) ! [ ] { } "

    result = reverse_a_string(input_str)

    assert result == " } { ] [ ! ) ( * & ^ $"
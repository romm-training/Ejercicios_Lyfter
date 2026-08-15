import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from entregable1_bubblesort import order_array, print_array
import pytest

def test_validate_short_list():
    input_list = [5,6,7,8,2,4,5,9]

    print_array(input_list)
    result = order_array(input_list)
    print_array(result)

    assert result == [2,4,5,5,6,7,8,9]

def test_validate_long_list():
    import random
    input_list = [random.randint(1, 1000) for _ in range(100)]

    print_array(input_list)
    result = order_array(input_list)
    print_array(result)

    assert result == sorted(input_list)

def test_validate_empty_list():
    input_list = []

    result = order_array(input_list)

    assert result == []

def test_other_types():
    input_list = 0

    with pytest.raises(TypeError):
        result = order_array(input_list)

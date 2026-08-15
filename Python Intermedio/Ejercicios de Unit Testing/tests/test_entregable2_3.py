import pytest, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from entregable2_3 import sum_list

def test_sum_list_normal():
    input_list = [5,6,7,8,2,4,5,9]

    result = sum_list(input_list)

    assert result == 46

def test_sum_list_including_negatives():
    input_list = [5,6,-7,8,-2,4,0,9]

    result = sum_list(input_list)

    assert result == 23

def test_sum_list_all_negatives():
    input_list = [-5,-6,-7,-8,-2,-4,-5,-9]

    result = sum_list(input_list)

    assert result == -46



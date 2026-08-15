import pytest, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from entregable2_7 import extract_prime_numbers_list

def test_extract_prime_numbers_list_normal():
    input_list = [2,4,1,3,5,6,8,13,17,18,24]

    result = extract_prime_numbers_list(input_list)

    assert result == [2,3,5,13,17]

def test_extract_prime_numbers_list_no_primes():
    input_list = [4,6,8,18,24]

    result = extract_prime_numbers_list(input_list)

    assert result == []

def test_extract_prime_numbers_list_including_0_1():
    input_list = [4,6,0,1,8,2,18,24]

    result = extract_prime_numbers_list(input_list)

    assert result == [2]
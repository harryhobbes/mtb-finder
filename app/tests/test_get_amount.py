import pytest
from finder import get_amount

def test_get_amount_int():
    assert get_amount(1) == 1.0

def test_get_amount_float():
    assert get_amount(1.0) == 1.0

def test_get_amount_string_float():
    assert get_amount('1.0') == 1.0

def test_get_amount_negative():
    assert get_amount(-1.0) == False

def test_get_amount_string_float_w_dollar():
    assert get_amount('$1000.00') == 1000.00

def test_get_amount_complex_string_float_w_dollar():
    assert get_amount('$1,000.00') == 1000.00

def test_get_amount_string():
    assert get_amount('some text') == False

def test_get_amount_zero():
    assert get_amount(0) == False
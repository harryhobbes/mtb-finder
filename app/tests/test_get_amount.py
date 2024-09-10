import pytest
from finder import get_amount

def test_get_amount_int():
    assert get_amount(1) == 1.0

def test_get_amount_float():
    assert get_amount(1.0) == 1.0

def test_get_amount_text():
    assert get_amount('some text') == False

def test_get_amount_zero():
    assert get_amount(0) == False
from decimal import Decimal

import os
import sys

# Allow importing the converter module from the project root.
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from converter import convert_rub_to_ton, convert_ton_to_rub


def test_convert_ton_to_rub():
    rate = Decimal("100")
    assert convert_ton_to_rub(Decimal("1"), rate) == Decimal("100.00")
    assert convert_ton_to_rub(Decimal("0"), rate) == Decimal("0.00")


def test_convert_rub_to_ton():
    rate = Decimal("100")
    assert convert_rub_to_ton(Decimal("100"), rate) == Decimal("1.000000")
    assert convert_rub_to_ton(Decimal("0"), rate) == Decimal("0.000000")

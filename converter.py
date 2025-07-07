"""Currency conversion helpers."""

from decimal import Decimal


RATE_CACHE: dict[str, tuple[Decimal, float]] = {}
CACHE_TTL = 30  # seconds


def convert_ton_to_rub(amount: Decimal, rate: Decimal) -> Decimal:
    """Convert TON to RUB using the provided rate."""
    return (amount * rate).quantize(Decimal("0.01"))


def convert_rub_to_ton(amount: Decimal, rate: Decimal) -> Decimal:
    """Convert RUB to TON using the provided rate."""
    if rate == 0:
        raise ValueError("Rate cannot be zero")
    return (amount / rate).quantize(Decimal("0.000001"))

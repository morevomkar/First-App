# calculator.py
"""Simple calculator library."""

from math import sqrt
from typing import Union

Number = Union[int, float]

def add(a: Number, b: Number) -> Number:
    return a + b

def sub(a: Number, b: Number) -> Number:
    return a - b

def mul(a: Number, b: Number) -> Number:
    return a * b

def div(a: Number, b: Number) -> Number:
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return a / b

def power(a: Number, b: Number) -> Number:
    return a ** b

def sqrt_num(a: Number) -> Number:
    if a < 0:
        raise ValueError("Cannot take square root of negative number.")
    return sqrt(a)

# Optional: a small dispatcher for string operations
def calculate(op: str, a: Number, b: Number = None) -> Number:
    """Calculate using operation name. For unary ops pass b=None."""
    op = op.lower()
    if op in ("+", "add", "plus"):
        assert b is not None
        return add(a, b)
    if op in ("-", "sub", "minus"):
        assert b is not None
        return sub(a, b)
    if op in ("*", "mul", "times"):
        assert b is not None
        return mul(a, b)
    if op in ("/", "div", "divide"):
        assert b is not None
        return div(a, b)
    if op in ("^", "pow", "power"):
        assert b is not None
        return power(a, b)
    if op in ("sqrt", "root"):
        return sqrt_num(a)
    raise ValueError(f"Unknown operation: {op}")

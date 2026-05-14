"""
math_tools.py
-------------
This module provides basic mathematical operations and a custom calculator class.
It serves as an example of how to use single-line and multi-line docstrings 
throughout a Python file.

Author: AI Assistant
Date: May 2026
"""

def add(a, b):
    """Return the sum of two numbers."""
    return a + b

def divide(numerator, denominator):
    """
    Perform floating-point division.

    Args:
        numerator (float): The number to be divided.
        denominator (float): The number to divide by.

    Returns:
        float: The result of the division.

    Raises:
        ZeroDivisionError: If the denominator is zero.
    """
    if denominator == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return numerator / denominator

class AdvancedCalculator:
    """
    A class used to represent an advanced mathematical calculator.

    Attributes:
        precision (int): The number of decimal places for rounding results.
    """

    def __init__(self, precision=2):
        """
        Initialize the calculator with a specific decimal precision.

        Args:
            precision (int, optional): Decimal places for results. Defaults to 2.
        """
        self.precision = precision

    def power(self, base, exponent):
        """
        Calculate the power of a number.

        Example:
            >>> calc = AdvancedCalculator()
            >>> calc.power(2, 3)
            8.0

        Args:
            base (float): The base number.
            exponent (float): The exponent value.

        Returns:
            float: The base raised to the power of the exponent, rounded.
        """
        result = base ** exponent
        return round(float(result), self.precision)

if __name__ == "__main__":
    # Accessing docstrings via the __doc__ attribute or help()
    print("Module Docstring:", __doc__)
    print("Function Docstring:", add.__doc__)
    print("Class Docstring:", AdvancedCalculator.__doc__)
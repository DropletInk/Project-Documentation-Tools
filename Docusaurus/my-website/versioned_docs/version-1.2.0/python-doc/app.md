
<a id="app1"></a>

# app1

<a id="app1.p1"></a>

# app1.p1

<a id="app1.p1.add"></a>

#### add

```python
def add(a: int, b: int) -> int
```

Add two numbers.

**Arguments**:

- `a` _int_ - First number
- `b` _int_ - Second number
  

**Returns**:

- `int` - Sum of both numbers

<a id="app1.ocr"></a>

# app1.ocr

math_tools.py
-------------
This module provides basic mathematical operations and a custom calculator class.
It serves as an example of how to use single-line and multi-line docstrings 
throughout a Python file.

Author: AI Assistant
Date: May 2026

<a id="app1.ocr.add"></a>

#### add

```python
def add(a, b)
```

Return the sum of two numbers.

<a id="app1.ocr.divide"></a>

#### divide

```python
def divide(numerator, denominator)
```

Perform floating-point division.

**Arguments**:

- `numerator` _float_ - The number to be divided.
- `denominator` _float_ - The number to divide by.
  

**Returns**:

- `float` - The result of the division.
  

**Raises**:

- `ZeroDivisionError` - If the denominator is zero.

<a id="app1.ocr.AdvancedCalculator"></a>

## AdvancedCalculator Objects

```python
class AdvancedCalculator()
```

A class used to represent an advanced mathematical calculator.

**Attributes**:

- `precision` _int_ - The number of decimal places for rounding results.

<a id="app1.ocr.AdvancedCalculator.__init__"></a>

#### \_\_init\_\_

```python
def __init__(precision=2)
```

Initialize the calculator with a specific decimal precision.

**Arguments**:

- `precision` _int, optional_ - Decimal places for results. Defaults to 2.

<a id="app1.ocr.AdvancedCalculator.power"></a>

#### power

```python
def power(base, exponent)
```

Calculate the power of a number.

**Example**:

  >>> calc = AdvancedCalculator()
  >>> calc.power(2, 3)
  8.0
  

**Arguments**:

- `base` _float_ - The base number.
- `exponent` _float_ - The exponent value.
  

**Returns**:

- `float` - The base raised to the power of the exponent, rounded.


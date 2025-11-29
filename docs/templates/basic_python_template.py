#!/usr/bin/env python3
"""
Basic Python - One-Liners Collection

A comprehensive collection of Python one-liner solutions for common programming tasks.
Each problem demonstrates Pythonic approaches and efficient problem-solving techniques.

This file contains Python one-liner problems and solutions.

Author: chronosnehal
Repository: ThinkCraft
"""

from typing import List, Dict, Any, Tuple, Optional, Set, Callable
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from functools import reduce
from itertools import chain, combinations
import random
import string
import math
import re
import operator
import json
from urllib.parse import urlparse


# ============================================================================
# ONE-LINER PROBLEM FORMAT
# ============================================================================
# Each problem follows this exact format:
#
# # Problem X: PROBLEM TITLE IN UPPERCASE
# # The function_name function description of what it does.
# def function_name(params: Type) -> ReturnType:
#     return one_liner_solution
#
# ============================================================================


# Problem 1: EXAMPLE - CONVERT LIST TO DICTIONARY
# The list_to_dict function converts a list to a dictionary where the index is the key and the list element is the value.
def list_to_dict(lst: List[Any]) -> Dict[int, Any]:
    return {i: val for i, val in enumerate(lst)}


# Problem 2: EXAMPLE - MERGE MULTIPLE DICTIONARIES
# The merge_dicts function merges multiple dictionaries into a single dictionary, with later dictionaries overwriting earlier ones.
def merge_dicts(*dicts: Dict[Any, Any]) -> Dict[Any, Any]:
    return {k: v for d in dicts for k, v in d.items()}


# Problem 3: EXAMPLE - CONVERT CAMELCASE TO SNAKE_CASE
# The camel_to_snake function converts a camelCase string to snake_case.
def camel_to_snake(s: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()


# Problem 4: EXAMPLE - ROTATE LIST BY N POSITIONS
# The rotate_list function rotates a list by n positions to the right (positive n) or left (negative n).
def rotate_list(lst: List[Any], n: int) -> List[Any]:
    return lst[-n:] + lst[:-n] if n != 0 else lst


# Problem 5: EXAMPLE - VALIDATE CREDIT CARD (LUHN ALGORITHM)
# The validate_credit_card function validates a credit card number using the Luhn algorithm.
def validate_credit_card(card_number: str) -> bool:
    digits = [int(d) for d in card_number.replace(' ', '')]
    return sum(digits[-1::-2] + [sum(divmod(d * 2, 10)) for d in digits[-2::-2]]) % 10 == 0 if len(digits) > 0 else False


# ============================================================================
# TEST CODE FORMAT
# ============================================================================
# Test code is added in the main() function following this format:
#
# # Problem X Test Code:
# # print(function_name(test_params))
# # Output: expected_output
#
# ============================================================================


def main():
    """
    Demonstration of Python one-liners.
    
    Uncomment test sections below to validate specific problems.
    """
    
    # Problem 1 Test Code:
    # print(list_to_dict(['a', 'b', 'c']))
    # Output: {0: 'a', 1: 'b', 2: 'c'}
    
    # Problem 2 Test Code:
    # print(merge_dicts({'a': 1}, {'b': 2}, {'a': 3}))
    # Output: {'a': 3, 'b': 2}
    
    # Problem 3 Test Code:
    # print(camel_to_snake('camelCaseString'))
    # Output: camel_case_string
    
    # Problem 4 Test Code:
    # print(rotate_list([1, 2, 3, 4, 5], 2))
    # Output: [4, 5, 1, 2, 3]
    
    # Problem 5 Test Code:
    # print(validate_credit_card('4532015112830366'))
    # Output: True
    
    print("\n" + "=" * 80)
    print("Uncomment test sections above to validate specific problems.")
    print("=" * 80)


if __name__ == "__main__":
    main()


# ============================================================================
# TEMPLATE GUIDELINES FOR BASIC PYTHON ONE-LINERS
# ============================================================================
#
# 1. FILE HEADER:
#    - File-level docstring with description
#    - Author and repository information
#    - Total problem count (update when adding problems)
#
# 2. IMPORTS:
#    - Import only what's needed for the one-liners
#    - Common imports: typing, collections, itertools, functools, re, math, etc.
#
# 3. PROBLEM FORMAT:
#    - Problem number: Sequential, starting from 1
#    - Title: UPPERCASE with underscores for spaces
#    - Description: One sentence describing what the function does
#    - Function: Descriptive name, type hints, one-liner return
#
# 4. ONE-LINER REQUIREMENTS:
#    - Must be a true one-liner (single return statement)
#    - Can use comprehensions, lambda, ternary operators, etc.
#    - Should be Pythonic and readable
#    - Include type hints for parameters and return type
#
# 5. TEST CODE:
#    - Add test code in main() function
#    - Comment out by default
#    - Include expected output in comment
#    - Use descriptive variable names
#
# 6. CATEGORIES:
#    - Data Structure Operations
#    - Text Processing
#    - List Advanced Operations
#    - Data Validation
#    - Mathematical Operations
#    - String Operations
#    - Date & Time Operations
#    - Array & List Operations
#    - And more...
#
# 7. NAMING CONVENTIONS:
#    - Function names: snake_case
#    - Problem titles: UPPERCASE_WITH_UNDERSCORES
#    - Variables: snake_case
#
# 8. TYPE HINTS:
#    - Always include type hints for parameters
#    - Always include return type annotation
#    - Use typing module types: List, Dict, Any, Tuple, Optional, Set, Callable
#
# ============================================================================

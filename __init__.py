"""
Vectortuple: Treat tuples like one dimensional vectors!
by Connor Ferster 03/2019
"""
from math import pi, acos, sqrt
from typing import Union

def collapse_to_tuple(d: dict, tuple_type: type) -> tuple:
    """Returns a tuple (or namedtuple type) for the values
    stored in the dict, 'd' as a 'tuple_type'."""
    if tuple_type is not tuple:
        t = tuple_type(*d.values())
    else:
        t = tuple(d.values())
    return t

def is_namedtuple(t: tuple) -> bool:
    """Function written by Alex Martelli and retrieved from 
    Stack Overflow: 
    https://stackoverflow.com/questions/2166818/
    how-to-check-if-an-object-is-an-instance-of-a-namedtuple
     
    Returns True if it appears that 't' is an instance 
    of collections.namedtuple. Returns False otherwise.
    """
    tuple_type = type(t)
    bases = tuple_type.__bases__
    if len(bases) != 1 or bases[0] != tuple: 
        return False
    fields = getattr(tuple_type, '_fields', None)
    if not isinstance(fields, tuple): 
        return False
    return all(type(n)==str for n in fields)

def valid_tuple(t: tuple) -> bool:
    """
    Returns True if tuple, 't', passes all validation checks.
    Returns False otherwise.
    """
    if not (type(t) is tuple or is_namedtuple(t)): return False
    if not all_numbers(t): return False
    return True

def same_shape(t1: tuple, t2: tuple) -> bool:
    """
    Returns True if t1 and t2 are the same shape. 
    False, otherwise."""
    if t1 and t2:
        return len(t1) == len(t2)
    return False

def all_numbers(t: tuple) -> bool:
    """
    Returns True if all the items in, 't' are numbers.
    False otherwise.
    """
    for digit in t:
        if not isinstance(digit, (int, float)): return False
    else: return True

def tuple_check(t1: tuple, t2: tuple = None) -> None:
    """
    Returns None. Raises error if any of the tuple validation tests fail.
    """
    if not valid_tuple(t1): 
        raise ValueError(f"Input object {t1} is not valid for tuple vector operations.")
    if not t2 is None and not valid_tuple(t2):
        raise ValueError(f"Input object {t2} is not valid for tuple vector operations.")
    if not t2 is None and not same_shape(t1, t2):
        raise ValueError(f"Input tuples must be same shape, not {len(t1)} and {len(t2)}.")

def dot(t1: tuple, t2: tuple) -> float:
    """
    Returns the dot product of the tuples, 't1' and 't2'.
    """
    tuple_check(t1, t2)
    dot = 0
    for idx, val in enumerate(t1):
        dot += val * t2[idx]
    return dot
    
def cross(t1: tuple, t2: tuple) -> tuple:
    """
    Returns the cross product of two 3-dimensional tuples, 't1' and 't2'.
    (Raises error if tuples are not 3-dimensional). Maintains the tuple type
    't1' (e.g. if it is a namedtuple).
    """
    tuple_check(t1, t2)
    if len(t1) == len(t2) == 3:
        i = t1[1]*t2[2] - t2[1]*t1[2]
        j = -(t1[0]*t2[2] - t2[0]*t1[2])
        k = t1[0]*t2[1] - t2[0]*t1[1]
        if type(t1) is tuple:
            return (i,j,k)
        else:
            return type(t1)(*(i,j,k))
    else:
        raise TypeError("Input tuples must be 3-dimensional. Got: {t1}, {t2}".format(t1=t1, t2=t2))
        
def add(t1: tuple, other: Union[tuple, int, float]) -> tuple:
    """
    Returns a tuple of element-wise multiplication of 't1' and 'other'
    """
    if isinstance(other, (int, float)):
        tuple_check(t1)
        acc = {idx: val+other for idx, val in enumerate(t1)}
    else: 
        tuple_check(t1, other)
        acc = {idx: val+other[idx] for idx, val in enumerate(t1)}
    return collapse_to_tuple(acc, type(t1))

def subtract(t1: tuple, other: Union[tuple, int, float]) -> tuple:
    """
    Returns a tuple of element-wise multiplication of 't1' and other
    """
    if isinstance(other, (int, float)):
        tuple_check(t1)
        acc = {idx: val-other for idx, val in enumerate(t1)}
    else: 
        tuple_check(t1, other)
        acc = {idx: val-other[idx] for idx, val in enumerate(t1)}
    return collapse_to_tuple(acc, type(t1))
        
def multiply(t1: tuple, other: Union[tuple, int, float]) -> tuple:
    """
    Returns a tuple of element-wise multiplication of 't1' and other
    """
    if isinstance(other,(int, float)):
        tuple_check(t1)
        acc = {idx: val*other for idx, val in enumerate(t1)}
    else: 
        tuple_check(t1, other)
        acc = {idx: val*other[idx] for idx, val in enumerate(t1)}
    return collapse_to_tuple(acc, type(t1))
    
def divide(t1: tuple, other: Union[tuple, int, float]) -> tuple:    
    """
    Returns a tuple of element-wise division of 't1' and 't2'
    """
    acc = {}
    if isinstance(other, (int, float)):
        tuple_check(t1)
        for idx, val in enumerate(t1):
            if val == 0 and other == 0:
                acc.update({idx: float("nan")})
            elif other == 0:
                acc.update({idx: float("inf")})
            else:
                acc.update({idx: val/other})
    else: 
        tuple_check(t1, other)
        for idx, val in enumerate(t1):
            if val == 0 and other[idx] == 0:
                acc.update({idx: float("nan")})
            elif other[idx] == 0:
                acc.update({idx: float("inf")})
            else:
                acc.update({idx: val/other[idx]})
    return collapse_to_tuple(acc, type(t1))

def vround(t: tuple, precision: int = 0) -> tuple:
    """
    Returns a tuple with elements rounded to 'precision'.
    """
    tuple_check(t)
    out_dict = {idx: round(val, precision) for idx, val in enumerate(t)}
    return collapse_to_tuple(out_dict, type(t))

def mean(t: tuple, ignore_empty: bool = False) -> float:
    """
    Returns the average of the values in the tuple, 't'. If 'ignore_empty' 
    is True, then only the values that are not either 0 or None are averaged.
    If 'ignore_empty' is False, all values are used and None is taken as 0. 
    """
    tuple_check(t)
    count = 0
    total = 0
    for val in t:
        if ignore_empty: 
            if val == 0 or val == None:
                continue
            else:
                total += val
                count += 1
        else:
            total += val
            count += 1  
    return total/count

def magnitude(t: tuple) -> float:
    """
    Returns the vector magnitude of the tuple, 't' using the 
    Pythagorean method.
    """
    tuple_check(t)
    mag_sqr = 0
    for val in t:
        mag_sqr += val**2
    return sqrt(mag_sqr)
    
def normalize(t: tuple) -> tuple:
    """
    Returns the normalized unit vector of the vector tuple, 't'.
    """
    tuple_check(t)
    return divide(t, magnitude(t))

def _clip(n: float) -> float:
    """
    Helper function to emulate numpy.clip for the specific
    use case of preventing math domain errors on the 
    acos function by "clipping" values that are > abs(1).
    e.g. _clip(1.001) == 1
         _clip(-1.5) == -1
         _clip(0.80) == 0.80
    """
    sign = n / abs(n)
    if abs(n) > 1: return 1 * sign
    else: return n
        

def angle(t1: tuple, t2: tuple, degrees: bool = False) -> float:
    """
    Returns the angle between two vector tuples, 't1' and 't2',
    in rads. If 'degrees' = True, then returned in degrees.
    """
    tuple_check(t1,t2)
    rad2deg = 1.0
    if degrees: rad2deg = 180/pi
    denom = (magnitude(t1) * magnitude(t2))
    if denom == 0: return pi/4 * rad2deg
    else: return acos(_clip(dot(t1, t2) / (magnitude(t1) * magnitude(t2)))) * rad2deg
    
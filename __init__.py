"""
Vectortuple: Treat tuples like one dimensional vectors!
by Connor Ferster 03/2019
"""
from math import pi, acos, sqrt

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

def tuple_validation(t: tuple) -> None:
    """
    Returns True if tuple, 't', passes all validation checks.
    Returns False otherwise.
    """
    all_numbers(t)
    if not (type(t) is tuple or is_namedtuple(t)):
        raise TypeError("Inputs tuples must be tuples: {}".format(t))

def same_shape(t1: tuple, t2: tuple) -> None:
    """
    Returns True if t1 and t2 are the same shape. 
    False, otherwise."""
    if not len(t1) == len(t2):
        raise ValueError("Tuples for vector math must be same size, not lengths {} and {}".format(len(t1), len(t2)))

def all_numbers(t: tuple) -> None:
    """
    Returns True if all the items in, 't' are numbers.
    False otherwise.
    """
    for digit in t:
        if not isinstance(digit, (int, float)):
            raise ValueError("Tuples for vector operations must be all numbers: {}".format(t))

def tuple_check(t1: tuple, t2: tuple) -> None:
    """Returns None. Raises error if any of the tuple validation tests fail.
    """
    tuple_validation(t1)
    tuple_validation(t2)
    same_shape(t1, t2)

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
            return type(t1)(i,j,k)
    else:
        raise TypeError("Input tuples must be 3-dimensional. Got: {t1}, {t2}".format(t1=t1, t2=t2))
        
def add(t1: tuple, other) -> tuple:
    """
    Returns a tuple of element-wise multiplication of 't1' and 'other'
    """
    tuple_validation(t1)
    if isinstance(other, (int, float)):
        out_dict = {idx: val+other for idx, val in enumerate(t1)}
    else: 
        tuple_check(t1, other)
        out_dict = {idx: val+other[idx] for idx, val in enumerate(t1)}
    return collapse_to_tuple(out_dict, type(t1))

def subtract(t1: tuple, other) -> tuple:
    """
    Returns a tuple of element-wise multiplication of 't1' and other
    """
    tuple_validation(t1)
    if isinstance(other, (int, float)):
        out_dict = {idx: val-other for idx, val in enumerate(t1)}
    else: 
        tuple_check(t1, other)
        out_dict = {idx: val-other[idx] for idx, val in enumerate(t1)}
    return collapse_to_tuple(out_dict, type(t1))
        
def multiply(t1: tuple, other) -> tuple:
    """
    Returns a tuple of element-wise multiplication of 't1' and other
    """
    tuple_validation(t1)
    if isinstance(other,(int, float)):
        out_dict = {idx: val*other for idx, val in enumerate(t1)}
    else: 
        tuple_check(t1, other)
        out_dict = {idx: val*other[idx] for idx, val in enumerate(t1)}
    return collapse_to_tuple(out_dict, type(t1))

def divide(t1: tuple, other) -> tuple:
    """
    Returns a tuple of element-wise division of 't1' and 't2'
    """
    out_dict = {}
    if isinstance(other, (int, float)):
        tuple_validation(t1)
        for idx, val in enumerate(t1):
            if val == 0 and other == 0:
                out_dict.update({idx: float("nan")})
            elif other == 0:
                out_dict.update({idx: float("inf")})
            else:
                out_dict.update({idx: val/other})
    else: 
        tuple_check(t1, other)
        for idx, val in enumerate(t1):
            if val == 0 and other[idx] == 0:
                out_dict.update({idx: float("nan")})
            elif other[idx] == 0:
                out_dict.update({idx: float("inf")})
            else:
                out_dict.update({idx: val/other[idx]})
    return collapse_to_tuple(out_dict, type(t1))

def vround(t: tuple, precision = 0) -> tuple:
    """
    Returns a tuple with elements rounded to 'precision'.
    """
    tuple_validation(t)
    out_dict = {idx: round(val, precision) for idx, val in enumerate(t)}
    return collapse_to_tuple(out_dict, type(t))

def mean(t: tuple, ignore_empty = False) -> float:
    """
    Returns the average of the values in the tuple, 't'. If 'ignore' is True,
    then only the values that are not either 0 or None are averaged.
    If 'ignore' is False, all values are used with None taken as 0. 
    """
    tuple_validation(t)
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
    Returns the magnitude of the tuple, 't', as a vector though it were
    a vector.
    """
    tuple_validation(t)
    mag_sqr = 0
    for val in t:
        mag_sqr += val**2
    return sqrt(mag_sqr)
    
def normalize(t: tuple) -> tuple:
    """
    Returns the normalized unit vector of the vector tuple, 't'.
    """
    tuple_validation(t)
    return divide(t, magnitude(t))

def _clip(n: float) -> float:
    """
    Helper function to emulate numpy.clip for the specific
    use case of preventing math domain errors on the 
    acos function. 
    """
    sign = n / abs(n)
    if abs(n) > 1: return 1 * sign
    else: return n
        

def angle(t1: tuple, t2: tuple, degrees = False) -> float:
    """
    Returns the angle between two vector tuples, 't1' and 't2',
    in rads. If 'degrees' = True, then returned in degrees.
    """
    # TODO: Fix math domain error when doing acos(1) for parallel vectors
    rad2deg = 1
    if degrees:
        rad2deg = 180/pi
    tuple_check(t1,t2)
    denom = (magnitude(t1) * magnitude(t2))
    
    if denom == 0:
        return pi/4 * rad2deg
    else:
        return acos(_clip(dot(t1, t2) / (magnitude(t1) * magnitude(t2)))) * rad2deg
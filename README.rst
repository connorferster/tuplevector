.. forallpeople documentation master file, created by
   sphinx-quickstart on Wed May 15 09:20:02 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

tuplevector: Treat tuples (and NamedTuples) as vectors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tuplevector is a simple library of pure functions that allow
for element-wise arithmetic operations on numeric tuples 
that are the same length. 

Could you have done this yourself? Yes, probably. 
But now you don't have to.


Why tuplevector? What's the advantage?
======================================

The big advantage is that you can do vector arithmetic on your own,
user-defined NamedTuple and the result will be given back to you
in your same user-defined NamedTuple! Tuplevector preserves the type
of your first input NamedTuple. 

Example:

```
from collections import namedtuple
from typing import NamedTuple
import tuplevector as vec

Vector = namedtuple("Vector", ["i", "j", "k"])
Point = NamedTuple("Point", [("x", float),
                             ("y", float),
                             ("z", float)])
                             
V1 = Vector(3, 4, 5)
P1 = Point(6, 7, 8)
T1 = (1, 2, 3)

print(vec.add(V1, P1))
>>>  Vector(i=9, j=11, k=13)

print(vec.add(P1, T1))
>>> Point(x=4, y=6, z=8)
```

Wouldn't I just use NumPy for vector math?
==========================================

Sure, you could. But:
* Do you really need to import all of NumPy to add some vectors?
* You would have to give up your elegant namedtuple data type
* Some platforms cannot run NumPy (e.g. MicroPython)




.. toctree::
   :maxdepth: 2
   :caption: Using the Library
   install
   usage


.. toctree::
 :maxdepth: 2
 :caption: Motivation and Use-cases



 usage

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

""" This is license
"""

from ctypes import *

class _LandMarks(Structure):
    _fields_ = [('x',c_int*5),('y',c_int*5)]

class _Face(Structure):
    pass
_Face._fields_ = [
    ('left',c_int),
    ('top',c_int),
    ('right',c_int),
    ('bottom',c_int),
    ('score',c_double),
    ('next',POINTER(_Face))]

class Face(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.landmarks = [(0,0)] * 5

class _Image(Structure):
    _fields_ = [('data', c_void_p),('width',c_int),('height',c_int),('channels',c_int)]
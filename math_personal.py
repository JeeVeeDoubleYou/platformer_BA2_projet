import math

"""Defines useful but non-standard simple math functions."""

def atan2_deg(x: float, y: float) -> float:
    return math.atan2(x,y)*180/math.pi

def sin_deg(x: float) -> float:
    return math.sin(x*math.pi/180)

def cos_deg(x: float) -> float:
    return math.cos(x*math.pi/180)



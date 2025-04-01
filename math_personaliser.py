import math

def atan2_deg_aprox(x: float, y: float) -> float:
    """use the symetries of arctan"""
    if x == 0 and y == 0:
        return 45   #take care of the case x=y=0
    s_x = x > 0     #x is positive
    s_y = y > 0     #y is positive
    c_xy = abs(x) > abs(y)    # x is gerater than y
    if s_y:
        if s_x:
            if c_xy:
                return 90-tan_deg_aprox(y/x)
            return tan_deg_aprox(x/y)
        if c_xy:
            return -90+tan_deg_aprox(-y/x)
        return -tan_deg_aprox(-x/y)
    if s_x:
        if c_xy:
            return 90+tan_deg_aprox(-y/x)
        return 180-tan_deg_aprox(-x/y)
    if c_xy:
        return -90-tan_deg_aprox(y/x)
    return -180+tan_deg_aprox(x/y)
    
def tan_deg_aprox(x: float):
    return (-15.5450048923999*x+60.7150688287897)*x


def atan2_deg(x,y):
    return math.atan2(x,y)*180/math.pi

def sin_deg(x):
    return math.sin(x*math.pi/180)

def cos_deg(x):
    return math.cos(x*math.pi/180)



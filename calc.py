def mapping(x, i_min, i_max, o_min, o_max) -> float:
    """Maps a value from a given range into another range"""

    return (x - i_min) * (o_max - o_min) / (i_max - i_min) + o_min


def line(xo: float, yo: float, x: float, y: float) -> tuple:
    """Calculates the equation of the line from two given points.
    Equation: A.x + B.y = C"""

    a = yo - y
    b = x - xo
    c = yo * x - y * xo

    return (a, b, c)


def intersection(abc1: tuple, abc2: tuple) -> tuple:
    """Calculates the intersection of two lines, if any, otherwise,
    returns False. (Cramer's rule)"""

    d = abc1[0] * abc2[1] - abc1[1] * abc2[0]

    if d == 0:
        return False

    dx = abc1[2] * abc2[1] - abc1[1] * abc2[2]
    dy = abc1[0] * abc2[2] - abc1[2] * abc2[0]

    return (dx / d, dy / d)

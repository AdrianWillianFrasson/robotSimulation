def lineCalc(xo: float, yo: float, x: float, y: float) -> tuple:
    # Line equation: A.x + B.y = C
    a = yo - y
    b = x - xo
    c = yo * x - y * xo
    return (a, b, c)


def intersection(abc1: tuple, abc2: tuple) -> tuple:
    do = abc1[0] * abc2[1] - abc1[1] * abc2[0]

    if do == 0:
        return False

    dx = abc1[2] * abc2[1] - abc1[1] * abc2[2]
    dy = abc1[0] * abc2[2] - abc1[2] * abc2[0]

    return (dx / do, dy / do)

from geometry import lineCalc


class Obstacle(object):
    def __init__(self, xo: float, yo: float, x: float, y: float):
        self.xo = xo
        self.yo = yo
        self.x = x
        self.y = y

        # Line equation: A.x + B.y = C
        self.abc = lineCalc(xo, yo, x, y)

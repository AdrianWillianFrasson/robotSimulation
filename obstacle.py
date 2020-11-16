from calc import line


class Obstacle(object):
    """Represents an obstacle on the screen, it's a line segment"""

    def __init__(self, xo: float, yo: float, x: float, y: float):
        self.xo = xo  # initial x coordinate
        self.yo = yo  # initial y coordinate
        self.x = x    # final x coordinate
        self.y = y    # final y coordinate

        # Calculates the representative line of this segment
        self.abc = line(xo, yo, x, y)

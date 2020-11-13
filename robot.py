from turtle import Turtle, Screen
from math import atan2, sin, cos, pi


class Robot(object):
    def __init__(self, obstcl: list, x: float, y: float):
        self.turtle = Turtle()
        self.obstcl = obstcl
        self.angles = [-90.0, -60.0, 0.0, 60.0, 90.0]
        self.tag = f"sen{hash(self)}"

        self.screen = Screen()
        self.canvas = self.screen.getcanvas()

        # Config
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.goto((x, y))

    def run(self):
        self.updateSensors()
        # print(results)

        self.turtle.right(1.0)
        self.turtle.forward(2.0)

    def follow(self, x: float, y: float):
        print(x, y)

    def updateSensors(self):
        self.canvas.delete(self.tag)
        xo, yo = self.turtle.pos()

        for angle in self.angles:
            a = angle + self.turtle.heading()
            xf = cos(a * pi / 180.0) + xo
            yf = sin(a * pi / 180.0) + yo

            def generate():
                for lo in self.obstcl:
                    intersec = self.intersection((xo, yo, xf, yf), lo)

                    if intersec is False:
                        continue

                    xi, yi = intersec

                    if lo[0] == lo[2]:
                        if not (min(lo[1], lo[3]) <= yi <= max(lo[1], lo[3])):
                            continue
                    else:
                        if not (min(lo[0], lo[2]) <= xi <= max(lo[0], lo[2])):
                            continue

                    h = round(atan2(yi - yo, xi - xo) * 180.0 / pi)
                    if h == a or h + 360.0 == a:
                        yield (xi, yi)

            g = [(xi, yi) for xi, yi in generate()]
            p = [(p[0]**2 + p[1]**2)**(1/2) for p in g]

            if p:
                xi, yi = g[p.index(min(p))]

                self.canvas.create_line(
                    xo, -yo, xi, -yi, fill="red", tags=self.tag)

    def intersection(self, l1: tuple, l2: tuple) -> tuple:
        def line(xo, yo, x, y):
            # Line equation: a.x + b.y = c
            a = yo - y
            b = x - xo
            c = yo * x - y * xo
            return (a, b, c)

        a1, b1, c1 = line(l1[0], l1[1], l1[2], l1[3])
        a2, b2, c2 = line(l2[0], l2[1], l2[2], l2[3])

        do = a1 * b2 - b1 * a2

        if do == 0:
            return False

        dx = c1 * b2 - b1 * c2
        dy = a1 * c2 - c1 * a2

        return (dx / do, dy / do)

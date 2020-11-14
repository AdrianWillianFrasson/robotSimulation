from turtle import Turtle, Screen
from math import atan2, sqrt, sin, cos, pi

from geometry import lineCalc, intersection


class Robot(object):
    def __init__(self, robots: list, obstcl: list, x: float, y: float):
        self.turtle = Turtle()
        self.obstcl = obstcl
        self.robots = robots
        self.sensor = [-90.0, -60.0, 0.0, 60.0, 90.0]
        self.result = list()
        self.tag = f"s{hash(self)}"

        self.screen = Screen()
        self.canvas = self.screen.getcanvas()

        # Config
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.goto((x, y))

    def run(self):
        self.result = self.updateSensors()

        self.turtle.left(2.0)
        self.turtle.forward(1.0)
        self.detectCollision()

    def follow(self, x: float, y: float):
        print(x, y)

    def detectCollision(self):
        xo, yo = self.turtle.pos()

        for ob in self.obstcl:
            a, b, c = ob.abc

            if 5.0 > abs(a*xo + b*yo - c) / sqrt(a*a + b*b):
                x = (b*(b*xo - a*yo) + a*c) / (a*a + b*b)
                # y = (a*(-b*xo + a*yo) + b*c) / (a*a + b*b)

                if min(ob.xo, ob.x) <= x <= max(ob.xo, ob.x):
                    try:
                        self.robots.remove(self)
                        self.canvas.delete(self.tag)
                    except ValueError:
                        pass

    def updateSensors(self) -> list:
        self.canvas.delete(self.tag)
        xo, yo = self.turtle.pos()
        results = list()

        for angle in self.sensor:
            a = angle + self.turtle.heading()
            xf = cos(a * pi / 180.0) + xo
            yf = sin(a * pi / 180.0) + yo

            def generate():
                for ob in self.obstcl:
                    itsec = intersection(lineCalc(xo, yo, xf, yf), ob.abc)

                    if itsec is False:
                        continue

                    xi, yi = itsec

                    if ob.xo == ob.x:
                        if not (min(ob.yo, ob.y) <= yi <= max(ob.yo, ob.y)):
                            continue
                    else:
                        if not (min(ob.xo, ob.x) <= xi <= max(ob.xo, ob.x)):
                            continue

                    h = round(atan2(yi - yo, xi - xo) * 180.0 / pi)
                    if h == a or h + 360.0 == a:
                        yield (xi, yi)

            g = [(xi, yi) for xi, yi in generate()]
            p = [sqrt((p[0]-xo)*(p[0]-xo) + (p[1]-yo)*(p[1]-yo)) for p in g]

            if p:
                xi, yi = g[p.index(min(p))]
                results.append(min(p))

                self.canvas.create_line(
                    xo, -yo, xi, -yi, fill="red", tags=self.tag)

        return results

from turtle import Turtle, Screen
from math import atan2, sqrt, sin, cos, pi

from calc import intersection, line


class Robot(object):
    def __init__(self, robots: list, obstcl: list, x: float, y: float):
        self.turtle = Turtle()  # Turtle object
        self.obstcl = obstcl    # Obstacles list reference
        self.robots = robots    # Robots list reference
        self.result = list()    # Sensors list results
        self.target = list()    # targets list

        # Sensors angles list
        self.sensor = [-90.0, -45.0, 0.0, 45.0, 90.0]

        # Gets the singleton screen/canvas object
        self.screen = Screen()
        self.canvas = self.screen.getcanvas()

        # Turtle settings
        self.turtle.penup()       # Stops drawing
        self.turtle.speed(0)      # Maximum speed
        self.turtle.goto((x, y))  # Goes to the defined position

        # Auxiliary
        self.__tag = f"r{hash(self)}"  # Robot unique ID
        self.__nTgt = 0                # Targets numbers

    def run(self):
        """Runs the robot routine"""

        self.result = self.updateSensors()
        self.detectTarget()

        self.turtle.forward(2.0)
        self.detectCollision()

    def follow(self, x: float, y: float):
        """Creates new targets for the robots to follow"""

        # Target unique ID
        tag = f"{self.__tag}{self.__nTgt}"

        # Creates a circle at the position (x, y), representing a target
        self.canvas.create_oval(x-5, -(y-5), x+5, -(y+5), fill="blue", tag=tag)

        self.target.append((x, y, tag))
        self.__nTgt += 1

    def detectTarget(self):
        """Detects if the robot reached a target"""

        # If there are targets
        if self.target:
            xo, yo = self.turtle.pos()    # Robot (x, y) Position
            xt, yt, tag = self.target[0]  # Target (x, y) position

            # Sets the direction of the robot to the target's direction
            self.turtle.setheading(round(self.turtle.towards(xt, yt)))

            # If the distance between the robot and the target is
            # less than 2 (something) the robot has reached the target
            if 2.0 > sqrt((xt-xo)*(xt-xo) + (yt-yo)*(yt-yo)):
                self.target.pop(0)       # Delets the target
                self.canvas.delete(tag)  # clears the canvas

    def detectCollision(self):
        """Detects if the robot has hit an obstacle"""

        # Robot (x, y) Position
        xo, yo = self.turtle.pos()

        # Checks for eache obstacle
        for ob in self.obstcl:
            a, b, c = ob.abc  # Obstacle line (A.x + B.y = C)

            # Calcs the distance between a point (robot)
            # and the line (obstacle)
            if 5.0 > abs(a*xo + b*yo - c) / sqrt(a*a + b*b):

                # The point on the obstacle which is closest to the robot
                x = (b*(b*xo - a*yo) + a*c) / (a*a + b*b)
                # y = (a*(-b*xo + a*yo) + b*c) / (a*a + b*b)

                # If the "x" coordinate is in the segment range of the obstacle
                if min(ob.xo, ob.x) <= x <= max(ob.xo, ob.x):
                    try:
                        self.robots.remove(self)        # Delets the robot
                        self.canvas.delete(self.__tag)  # Clears the canvas
                    except ValueError:
                        pass

    def updateSensors(self) -> list:
        """Updates the sensors lines and returns the distances
        between the sensors and the first obstacle"""

        self.canvas.delete(self.__tag)  # Delets old lines
        xo, yo = self.turtle.pos()      # Robot (x, y) Position
        distances = list()              # Distances list

        # Each angle represents a sensor
        for angle in self.sensor:
            # Absolute angle of the sensor
            abs_angle = angle + self.turtle.heading()

            # Calcs another point for the sensor line, the
            # first one is the position of the robot (xo, yo)
            xf = cos(abs_angle * pi / 180.0) + xo
            yf = sin(abs_angle * pi / 180.0) + yo

            # Gets intersections
            intersecs = self.findIntersections(xo, yo, xf, yf, abs_angle)

            # If there are any
            if intersecs:
                # Gets the closest to the sensor
                d, xi, yi = min(intersecs)
                distances.append(d)

                # Creates a line from the robot to the
                # intersection, representing the sensor
                self.canvas.create_line(
                    xo, -yo, xi, -yi, fill="red", tag=self.__tag)

        return distances

    def findIntersections(self, xo, yo, xf, yf, abs_angle) -> list:
        """Returns possibles intersections between
        the sensor and an obstacle"""

        intersecs = list()  # Intersections list

        # For each obstacle
        for ob in self.obstcl:
            # Gets the intersection coordinate (xi, yi)
            itsec = intersection(line(xo, yo, xf, yf), ob.abc)

            # If have none, ignore this obstacle and go to the next
            if itsec is False:
                continue

            xi, yi = itsec

            # Checks if the intersection coordinates
            # are in the segment range of the obstacle
            if ob.xo == ob.x:
                if not (min(ob.yo, ob.y) <= yi <= max(ob.yo, ob.y)):
                    continue
            else:
                if not (min(ob.xo, ob.x) <= xi <= max(ob.xo, ob.x)):
                    continue

            # Checks if the intersection coordinates
            # are in the same direction of the sensor
            h = round(atan2(yi - yo, xi - xo) * 180.0 / pi)
            if abs_angle in (h, h + 360.0):
                # Append the distance between the robot and the obstacle
                # and the intersection coordinates
                intersecs.append(
                    (sqrt((xi-xo)*(xi-xo) + (yi-yo)*(yi-yo)), xi, yi))

        return intersecs

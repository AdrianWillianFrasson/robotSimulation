from turtle import Screen

from robot import Robot
from obstacle import Obstacle


class RobotSimulation(object):
    def __init__(self):
        self.obstcl = list()
        self.robots = list()
        self.screen = None
        self.canvas = None
        self.frTime = 1

        # Auxiliary
        self.__obsPtn = tuple()  # Obstacle first point
        self.__obsFlg = False    # Auxiliary flag

    def play(self):
        self.screen = Screen()
        self.canvas = self.screen.getcanvas()

        # Screen config
        self.screen.title("Robot Simulation")
        self.screen.setup(width=1080, height=720)

        # Screen Margins
        self.createObstacle(-500.0, -320.0)
        self.createObstacle(-500.0, 200.0)
        self.createObstacle(-500.0, 200.0)
        self.createObstacle(500.0, 200.0)
        self.createObstacle(500.0, 200.0)
        self.createObstacle(500.0, -320.0)
        self.createObstacle(500.0, -320.0)
        self.createObstacle(-500.0, -320.0)

        self.createObstacle(-500.0, 230.0)
        self.createObstacle(-500.0, 320.0)
        self.createObstacle(-500.0, 320.0)
        self.createObstacle(500.0, 320.0)
        self.createObstacle(500.0, 320.0)
        self.createObstacle(500.0, 230.0)
        self.createObstacle(500.0, 230.0)
        self.createObstacle(-500.0, 230.0)

        self.canvas.create_text(-470, -305, text="sensor 1:")
        self.canvas.create_text(-470, -290, text="sensor 2:")
        self.canvas.create_text(-470, -275, text="sensor 3:")
        self.canvas.create_text(-470, -260, text="sensor 4:")
        self.canvas.create_text(-470, -245, text="sensor 5:")

        # Bindings
        self.screen.onclick(self.follow, 1)          # L button
        self.screen.onclick(self.createRobot, 2)     # M button
        self.screen.onclick(self.createObstacle, 3)  # R button

        # Start update loop
        self.screen.ontimer(self.updateScreen, self.frTime)
        self.screen.mainloop()

    def createObstacle(self, x: float, y: float):
        if self.__obsFlg:
            xo = self.__obsPtn[0]
            yo = self.__obsPtn[1]
            self.canvas.create_line(xo, -yo, x, -y, tags="obs")
            self.obstcl.append(Obstacle(xo, yo, x, y))
            self.__obsFlg = False

        else:
            self.__obsPtn = (x, y)
            self.__obsFlg = True

    def createRobot(self, x: float, y: float):
        self.robots.append(Robot(self.robots, self.obstcl, x, y))

    def follow(self, x: float, y: float):
        for robot in self.robots:
            robot.follow(x, y)

    def updateScreen(self):
        for robot in self.robots:
            robot.run()

        if self.robots:
            self.updateDisplay(self.robots[0].result)

        self.screen.ontimer(self.updateScreen, self.frTime)

    def updateDisplay(self, results: list):
        self.canvas.delete("dsp")

        rs = [self.map2(x, 0, 1127, -440, 550) for x in results]

        self.canvas.create_line(-440, -305, rs[0], -305, fill="red", tag="dsp")
        self.canvas.create_line(-440, -290, rs[1], -290, fill="red", tag="dsp")
        self.canvas.create_line(-440, -275, rs[2], -275, fill="red", tag="dsp")
        self.canvas.create_line(-440, -260, rs[3], -260, fill="red", tag="dsp")
        self.canvas.create_line(-440, -245, rs[4], -245, fill="red", tag="dsp")

    def map2(self, x, i_min, i_max, o_min, o_max):
        return (x - i_min) * (o_max - o_min) / (i_max - i_min) + o_min

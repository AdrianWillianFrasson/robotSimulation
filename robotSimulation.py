from turtle import Screen
from robot import Robot


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
        self.createObstacle(-500.0, 320.0)
        self.createObstacle(500.0, 320.0)
        self.createObstacle(500.0, -320.0)
        self.createObstacle(-500.0, 320.0)
        self.createObstacle(500.0, 320.0)
        self.createObstacle(500.0, -320.0)
        self.createObstacle(-500.0, -320.0)

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
            self.obstcl.append((xo, yo, x, y))
            self.__obsFlg = False

        else:
            self.__obsPtn = (x, y)
            self.__obsFlg = True

    def createRobot(self, x: float, y: float):
        self.robots.append(Robot(self.obstcl, x, y))

    def follow(self, x: float, y: float):
        for robot in self.robots:
            robot.follow(x, y)

    def updateScreen(self):
        for robot in self.robots:
            robot.run()

        self.screen.ontimer(self.updateScreen, self.frTime)

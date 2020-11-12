from turtle import Screen
from robot import Robot


class RobotSimulation(object):
    def __init__(self, width: int, height: int):
        self.obstcl = list()
        self.robots = dict()
        self.screen = None
        self.canvas = None
        self.frTime = 50

        # Window (width x height)
        self.width = width
        self.height = height

        # Auxiliary
        self.__obsPtn = tuple()  # Obstacle first point
        self.__obsFlg = False    # Auxiliary flag

    def play(self):
        self.screen = Screen()
        self.canvas = self.screen.getcanvas()

        # Screen config
        self.screen.title("Robot Simulation")
        self.screen.setup(width=self.width, height=self.height)

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
            self.canvas.create_line(self.__obsPtn[0], -self.__obsPtn[1], x, -y)
            self.obstcl.append((self.__obsPtn[0], self.__obsPtn[1], x, y))
            self.__obsFlg = False

        else:
            self.__obsPtn = (x, y)
            self.__obsFlg = True

    def createRobot(self, x: float, y: float):
        robot = Robot(self.obstcl, x, y)
        self.robots[hash(robot)] = robot

    def follow(self, x: float, y: float):
        print(x, y)
        for robot in self.robots.values():
            robot.follow(x, y)

    def updateScreen(self):
        for robot in self.robots.values():
            robot.run()

        self.screen.ontimer(self.updateScreen, self.frTime)

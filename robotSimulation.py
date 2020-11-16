from turtle import Screen

from obstacle import Obstacle
from robot import Robot
from calc import mapping


class RobotSimulation(object):
    """Responsible for update the screen
    and create new robots and obstacles"""

    def __init__(self):
        self.obstcl = list()  # Obstacles list
        self.robots = list()  # Robots list
        self.screen = None    # Screen object
        self.canvas = None    # Canvas object

        # Auxiliary
        self.__oldPtn = tuple()  # Obstacle first point
        self.__clickF = False    # Auxiliary click flag

    def play(self):
        """Runs the simulator"""

        # Gets the singleton screen/canvas object
        self.screen = Screen()
        self.canvas = self.screen.getcanvas()

        # Screen settings
        self.screen.title("Robot Simulation")
        self.screen.setup(width=1080, height=720)

        # Screen margins
        self.createObstacle(-500.0, -320.0)
        self.createObstacle(-500.0, 200.0)
        self.createObstacle(-500.0, 200.0)
        self.createObstacle(500.0, 200.0)
        self.createObstacle(500.0, 200.0)
        self.createObstacle(500.0, -320.0)
        self.createObstacle(500.0, -320.0)
        self.createObstacle(-500.0, -320.0)

        # Display margins
        self.createObstacle(-500.0, 230.0)
        self.createObstacle(-500.0, 320.0)
        self.createObstacle(-500.0, 320.0)
        self.createObstacle(500.0, 320.0)
        self.createObstacle(500.0, 320.0)
        self.createObstacle(500.0, 230.0)
        self.createObstacle(500.0, 230.0)
        self.createObstacle(-500.0, 230.0)

        # Display texts
        self.canvas.create_text(-470, -305, text="sensor 1:")
        self.canvas.create_text(-470, -290, text="sensor 2:")
        self.canvas.create_text(-470, -275, text="sensor 3:")
        self.canvas.create_text(-470, -260, text="sensor 4:")
        self.canvas.create_text(-470, -245, text="sensor 5:")

        # Mouse connects
        self.screen.onclick(self.follow, 1)          # L button
        self.screen.onclick(self.createRobot, 2)     # M button
        self.screen.onclick(self.createObstacle, 3)  # R button

        # Starts the update loop
        while True:
            self.updateRobots()
            self.updateDisplay()
            self.screen.update()

    def follow(self, x: float, y: float):
        """Does all robots on the screen
        follow the coordinate (x, y)"""

        for robot in self.robots:
            robot.follow(x, y)

    def createRobot(self, x: float, y: float):
        """Creates a robot at the coordinate (x, y)"""

        self.robots.append(Robot(self.robots, self.obstcl, x, y))

    def createObstacle(self, x: float, y: float):
        """Creates an obstacle on the screen. The first click, defines
        the starting point and the second click, the end point"""

        # Second click
        if self.__clickF:
            xo, yo = self.__oldPtn
            self.canvas.create_line(xo, -yo, x, -y)
            self.obstcl.append(Obstacle(xo, yo, x, y))
            self.__clickF = False

        # First click
        else:
            self.__oldPtn = (x, y)
            self.__clickF = True

    def updateRobots(self):
        """Run the routine of the robots"""

        for robot in self.robots:
            robot.run()

    def updateDisplay(self):
        """Updates the values of the display"""

        # Deletes old values
        self.canvas.delete("val")

        # If there are robots and it has results, shows
        # the results of the first robot on the display
        if self.robots and self.robots[0].result:
            rs = [mapping(x, 0, 1127, -440, 550)
                  for x in self.robots[0].result]

            self.canvas.create_line(
                -440, -305, rs[0], -305, fill="red", tag="val")
            self.canvas.create_line(
                -440, -290, rs[1], -290, fill="red", tag="val")
            self.canvas.create_line(
                -440, -275, rs[2], -275, fill="red", tag="val")
            self.canvas.create_line(
                -440, -260, rs[3], -260, fill="red", tag="val")
            self.canvas.create_line(
                -440, -245, rs[4], -245, fill="red", tag="val")

import turtle


class RobotSimulation(object):
    def __init__(self, width: int, height: int):
        self.turtles = dict()
        self.screen = None
        self.canvas = None

        # Window (width x height)
        self.width = width
        self.height = height

    def play(self):
        self.screen = turtle.Screen()
        self.canvas = self.screen.getcanvas()

        # Screen config
        self.screen.title("Robot Simulation")
        self.screen.setup(width=self.width, height=self.height)

        # Bindings
        self.screen.onclick(self.follow, 1)          # L button
        self.screen.onclick(self.createRobot, 2)     # M button
        self.screen.onclick(self.createObstacle, 3)  # R button

        # Play MainLoop
        turtle.mainloop()

    def createRobot(self, x, y):
        print("robot")

    def createObstacle(self, x, y):
        print("obstacle")

    def follow(self, x, y):
        print("follow")

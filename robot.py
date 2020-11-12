from turtle import Turtle, Screen


class Robot(object):
    def __init__(self, obstcl: list, x: float, y: float):
        self.turtle = Turtle()  # Tutle
        self.obstcl = obstcl
        self.x_axis = x         # x-axis
        self.y_axis = y         # y-axis

        self.screen = Screen()
        self.canvas = self.screen.getcanvas()

        # Config
        # self.t.penup()
        self.turtle.speed(0)
        self.turtle.goto((self.x_axis, self.y_axis))

    def run(self):
        self.turtle.forward(10.0)
        print(self.obstcl)

    def follow(self, x: float, y: float):
        print("Following", x, y)

import math

class Shape:
    def area(self):
        pass   


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2


def print_area(shape_object):
    print("Area =", shape_object.area())


# Testing
c = Circle(5)
s = Square(4)

print_area(c)
print_area(s)

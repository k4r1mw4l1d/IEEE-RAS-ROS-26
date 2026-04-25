<<<<<<< HEAD
class Rectangle:
    def __init__(self, w, h):
        self.width = w
        self.height = h

    def get_area(self):
        return self.width * self.height
    
area = Rectangle(10, 5)
=======
class Rectangle:
    def __init__(self, w, h):
        self.width = w
        self.height = h

    def get_area(self):
        return self.width * self.height
    
area = Rectangle(10, 5)
>>>>>>> b424a5e40c93cbecb347dcdcda05a113238ded1d
print(f"Area is {area.get_area()}")
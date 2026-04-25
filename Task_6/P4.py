class Rectangle:
    def __init__(self, w, h):
        self.width = w
        self.height = h

    def get_area(self):
        return self.width * self.height
    
area = Rectangle(10, 5)
print(f"Area is {area.get_area()}")
class Dog:
    def __init__(self, name, bread):
        self.name = name
        self.bread = bread
    
    def bark(self):
        print(f"Woof! My name is {self.name}")


dog = Dog("Shamshoon", "Husky")
dog.bark()
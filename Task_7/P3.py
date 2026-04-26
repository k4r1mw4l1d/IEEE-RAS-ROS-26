class Passenger:
    def __init__(self, name):
        self.name = name


class Flight:
    def __init__(self):
        self.passengers = []

    def add_passenger(self, passengerobj):
        self.passengers.append(passengerobj)


p1 = Passenger("Karim")
p2 = Passenger("Mahmoud")
p3 = Passenger("Khairy")

flight = Flight()
flight.add_passenger(p1)
flight.add_passenger(p2)
flight.add_passenger(p3)

for p in flight.passengers:
    print(p.name)

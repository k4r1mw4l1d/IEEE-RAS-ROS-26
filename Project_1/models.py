import json

class Drone:
    def __init__(self, drone_id, capacity=5, battery=100):
        self.drone_id = drone_id 
        self.battery = battery
        self.capacity = capacity
        self.position = [0, 0]

class Package:
    def __init__(self, weight, destination):
        self.weight = weight 
        self.destination = destination

class Fleet:
    def __init__(self):
        self.drones = []

    def save_to_json(self, filename="fleet_state.json"):
        data = [{"drone_id": d.drone_id, "battery": d.battery, "capacity": d.capacity} for d in self.drones]
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_from_json(self, filename="fleet_state.json"):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.drones = [Drone(d['drone_id'], d['capacity'], d['battery']) for d in data]
        except FileNotFoundError:
            self.drones = []
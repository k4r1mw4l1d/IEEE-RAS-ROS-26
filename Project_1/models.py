import json

class Drone:
    def __init__(self, drone_id, battery=100.0, capacity=10.0, position=[0, 0], total_power_used=0.0):
        self.drone_id = drone_id
        self.battery = battery
        self.capacity = capacity
        self.position = position
        self.total_power_used = total_power_used

class Package:
    def __init__(self, weight, destination):
        self.weight = weight
        self.destination = destination

class Fleet:
    def __init__(self):
        self.drones = []

    def save_to_json(self):
        data = [d.__dict__ for d in self.drones]
        with open("fleet_state.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_from_json(self):
        try:
            with open("fleet_state.json", "r") as f:
                data = json.load(f)
                self.drones = [Drone(**d) for d in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.drones = []
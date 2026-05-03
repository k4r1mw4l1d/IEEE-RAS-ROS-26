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
        data = []
        for d in self.drones:
            info = {
                "drone_id": d.drone_id, 
                "battery": d.battery,
                "capacity": d.capacity
            }
            data.append(info)

        f = open(filename, 'w')
        json.dump(data, f)
        f.close()
        print(f"Saved to {filename}")

    def load_from_json(self, filename="fleet_state.json"):
        try:
            f = open(filename, 'r')
            data = json.load(f)
            f.close()

            self.drones = []
            for d in data:
                new_drone = Drone(d['drone_id'], d['capacity'], d['battery'])
                self.drones.append(new_drone)
            print("Loaded Successfully")
        except:
            print("File not found")
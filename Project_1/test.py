from models import Fleet, Drone
from navigation import no_fly_zone, navigator


f = Fleet()
f.drones.append(Drone("ZAG-01", 10, 100)) 
f.save_to_json() 

test_fleet = Fleet()
test_fleet.load_from_json()

d = test_fleet.drones[0] 
print(d.drone_id, d.battery, d.capacity)

print("=" * 40)

navigator_test = navigator()
navigator_test.add_zone(2, 4, 2, 4)

navigator_test.get_path([0,0], [3,3])

navigator_test.get_path([0,0], [4,5])
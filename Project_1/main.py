from models import Drone, Package
from navigation import navigator
from mission import Mission

nav = navigator()
nav.add_zone_rectangle(2, 4, 2, 4)

drone = Drone("ZAG-01", capacity=10, battery=100)
package = Package(weight=5, destination=[6, 6])

m = Mission(drone, package, nav)
m.run()
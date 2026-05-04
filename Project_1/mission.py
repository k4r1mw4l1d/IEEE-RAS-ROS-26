from navigation import navigator

BASE_DRAIN = 2 


def calculate_flight_envelope(drone, package, path):
    """
    Calculates the total battery drain for a mission.
    Returns (drain_per_step, total_drain, is_feasible)
    """
    drain_per_step = BASE_DRAIN * (1 + package.weight / drone.capacity)
    total_drain = drain_per_step * len(path)

    usable_battery = drone.battery - 10
    is_feasible = total_drain <= usable_battery

    return drain_per_step, total_drain, is_feasible


class Mission:
    def __init__(self, drone, package, navigator):
        self.drone = drone
        self.package = package
        self.navigator = navigator
        self.status = "pending"  
        self.path = []

    def prepare(self):
        """Validate the mission before executing it. Returns True if ready."""
        
        if self.package.weight > self.drone.capacity:
            print(f"Mission failed: package weight ({self.package.weight}) "
                  f"exceeds drone capacity ({self.drone.capacity})")
            self.status = "cancelled"
            return False

        # Get path from navigator
        path = self.navigator.get_path(self.drone.position, self.package.destination)
        if path is None:
            print("Mission failed: no valid path to destination")
            self.status = "cancelled"
            return False

        # Check flight envelope (battery)
        drain_per_step, total_drain, is_feasible = calculate_flight_envelope(
            self.drone, self.package, path
        )

        if not is_feasible:
            usable = self.drone.battery - 10
            print(f"Mission failed: requires {total_drain:.1f} battery units "
                  f"but only {usable:.1f} usable (keeping 10% reserve)")
            self.status = "cancelled"
            return False

        # All checks passed
        self.path = path
        self.drain_per_step = drain_per_step
        print(f"Mission ready: {len(path)} steps, "
              f"{drain_per_step:.2f} drain/step, "
              f"{total_drain:.1f} total drain")
        return True

    def execute(self):
        """Move the drone step by step along the path."""

        if self.status == "cancelled":
            print("Cannot execute a cancelled mission")
            return

        self.status = "active"
        print(f"\nMission started: Drone {self.drone.drone_id} "
              f"delivering {self.package.weight}kg to {self.package.destination}")
        print("-" * 40)

        for step in self.path:
            # Check battery before each step (10% emergency threshold)
            if self.drone.battery <= 10:
                print(f"Battery critical ({self.drone.battery:.1f}%)! "
                      f"Cancelling mission, returning to base.")
                self._return_to_base()
                return

            # Move drone and drain battery
            self.drone.position = step
            self.drone.battery -= self.drain_per_step
            print(f"  Drone at {self.drone.position} | "
                  f"Battery: {self.drone.battery:.1f}%")

        # Destination reached
        self.status = "delivered"
        print(f"\nDelivered! Drone {self.drone.drone_id} reached "
              f"{self.package.destination} with {self.drone.battery:.1f}% battery remaining")

    def _return_to_base(self):
        """Emergency return to [0, 0]."""
        return_path = self.navigator.get_path(self.drone.position, [0, 0])

        if return_path is None:
            print("Warning: cannot find path back to base!")
            self.status = "cancelled"
            return

        print("Returning to base...")
        for step in return_path:
            self.drone.position = step
            self.drone.battery -= BASE_DRAIN   # no package on return trip
            print(f"  Returning: {self.drone.position} | "
                  f"Battery: {self.drone.battery:.1f}%")

        self.status = "cancelled"
        print(f"Drone {self.drone.drone_id} returned to base safely")

    def run(self):
        """Convenience method: prepare then execute in one call."""
        if self.prepare():
            self.execute()
BASE_DRAIN = 2.0

class Mission:
    def __init__(self, drone, package, navigator):
        self.drone = drone
        self.package = package
        self.navigator = navigator
        self.status = "pending"
        self.path = []
        self.drain_per_step = BASE_DRAIN

    def prepare(self):
        if not self.path: return False
        # Calculate drain rate: heavier packages drain battery faster
        self.drain_per_step = BASE_DRAIN * (1 + self.package.weight / self.drone.capacity)
        return True

    def trigger_emergency_return(self):
        self.status = "emergency_return"
        # Calculate new path from current location back to base [0,0]
        return_path = self.navigator.get_path(self.drone.position, [0, 0])
        if return_path:
            self.path = return_path
            return True
        return False
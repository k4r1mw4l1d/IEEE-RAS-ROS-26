class no_fly_zone:
    def __init__(self, coordinates):
        self.blocked = set()
        for point in coordinates:
            self.blocked.add((point[0], point[1]))

    @classmethod
    def from_rectangle(cls, x1, x2, y1, y2):
        """Helper to create a zone from a rectangle instead of listing every point."""
        coords = []
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                coords.append([x, y])
        return cls(coords)

    def check_forbidden(self, x, y):
        return (x, y) in self.blocked


class navigator:
    def __init__(self):
        self.zones = []

    def add_zone(self, coordinates):
        """Register a no-fly zone as a cluster of coordinates."""
        new_zone = no_fly_zone(coordinates)
        self.zones.append(new_zone)

    def add_zone_rectangle(self, x1, x2, y1, y2):
        """Convenience method to register a rectangular no-fly zone."""
        new_zone = no_fly_zone.from_rectangle(x1, x2, y1, y2)
        self.zones.append(new_zone)

    def is_blocked(self, x, y):
        """Check if a point is inside any registered no-fly zone."""
        for zone in self.zones:
            if zone.check_forbidden(x, y):
                return True
        return False

    def get_path(self, start, end):
        current_x, current_y = start[0], start[1]
        path = [start]

        while [current_x, current_y] != end:
            moved = False

            candidates = []
            if current_x < end[0]:
                candidates.append((current_x + 1, current_y))
            elif current_x > end[0]:
                candidates.append((current_x - 1, current_y))
            if current_y < end[1]:
                candidates.append((current_x, current_y + 1))
            elif current_y > end[1]:
                candidates.append((current_x, current_y - 1))

            # Try the preferred moves first
            for nx, ny in candidates:
                if not self.is_blocked(nx, ny):
                    current_x, current_y = nx, ny
                    path.append([current_x, current_y])
                    moved = True
                    break

            if not moved:
                detours = [
                    (current_x + 1, current_y),
                    (current_x - 1, current_y),
                    (current_x, current_y + 1),
                    (current_x, current_y - 1),
                ]
                for nx, ny in detours:
                    if not self.is_blocked(nx, ny) and [nx, ny] not in path:
                        current_x, current_y = nx, ny
                        path.append([current_x, current_y])
                        moved = True
                        break

            if not moved:
                print(f"Path blocked: no route from {start} to {end}")
                return None

        print(f"Path found: {path}")
        return path
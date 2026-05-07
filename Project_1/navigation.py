import heapq

class no_fly_zone:
    def __init__(self, coordinates):
        self.blocked = set((point[0], point[1]) for point in coordinates)

    @classmethod
    def from_rectangle(cls, x1, x2, y1, y2):
        coords = [[x, y] for x in range(min(x1, x2), max(x1, x2) + 1) 
                         for y in range(min(y1, y2), max(y1, y2) + 1)]
        return cls(coords)

    def check_forbidden(self, x, y):
        return (x, y) in self.blocked

class navigator:
    def __init__(self):
        self.zones = []

    def add_zone_rectangle(self, x1, x2, y1, y2):
        label = f"Zone: ({x1},{y1}) to ({x2},{y2})"
        self.zones.append({"label": label, "zone": no_fly_zone.from_rectangle(x1, x2, y1, y2)})

    def remove_zone(self, index):
        if 0 <= index < len(self.zones): self.zones.pop(index)

    def is_blocked(self, x, y):
        if not (0 <= x <= 20 and 0 <= y <= 20): return True
        return any(z["zone"].check_forbidden(x, y) for z in self.zones)

    def get_path(self, start, end):
        start, end = tuple(start), tuple(end)
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from, g_score = {}, {start: 0}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == end:
                path = []
                while current in came_from:
                    path.append(list(current)); current = came_from[current]
                path.append(list(start)); return path[::-1]

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if not self.is_blocked(*neighbor):
                    tentative_g = g_score[current] + 1
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f_score = tentative_g + abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1])
                        heapq.heappush(open_set, (f_score, neighbor))
        return None
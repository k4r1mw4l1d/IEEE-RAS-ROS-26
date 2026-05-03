class no_fly_zone:
    def __init__(self, x1, x2, y1, y2):
        self.x_min = min(x1, x2)
        self.x_max = max(x1, x2)
        self.y_min = min(y1, y2)
        self.y_max = max(y1, y2)

    def check_forbidden(self, x, y):
        if self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max:
            return True
        else:
            return False
        
class navigator:
    def __init__(self):
        self.zones = []

    def add_zone(self, x1, x2, y1, y2):
        new_zone = no_fly_zone(x1, x2, y1, y2)
        self.zones.append(new_zone)

    def get_path(self, start, end):
        current_x = start[0]
        current_y = start[1]
        path = []

        while [current_x, current_y] != end:
            if current_x < end[0]:
                current_x += 1
            elif current_x > end[0]:
                current_x -+ 1
            elif current_y < end[1]:
                current_y += 1
            elif current_y > end[1]:
                current_y -+ 1
    

        blocked = 0
        for zone in self.zones:
            if zone.check_forbidden(current_x, current_y):
                print("Path Blocked Cannot Enter here")
                blocked = 1
                break
        
        path.append([current_x, current_y])

        if blocked:
            print("Cannot Use This Path")
        else:
            print(f"Not Forbidden Area, The Path is {path}")
        






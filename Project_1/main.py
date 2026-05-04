import os
import time
from colorama import init, Fore, Style
from models import Drone, Package
from navigation import navigator
from mission import calculate_flight_envelope, BASE_DRAIN

init()  # initialize colorama for Windows

GRID_SIZE = 15
STEP_DELAY = 0.3   # seconds between each move


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def battery_bar(battery):
    filled = int(battery / 5)
    bar = "█" * filled + "░" * (20 - filled)
    if battery > 50:
        color = Fore.GREEN
    elif battery > 20:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    return f"{color}[{bar}] {battery:.1f}%{Style.RESET_ALL}"


def draw_grid(drone_pos, destination, blocked_points, path_taken, info_lines):
    clear()
    print(Fore.WHITE + Style.BRIGHT + "AeroPath Terminal Simulation")
    print("-" * (GRID_SIZE * 2 + 2) + Style.RESET_ALL)

    for row in range(GRID_SIZE):
        line = "  "
        for col in range(GRID_SIZE):
            point = [col, GRID_SIZE - 1 - row]

            if point == drone_pos:
                line += Fore.GREEN + Style.BRIGHT + "D " + Style.RESET_ALL
            elif point == destination:
                line += Fore.YELLOW + Style.BRIGHT + "X " + Style.RESET_ALL
            elif tuple(point) in blocked_points:
                line += Fore.RED + "# " + Style.RESET_ALL
            elif point in path_taken:
                line += Fore.CYAN + ". " + Style.RESET_ALL
            else:
                line += "+ "
        print(line)

    print("-" * (GRID_SIZE * 2 + 2))
    print(Fore.WHITE + "  D = Drone    " +
          Fore.YELLOW + "X = Destination    " +
          Fore.RED + "# = No-fly zone    " +
          Fore.CYAN + ". = Path taken" + Style.RESET_ALL)
    print("-" * (GRID_SIZE * 2 + 2))

    for line in info_lines:
        print(line)


def run_simulation(drone, package, nav):
    blocked_points = set()
    for zone in nav.zones:
        blocked_points.update(zone.blocked)

    destination = package.destination

    path = nav.get_path(drone.position, destination)
    if path is None:
        print(Fore.RED + "No valid path found!" + Style.RESET_ALL)
        return

    drain_per_step, total_drain, feasible = calculate_flight_envelope(drone, package, path)
    if not feasible:
        usable = drone.battery - 10
        print(Fore.RED + f"Insufficient battery! Need {total_drain:.1f} but only {usable:.1f} usable." + Style.RESET_ALL)
        return

    path_taken = []
    status = "In Flight"

    for step in path:
        if drone.battery <= 10:
            status = Fore.RED + "CRITICAL - Returning to base!" + Style.RESET_ALL
            return_path = nav.get_path(drone.position, [0, 0])
            if return_path:
                for rp in return_path:
                    drone.position = list(rp)
                    drone.battery = max(0, drone.battery - BASE_DRAIN)
                    path_taken.append(list(rp))
                    info = [
                        f"  Drone    : {Fore.GREEN}{drone.drone_id}{Style.RESET_ALL}",
                        f"  Status   : {status}",
                        f"  Position : {drone.position}",
                        f"  Battery  : {battery_bar(drone.battery)}",
                    ]
                    draw_grid(drone.position, destination, blocked_points, path_taken, info)
                    time.sleep(STEP_DELAY)
            status = Fore.YELLOW + "Returned to Base" + Style.RESET_ALL
            break

        drone.position = list(step)
        drone.battery = max(0, drone.battery - drain_per_step)
        path_taken.append(list(step))

        if drone.position == destination:
            status = Fore.GREEN + Style.BRIGHT + "Delivered!" + Style.RESET_ALL

        info = [
            f"  Drone    : {Fore.GREEN}{drone.drone_id}{Style.RESET_ALL}",
            f"  Status   : {status}",
            f"  Position : {drone.position}",
            f"  Battery  : {battery_bar(drone.battery)}",
            f"  Payload  : {package.weight}kg  |  Drain/step: {drain_per_step:.2f}",
            f"  Steps    : {len(path_taken)} / {len(path)}",
        ]
        draw_grid(drone.position, destination, blocked_points, path_taken, info)
        time.sleep(STEP_DELAY)

    input("\n  Press Enter to exit...")


if __name__ == "__main__":
    drone = Drone("ZAG-01", capacity=10, battery=100)
    package = Package(weight=5, destination=[10, 10])

    nav = navigator()
    nav.add_zone_rectangle(3, 3, 2, 8)
    nav.add_zone_rectangle(6, 9, 5, 5)

    run_simulation(drone, package, nav)
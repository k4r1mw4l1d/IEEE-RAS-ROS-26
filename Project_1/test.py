from navigation import no_fly_zone, navigator

print("=" * 50)
print("TEST 1: Free path, no zones")
print("=" * 50)
nav = navigator()
path = nav.get_path([0, 0], [3, 3])
assert path is not None, "Should find a path"
assert path[0] == [0, 0], "Should start at [0,0]"
assert path[-1] == [3, 3], "Should end at [3,3]"
print("PASSED\n")

print("=" * 50)
print("TEST 2: Rectangular zone, path goes around it")
print("=" * 50)
# Zone blocks [2,0] to [2,4] — a vertical wall
nav = navigator()
nav.add_zone_rectangle(2, 2, 0, 4)
path = nav.get_path([0, 0], [4, 0])
assert path is not None, "Should find a detour"
for step in path:
    assert not nav.is_blocked(step[0], step[1]), f"Step {step} goes through no-fly zone!"
assert path[-1] == [4, 0], "Should still reach destination"
print("PASSED\n")

print("=" * 50)
print("TEST 3: Cluster zone (irregular shape)")
print("=" * 50)
nav = navigator()
nav.add_zone([[1, 1], [1, 2], [2, 1]])   # L-shaped zone
path = nav.get_path([0, 0], [3, 3])
assert path is not None, "Should find a path around L-shape"
for step in path:
    assert not nav.is_blocked(step[0], step[1]), f"Step {step} goes through no-fly zone!"
assert path[-1] == [3, 3], "Should reach destination"
print("PASSED\n")

print("=" * 50)
print("TEST 4: Destination is unreachable (fully surrounded)")
print("=" * 50)
nav = navigator()
# Surround [2,2] on all 4 sides
nav.add_zone([[1, 2], [3, 2], [2, 1], [2, 3]])
path = nav.get_path([0, 0], [2, 2])
assert path is None, "Should return None — destination unreachable"
print("PASSED\n")

print("=" * 50)
print("TEST 5: Start equals end")
print("=" * 50)
nav = navigator()
path = nav.get_path([2, 2], [2, 2])
assert path == [[2, 2]], "Path should just be the start point"
print("PASSED\n")

print("=" * 50)
print("TEST 6: Multiple zones, path threads between them")
print("=" * 50)
nav = navigator()
nav.add_zone_rectangle(1, 1, 0, 3)   # vertical wall at x=1
nav.add_zone_rectangle(3, 3, 1, 4)   # vertical wall at x=3
path = nav.get_path([0, 0], [4, 4])
assert path is not None, "Should thread between two walls"
for step in path:
    assert not nav.is_blocked(step[0], step[1]), f"Step {step} goes through no-fly zone!"
assert path[-1] == [4, 4], "Should reach destination"
print("PASSED\n")

print("=" * 50)
print("ALL TESTS PASSED")
print("=" * 50)
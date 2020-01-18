from typing import Dict, List

from utils.cli import lines_in

CENTER_OF_MASS = 'COM'

orbit_list = [tuple(pair.split(')')) for pair in lines_in]

orbit_graph: Dict[str, List[str]] = {}
for center, orbiter in orbit_list:
    if center not in orbit_graph:
        orbit_graph[center] = [orbiter]
    else:
        orbit_graph[center].append(orbiter)


def orbit_count(node, depth=1):
    chksum = 0
    for o in orbit_graph.get(node, []):
        chksum += depth + orbit_count(o, depth=depth + 1)
    return chksum


print(orbit_count(CENTER_OF_MASS))

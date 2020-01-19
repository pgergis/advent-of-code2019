from typing import Dict, List

from utils.cli import lines_in


class Planet:
    def __init__(self, name):
        self.name = name
        self.orbiting = None
        self.orbited_by: List[Planet] = []

    def register(self, registry):
        registry[self.name] = self

    def add_to_orbit(self, other):
        self.orbited_by.append(other)
        other.oribiting = self


planet_registry: Dict[str, Planet] = {}
CENTER_OF_MASS = Planet("COM")
CENTER_OF_MASS.register(planet_registry)

orbit_list = [tuple(pair.split(")")) for pair in lines_in]
for center, orbiter in orbit_list:
    if center not in planet_registry:
        c = Planet(center)
        c.register(planet_registry)
    else:
        c = planet_registry[center]

    if orbiter not in planet_registry:
        o = Planet(orbiter)
        o.register(planet_registry)
    else:
        o = planet_registry[orbiter]

    c.add_to_orbit(o)


def orbit_count(node, depth=1):
    chksum = 0
    for o in node.orbited_by:
        chksum += depth + orbit_count(o, depth=depth + 1)
    return chksum

def transfers_to_target(start, end, visited=set()):
    pass


print("pt.1 (checksum):", orbit_count(CENTER_OF_MASS))

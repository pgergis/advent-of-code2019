CENTER_OF_MASS = "COM"


def build_orbit_graph(orbit_lines):
    def orbit_to_edge(orbit):
        return tuple(orbit.split(")"))

    graph = {}
    for orbit in orbit_lines:
        center, child = orbit_to_edge(orbit)
        if center not in graph:
            graph[center] = []
        graph[center].append(child)

    return graph


def get_all_orbits(center, orbit_graph):
    return [center] + [
        get_all_orbits(c, orbit_graph) for c in orbit_graph.get(center, [])
    ]


def count_all_orbits(orbit_graph):
    full_orbital_walk = get_all_orbits(CENTER_OF_MASS, orbit_graph)
    return full_orbital_walk



if __name__ == "__main__":
    from utils.cli import lines_in

    orbit_graph = build_orbit_graph(lines_in)

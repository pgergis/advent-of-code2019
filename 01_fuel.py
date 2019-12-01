def get_fuel_required(mass):
    return mass // 3 - 2


def get_fuel_required_extra(mass):
    fuel_req = max(get_fuel_required(mass), 0)
    if fuel_req == 0:
        return fuel_req

    return fuel_req + get_fuel_required_extra(fuel_req)


if __name__ == '__main__':
    from utils.file_parser import lines_in

    module_masses = list(map(int, lines_in))
    print(sum(map(get_fuel_required, module_masses)))
    print(sum(map(get_fuel_required_extra, module_masses)))

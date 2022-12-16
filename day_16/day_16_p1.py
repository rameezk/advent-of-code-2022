from common.timing import timeit


def parse_data(filename: str) -> tuple[dict, dict, dict]:
    flow_rates = {}
    valves_to = {}
    valves_open = {}

    with open(filename) as file:
        for line in file:
            words = line.strip().split()
            valve = words[1]
            flow_rate = int(words[4].split("=")[1].split(";")[0])
            to_valves = list(map(lambda w: w.replace(",", ""), words[9:]))

            flow_rates[valve] = flow_rate
            valves_to[valve] = to_valves
            valves_open[valve] = False

    return flow_rates, valves_to, valves_open


def calculate_pressure(valves_open: dict, flow_rates: dict):
    return sum(flow_rates[k] for k, v in valves_open.items() if v)


def simulate(
    minute,
    valve: str,
    pressures: list[int],
    valves_open: dict,
    flow_rates: dict,
    valves_to: dict,
    visited: dict,
):
    global most_pressure

    if visited.get((minute, valve), -1) >= sum(pressures):
        return
    visited[minute, valve] = sum(pressures)

    if minute == 30:
        most_pressure = max(most_pressure, sum(pressures))
        return

    # check every 2 min
    for should_try_open in [True, False]:
        if should_try_open:

            # If already open, don't open
            if valves_open[valve] or flow_rates[valve] <= 0:
                continue

            valves_open[valve] = True
            pressure = calculate_pressure(valves_open, flow_rates)
            simulate(
                minute + 1,
                valve,
                pressures + [pressure],
                valves_open,
                flow_rates,
                valves_to,
                visited,
            )
            valves_open[valve] = False
        else:
            pressure = calculate_pressure(valves_open, flow_rates)
            for to_valve in valves_to[valve]:
                simulate(
                    minute + 1,
                    to_valve if to_valve is not None else valve,
                    pressures + [pressure],
                    valves_open,
                    flow_rates,
                    valves_to,
                    visited,
                )


# The most horrible global variable ever
most_pressure = 0


@timeit
def solve_p1():
    flow_rates, valves_to, valves_open = parse_data("./input.txt")
    simulate(1, "AA", [0], valves_open, flow_rates, valves_to, {})
    return most_pressure


if __name__ == "__main__":
    p1 = solve_p1()
    print(p1)

from typing import Dict, List, Tuple

def main():

    notes: List[str] = []
    with open('input.txt') as input_file:
        notes = input_file.read().split('\n')

    notes[1] = notes[1].split(',')
    print(notes[1])

    ##########
    # Part 1 #
    ##########
    
    timestamp: int = int(notes[0])
    buses: List[int] = [int(n) for n in notes[1] if n != 'x']

    # Dict mapping bus numbers to the time in minutes until that bus next 
    # departs.
    # At current time t, the time to the next bus number b is 
    #   abs((t % b) - b)
    times: Dict[int, int] = {bus:abs((timestamp % bus) - bus) for bus in buses}


    # The bus number with the minimum time until next departure.
    # Tuple of that bus number and the time in minutes until its next departure.
    earliest_bus: Tuple[int, int] = min(times.items(), key=lambda v: v[1])

    solution_1: int = earliest_bus[0] * earliest_bus[1]
    s1: str = f'Part 1: {solution_1}. The earliest bus is number '\
              f'{earliest_bus[0]} and it departs in {earliest_bus[1]} minutes.'
    print(s1)

    ##########
    # Part 2 #
    ##########
    # List of Tuples of bus number and its position in the original schedule.
    # We want a timestamp `t` where each bus comes at timestamp t+dt, where `dt`
    # is that bus's position in the original schedule (its index in `notes[1]`).
    buses: List[Tuple[int, int]] = [
        (int(notes[1][i]), i) for i in range(len(notes[1])) if notes[1][i] != 'x'
    ]
    # We want the first bus in the schedule to come at timestamp `t`, so we only
    # check multiples of that `bus_number`.
    increment = buses[0][0]
    t = 0

    # TODO: This straightforward solution is too slow for larger inputs.
    #       There probably exists a faster computation for dealing with large
    #       numbers of congruence relations.
    while sum([(t + dt) % bus_number for (bus_number, dt) in buses]) != 0:
        t += increment

    s2: str = f'Part 2: {t}.'
    print(s2)

    with open('solution.txt', mode='w') as output_file:
        output_file.write(f'{s1}\n{s2}')

if __name__ == '__main__':
    main()
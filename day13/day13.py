from typing import Dict, List

def main():

    notes: List[str] = []
    with open('input.txt') as input_file:
        notes = input_file.read().split('\n')

    timestamp: int = int(notes[0])
    buses: List[int] = [int(n) for n in notes[1].split(',') if n != 'x']

    # Dict mapping bus numbers to the time until that bus next departs.
    # At current time t, the time to the next bus number b is 
    #   abs((t % b) - b)
    times: Dict[int, int] = {bus:abs((timestamp % bus) - bus) for bus in buses}

    earliest_bus: Tuple[int, int] = min(times.items(), key=lambda v: v[1])

    solution_1: int = earliest_bus[0] * earliest_bus[1]
    s1: str = f'Part 1: {solution_1}. The earliest bus is number '\
              f'{earliest_bus[0]} and it departs in {earliest_bus[1]} minutes.'
    print(s1)

    with open('solution.txt', mode='w') as output_file:
        output_file.write(s1)

if __name__ == '__main__':
    main()
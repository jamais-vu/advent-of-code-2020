from typing import Dict, List

def main():

    # Numbers spoken, where the number at index `i` was spoken on turn `i+1`.
    numbers: List[int] = []

    with open('input.txt') as input_file:
        numbers = [int(x) for x in input_file.read().split(',')]

    solution_1: int = nth_number_spoken(numbers, 2020)
    s1: str = f'Part 1: The 2020th number spoken is {solution_1}.'
    print(s1)

    solution_2: int = nth_number_spoken(numbers, 30000000)
    s2: str = f'Part 2: The 30000000th number spoken is {solution_2}.'
    print(s2)

    with open('solution.txt', mode='w') as output_file:
        output_file.write(f'Part 1: {solution_1}\nPart 2: {solution_2}')


def nth_number_spoken(numbers: List[int], n: int) -> int:
    """Given a list of starting numbers, finds the nth number spoken."""
    turn: int = len(numbers)
    most_recent_number: int = numbers[-1]

    # Dict of numbers mapped to the turn on which each number was last spoken.
    # The value is `index + 1` because that is the turn number.
    # We exclude the most recent number because we check it against the 
    # dictionary to see if it was spoken before.
    previously_spoken: Dict[int, int] = {
        n:index + 1 for index, n in enumerate(numbers[:-1])
    }

    previous_turn: int
    while turn < n:
        if most_recent_number in previously_spoken:
            # The turn on which the most recent number was previously spoken.
            previous_turn = previously_spoken[most_recent_number]
            # We set the TODO 
            previously_spoken[most_recent_number] = turn
            # The next number is the difference between the two turns on which
            # the most recent number was spoken.
            most_recent_number = turn - previous_turn
        else:
            previously_spoken[most_recent_number] = turn
            most_recent_number = 0

        turn += 1

    return most_recent_number


if __name__ == '__main__':
    main()
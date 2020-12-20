from typing import Dict, List

def main():

    # Numbers spoken, where the number at index `i` was spoken on turn `i+1`.
    starting_numbers: List[int] = []

    with open('input.txt') as input_file:
        starting_numbers = [int(x) for x in input_file.read().split(',')]

    ##########
    # Part 1 #
    ##########
    # If we don't copy starting_numbers then it will be modified for part 2.
    numbers: List[int] = starting_numbers.copy()
    while len(numbers) < 2020:
        numbers += [next_number(numbers)]

    solution_1: int = numbers[-1]
    s1: str = f'Part 1: The 2020th number spoken is {solution_1}.'
    print(s1)

    ##########
    # Part 2 #
    ##########
    # Dict here is kinda slow. For larger n I'd seek a faster solution.
    numbers: List[int] = starting_numbers.copy()
    
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
    while turn < 30000000:
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

    print(turn)
    print(most_recent_number)
    # print(last_spoken)


def next_number(numbers: List[int]) -> int:
    """Determines the next number to be spoken."""
    current_turn: int = len(numbers)
    most_recent_number: int = numbers[-1]

    if most_recent_number not in numbers[0:-1]:
        # If the last number was not spoken before, the next number is 0.
        return 0
    else:
        # We use numbers[:-1] to exclude the most recent number, since we want 
        # the index where it was spoken before that.
        turn_last_spoken: int = most_recent_index(numbers[:-1], most_recent_number) + 1
        return current_turn - turn_last_spoken


def most_recent_index(numbers: List[int], n: int) -> int:
    """Returns the greatest index in numbers which contains n.

    Raises ValueError if n is not in the given list.
    """
    for i in reversed(range(len(numbers))):
        if n == numbers[i]:
            return i

    raise ValueError(f'{n} is not in numbers.')


if __name__ == '__main__':
    main()
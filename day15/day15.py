from typing import List

def main():

    # Numbers spoken, where the number at index `i` was spoken on turn `i+1`.
    numbers: List[int] = []

    with open('input.txt') as input_file:
        numbers = [int(x) for x in input_file.read().split(',')]

    while len(numbers) < 2020:
        numbers += [next_number(numbers)]

    solution_1: int = numbers[-1]
    s1: str = f'Part 1: The 2020th number spoken is {solution_1}.'

    print(s1)

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
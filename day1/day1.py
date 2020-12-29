import functools
import itertools
import operator

from typing import List, Tuple


def main():
    
    with open('input.txt') as fo:
        numbers = list(map(int, fo.read().split('\n')))

    # Part 1: 2 numbers which sum to 2020
    goal = 2020
    pair = solve(numbers, goal, 2)
    solution_1 = functools.reduce(operator.mul, pair)
    s1 = f'Part 1: The pair which sum to {goal} is {pair}, and their product is {solution_1}'
    print(s1)

    # Part 2: 3 numbers which sum to 2020
    goal = 2020
    triple = solve(numbers, goal, 3)
    solution_2 = functools.reduce(operator.mul, triple)
    s2 = f'Part 2: The pair which sum to {goal} is {triple}, and their product is {solution_2}'
    print(s2)

    with open('solution.txt', mode='w') as fo:
        fo.write(f'{s1}\n{s2}')


def read_from_file(input_file: str) -> List[int]:
    """Returns a list of integers in a text file with one integer per line."""
    numbers = []
    with open(input_file, mode='r') as file_object:
        for line in file_object:
            numbers.append(int(line)) # Cast to int because we know they're ints
    return numbers


def solve(numbers: List[int], goal: int, n: int) -> Tuple[int]:
    """
    Finds which n-tuple of numbers in the list sums to the goal, and prints that 
    n-tuple as well as their product.

    Note: This assumes such an n-tuple exists in the given list.

    TODO: I think the type hint `Tuple[int]` is incorrect and denotes an n-tuple
          specifically of length 1.
    """

    # Create a generator of all n-tuples of numbers in the list
    combos = itertools.combinations(numbers, n)

    ntuple = tuple([0 for i in range(n)])

    while sum(ntuple) != goal:
        ntuple = next(combos )
    
    return ntuple


if __name__ == '__main__':
    main()
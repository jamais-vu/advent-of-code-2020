import sys

sys.path.append('..')

from typing import Dict, List, Tuple
from utilities import prod, write_to_file

def main():

    # Text representation of open squares ('.') and trees ('#').
    # Row `tree_grid[i]` is a string representing the ith row from the top.
    # Column `tree_grid[i][j]` is the jth letter from the left in the ith row.
    tree_grid: List[str]
    with open('input.txt') as input_file:
        tree_grid = (input_file.read()).split('\n')

    ##########
    # Part 1 #
    ##########

    # slope[0] represents the step right. slope[1] represents the step down.
    slope_1: Tuple[int, int] = (3, 1)
    solution_1: int = solve(tree_grid, slope_1)

    s1: str = f'Part 1: With slope {slope_1}, we encounter {solution_1} trees.'
    print(s1)

    ##########
    # Part 2 #
    ##########

    # We want to check the results of several slopes, and then multiply those
    # results together.
    # We create a dict mapping slopes to results.
    slopes_and_results: Dict[Tuple[int, int], int] = {
        (1, 1): 0,
        (3, 1): 0,
        (5, 1): 0,
        (7, 1): 0,
        (1, 2): 0
    }

    for slope in slopes_and_results.keys():
        slopes_and_results[slope] = solve(tree_grid, slope)

    solution_2: int = prod(slopes_and_results.values())
    s2: str = f'Part 2: The product of the results of the given slopes is {solution_2}.'

    for slope, result in slopes_and_results.items():
        s2 += f'\n\t- With slope {slope}, we encounter {result} trees.'

    print(s2)

    write_to_file([s1, s2], 'solution.txt')

def solve(tree_grid: List[str], slope: Tuple[int, int], debug: bool = False) -> int:
    """Goes through the tree grid and counts the number of trees encountered."""

    # Each row in the tree grid has the same length, which we consider to repeat
    # infinitely to the right. We use modular arithmetic to determine position.
    modulus: int = len(tree_grid[0])

    if debug:
        print(f'number of columns: {modulus}')
        print(f'number of rows:    {len(tree_grid)}')

    step_right: int = slope[0]
    step_down: int = slope[1]

    if debug:
        replaced_grid: List[str] = tree_grid.copy()
    
    # We start with i=1 because we do not check the starting position, which
    # is always open ('.').
    tree_count: int = 0
    j: int = 0
    for i in range(0, len(tree_grid), step_down):

            row = tree_grid[i]

            if debug:
                replaced_row = replace_row(row, j)
                replaced_grid[i] = replaced_row

            if row[j] == '#':
                tree_count += 1

                if debug:
                    replaced_grid[i] = replaced_row + f' j={j}'

            if debug:
                print(f'i,j: {i},{j}')
                print(f'tree_row: {row}')
                print(f'repl_row: {replaced_row}')

            j = (j + step_right) % modulus
            print(f'`j = (j + step_right) % modulus` ->\
            j = ({j} + {step_right}) % {modulus} -> {j}')

    if debug:
        draw_tree_grid: str = '\n'.join(f'{tree_grid[i]} i={str(i)}' for i in range(len(tree_grid)))
        draw_replaced_grid: str = '\n'.join(f'{replaced_grid[i]} i={str(i)}' for i in range(len(replaced_grid)))
        print(f'tree_grid:\n{draw_tree_grid}')
        print(f'replaced_grid:\n{draw_replaced_grid}')
        write_to_file(replaced_grid, 'replaced_grid.txt')

    return tree_count

def replace_row(row: str, j: int) -> str:
    """Returns the given row with the character at position j replaced.
    
    Used for visualizing the result of a path.
    """
    if row[j] == '.':
        return row[0:j] + 'O' + row[j+1:]
    elif row[j] == '#':
        return row[0:j] + 'X' + row[j+1:]
    else:
        raise Exception(f"Given row '{row}'' has neither '.' nor '#' at {j}!")

if __name__ == '__main__':
    main()
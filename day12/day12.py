from collections import namedtuple
from typing import Dict, List, NamedTuple, Tuple

def main():

    instructions: List[str] = []
    with open('input.txt') as input_file:
        instructions = input_file.read().split('\n')

    # Instructions is a list of actions:
    # - Action N means to move north by the given value.
    # - Action S means to move south by the given value.
    # - Action E means to move east by the given value.
    # - Action W means to move west by the given value.
    # - Action L means to turn left the given number of degrees.
    # - Action R means to turn right the given number of degrees.
    # - Action F means to move forward by the given value in the direction the 
    #   ship is currently facing.

    position: Tuple[int, int, int] = (0, 0, 0)
    for instruction in instructions:
        print('position: ', position)
        print('instruction: ', instruction)
        position = move(position, instruction)

    print('Done. position: ', position)
    manhattan_distance_from_start = abs(position[0]) + abs(position[1])
    s1 = f'Part 1: The Manhattan distance is {manhattan_distance_from_start}.'
    print(s1)

    with open('solution.txt', mode='w') as output_file:
        output_file.write(s1)

def move(position: Tuple[int, int, int], instruction: str) -> Tuple[int, int, int]:
    """TODO docstring"""
    x: int = position[0]
    y: int = position[1]
    angle: int = position[2]

    action: str = instruction[0]
    value: int = int(instruction[1:])

    if action == 'N':
        return (x, y + value, angle)
    
    elif action == 'S':    
        return (x, y - value, angle)

    elif action == 'E':    
        return (x + value, y, angle)

    elif action == 'W':    
        return (x - value, y, angle)

    elif action == 'L':
        return (x, y, (angle + value) % 360)

    elif action == 'R':
        return (x, y, (angle - value) % 360)

    elif action == 'F':
        instruction: str = angle_to_direction(angle) + str(value)
        return move(position, instruction)

def angle_to_direction(angle: int) -> str:
    """TODO docstring"""
    cardinal_directions: Dict[int, str] = {
        0: 'E',
        90: 'N',
        180: 'W',
        270: 'S'
    }
    return cardinal_directions[angle]

if __name__ == '__main__':
    main()
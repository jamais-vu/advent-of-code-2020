import functools
import numpy as np

from typing import List

def main():

    seats: List[str] = []
    # seats = np.loadtxt('example_1.txt', dtype=np.str)
    with open('input.txt') as input_file:
        seats = input_file.read().split('\n')
    
    ca: CellularAutomaton = CellularAutomaton(seats)

    # print(ca)

    ca.find_stable_grid()

    print(ca.count_occupied_seats())

    # print(ca)


class CellularAutomaton:
    def __init__(self, grid: List[str]) -> None:
        self.initial_grid: List[str] = grid
        self.grid: List[str] = grid
        self.time: int = 0 # Number of steps since initial grid

    def count_occupied_seats(self) -> int:
        return sum([row.count('#') for row in self.grid])

    def find_stable_grid(self, debug: bool = False) -> None:
        next_grid: List[str] = self.next_grid()

        while self.grid != next_grid:
            if debug:
                print(f'time={self.time}\n{self.grid_to_str(self.grid)}')
                print(f'time={self.time+1}\n{self.grid_to_str(next_grid)}')
                input('press enter to advance to next grid')
            self.grid = next_grid
            next_grid = self.next_grid()
            self.time += 1

        print('stable grid reached')

    def next_grid(self) -> List[str]:
        """TODO"""

        new_grid: List[str] = []
        
        for i in range(0, len(self.grid)):    
            row: str = self.grid[i]
            new_row: str = ''
            for j in range(0, len(row)):
                new_cell = self.cell_transition(i, j)
                new_row += new_cell

            new_grid += [new_row]

        return new_grid
                
    def cell_transition(self, i: int, j: int, debug: bool = False) -> str:
        """Transitions a cell from its current state to next state."""
        adjacent_cell_states = self.get_adjacent_cell_states(i, j)
        state = self.grid[i][j]
    
        if (state == 'L') and (adjacent_cell_states.count('#') == 0):
            # Seat is empty and and no adjacent seat is occupied.
            if debug: print(f'{i},{j} is {state} and has adjacent seats {adjacent_cell_states} -> #')
            return '#' # Seat becomes occupied.
        
        elif (state == '#') and (adjacent_cell_states.count('#') >= 4):
            # Seat is occupied and at least four adjacent seats are occupied.
            if debug: print(f'{i},{j} is {state} and has adjacent seats {adjacent_cell_states} -> L') 
            return 'L' # Seat becomes empty.

        else:
            if debug: print(f'{i},{j} is {state} and has adjacent seats {adjacent_cell_states} -> do nothing')
            return state # Seat state does not change.

    def get_adjacent_cell_states(self, i: int, j: int, debug: bool = False) -> List[str]:
        """TODO

        Two cells are adjacent if they are immediately up, down, left, right, or 
        diagonal from each other.
        """
        adjacent_cell_states: List[str] = []
        for x in range(i - 1, i + 2):
            for y in range(j -1, j + 2):
                if not (x == -1 or y == -1):
                # Negative values will "wrap" around to the opposite row or 
                # column, giving us incorrect adjacencies. 
                    try: 
                        adjacent_cell_states.append(self.grid[x][y])
                    except IndexError:
                            if debug:
                                print(f'[{x}][{y}] out of grid indices.')
        # The above for loops add the cell at (i, j) itself, which we don't
        # consider adjacent, so we remove it.
        adjacent_cell_states.remove(self.grid[i][j])
        return adjacent_cell_states
    
    def grid_to_str(self, grid: List[str], indent_length: int = 2) -> str:
        indent = ' ' * indent_length
        return indent + f'\n{indent}'.join(grid)

    def __str__(self):
        initial_grid_to_str: str = f'time=0\n{self.grid_to_str(self.initial_grid)}'
        current_grid_to_str: str = f'time={self.time}\n{self.grid_to_str(self.grid)}'
        return f'{initial_grid_to_str}\n{current_grid_to_str}'\

if __name__ == '__main__':
    main()
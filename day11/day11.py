from typing import Callable, List, Tuple

def main():

    seats: List[str] = []
    # seats = np.loadtxt('example_1.txt', dtype=np.str)
    with open('example_1.txt') as input_file:
        seats = input_file.read().split('\n')
    
    ca: CellularAutomaton = CellularAutomaton(seats)

    # print(ca)

    ca.find_stable_grid(ca.transition_rule_1)

    print(ca.count_occupied_seats())

    # print(ca)


class CellularAutomaton:
    def __init__(self, grid: List[str]) -> None:
        self.initial_grid: List[str] = grid
        self.grid: List[str] = grid
        self.time: int = 0 # Number of steps since initial grid

    def count_occupied_seats(self) -> int:
        return sum([row.count('#') for row in self.grid])

    def find_stable_grid(
        self,
        transition_rule: Callable[[Tuple[int]], str],
        debug: bool = False
        ) -> None:
        """
        Repeatedly transitions the grid under the given transition rule, until
        the grid is in a state such that no cell changes under that rule.
        """
        next_grid: List[str] = self.next_grid(transition_rule)

        while self.grid != next_grid:
            if debug:
                print(f'time={self.time}\n{self.grid_to_str(self.grid)}')
                print(f'time={self.time+1}\n{self.grid_to_str(next_grid)}')
                input('press enter to advance to next grid')
            self.grid = next_grid
            next_grid = self.next_grid(transition_rule)
            self.time += 1

        print('stable grid reached')

    def next_grid(
        self, 
        transition_rule: Callable[[Tuple[int]], str]
        ) -> List[str]:
        """Returns the next grid, determined by a given cell transition rule."""

        new_grid: List[str] = []
        
        for i in range(0, len(self.grid)):    
            row: str = self.grid[i]
            new_row: str = ''
            for j in range(0, len(row)):
                coords: Tuple[int] = (i, j)
                new_cell: str = transition_rule(coords)
                new_row += new_cell

            new_grid += [new_row]

        return new_grid
                
    def cell_transition(
        self, 
        coords: Tuple[int],
        transition_rule: Callable[[Tuple[int]], str]
        ) -> str:
        """Determines the next state of a cell using the transition rule."""
        return transition_rule(coords)

    def transition_rule_1(self, coords: Tuple[int], debug:bool = False) -> str:
        """The cell transition rule for Part 1."""
        adjacent_cell_states: List[str] = self.get_adjacent_cell_states(coords)
        i, j = coords
        state: str = self.grid[i][j]
        if (state == 'L') and (adjacent_cell_states.count('#') == 0):
            # Seat is empty and and no adjacent seat is occupied.
            if debug: print(f'{coords} is {state} and has adjacent seats {adjacent_cell_states} -> #')
            return '#' # Seat becomes occupied.
        
        elif (state == '#') and (adjacent_cell_states.count('#') >= 4):
            # Seat is occupied and at least four adjacent seats are occupied.
            if debug: print(f'{coords} is {state} and has adjacent seats {adjacent_cell_states} -> L') 
            return 'L' # Seat becomes empty.

        else:
            if debug: print(f'{coords} is {state} and has adjacent seats {adjacent_cell_states} -> do nothing')
            return state # Seat state does not change.

    def rule_2(i: int, j: int) -> str:
        """The transition rule for Part 2."""
        return None


    def get_adjacent_cell_states(
        self, 
        coords: Tuple[int], 
        debug: bool = False
        ) -> List[str]:
        """Gets the state of all adjacent 

        Two cells are adjacent if they are immediately up, down, left, right, or 
        diagonal from each other.
        """
        i, j = coords
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
        """Creates a formatted string representing a grid.

        Each row in the grid is indented by spaces of the given indent_length.
        """
        indent = ' ' * indent_length
        return indent + f'\n{indent}'.join(grid)

    def __str__(self):
        """String representation of initial and current grid states."""
        initial_grid: str = f'time=0\n{self.grid_to_str(self.initial_grid)}'
        current_grid: str = f'time={self.time}\n{self.grid_to_str(self.grid)}'
        return f'{initial_grid}\n{current_grid}'\

if __name__ == '__main__':
    main()
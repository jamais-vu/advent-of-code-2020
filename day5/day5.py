from typing import List

def main():

    boarding_passes: List[str]
    with open('input.txt') as input_file:
        boarding_passes = [line.strip() for line in input_file]

    # Each boarding pass is 10 characters:
    # The first 7 characters are either 'F' or 'B' and specify one of 128 rows.
    # - F means front, the lower half of the rows
    # - B means back, the upper half of the rows
    # Last 3 characters are either 'L' or 'R' and specify one of 8 columns.
    # - 'L' means left, the lower half of the columns
    # - 'R' means right, the upper half of the columns
    #
    # We convert these to binary and then find the decimal value.
    seat_ids: List[int] = [
        calculate_seat_id(boarding_pass) for boarding_pass in boarding_passes
    ]

    solution_1: str = f'Part 1: The highest seat ID is {max(seat_ids)}'
    print(solution_1)

    # My boarding pass is the only boarding pass not in the list, and I want 
    # my seat ID
    # Some of the seats at the very front or back don't exist, but my seat is 
    # not at the very front or back, so my seat ID is between the min and max
    # seat IDs. 
    # This means my seat ID is the only number not in that range.
    my_seat_id: List[int] = [
        i for i in range(min(seat_ids), max(seat_ids)+1) if i not in seat_ids
    ]

    solution_2: str = f'Part 2: My seat ID is {my_seat_id.pop()}'
    print(solution_2)

    with open('solution.txt', mode='w') as output_file:
        output_file.write(f'{solution_1}\n{solution_2}')

def calculate_seat_id(boarding_pass: str) -> int:
    """Calculate seat ID by multiplying the row by 8 then adding the column."""
    row: int = int(boarding_pass[0:7].replace('F', '0').replace('B', '1'), 2)
    column: int = int(boarding_pass[7:].replace('L', '0').replace('R', '1'), 2)
    return (row * 8) + column

if __name__ == '__main__':
    main()
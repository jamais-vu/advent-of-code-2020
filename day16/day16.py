import functools
import itertools
import operator
import re

from collections import defaultdict
from typing import Dict, Iterable, List


def main():

    notes: List[str] = []
    with open('input.txt') as input_file:
        notes = input_file.read().split('\n\n')

    fields: List[str] = notes[0].split('\n')

    # Create a dict mapping field names to list of valid ranges for each field.
    ranges: Dict[str, List[Iterable[int]]] = {}
    for field in fields:
        field_name: str = re.match(r'.*(?=:)', field)[0]
        ranges[field_name] = get_field_ranges(field)

    # Create a list of the values on your ticket.
    # First index contains string 'your ticket:', which we don't use.
    your_ticket: List[int] = list(map(int, notes[1].split(',')[1:]))

    # Create a list of lists of the values on each ticket.
    # Zeroth index contains string 'nearby tickets:', which we don't use.
    nearby_tickets: List[List[int]] = [
        get_ticket_values(ticket) for ticket in notes[2].split('\n')[1:]]
    
    # A list of all valid ranges, regardless of field.
    all_valid_ranges: List[Iterable[int]] = list(
        itertools.chain.from_iterable(ranges.values()))
    
    # We find the sum of all invalid values on all tickets, which is the 
    # solution to Part 1.
    # We also create a list of all valid tickets, which is used in Part 2.
    valid_tickets: List[List[int]] = []
    sum_of_invalid_values: int = 0
    for ticket in nearby_tickets:
        invalid_values = is_valid_ticket(ticket, all_valid_ranges)
        sum_of_invalid_values += invalid_values
        if invalid_values == 0:
            # The ticket is valid.
            valid_tickets += [ticket]

    s1: str = f'Part 1: The sum of invalid values is {sum_of_invalid_values}.'
    print(s1)

    ##########
    # Part 2 #
    ##########

    number_of_fields: int = len(fields)
    number_of_valid_tickets: int = len(valid_tickets)

    # Dict mapping column number to all valid field names for that column.
    column_to_field: Dict[int, List[str]] = defaultdict(list)
    for field_name, valid_ranges in ranges.items():
        # print('field_name:   ', field_name)
        # print('valid_ranges: ', valid_ranges)
        for column in range(number_of_fields):
            # print('column number: ', column)
            # print([ticket[column] for ticket in valid_tickets])
            if sum(is_valid_value(ticket[column], valid_ranges) for ticket in valid_tickets) == number_of_valid_tickets:
                column_to_field[column] += [field_name]
                # print(f'column {column} is {field_name}')
            # else:
                # print(f'column {column} is NOT {field_name}')

    # Set of fields for which there is only one column of valid values.
    solved_fields: Set[str] = {
        v[0] for v in column_to_field.values() if len(v) == 1}

    # What we have is some columns which can only be one field. We consider 
    # these fields to be "solved"; they cannot be any other column.
    # Since those columns are set to those fields, we remove those field names 
    # from the other columns, and check again which columns can only be one 
    # field. We repeat this process until each column can only be one field.
    # (This is some sort of contraint problem, but I don't know the name.)
    while len(solved_fields) < number_of_fields:
        for solved_field in solved_fields:
            for column, fields in column_to_field.items():
                if solved_field in fields and len(fields) != 1:
                    column_to_field[column].remove(solved_field)
        solved_fields =  {v[0] for v in column_to_field.values() if len(v) == 1}

    print(column_to_field)

    columns_as_str: str = '\n'.join(sorted(f'{column}: {field_name}' for column, field_name in column_to_field.items()))
    print(columns_as_str)

    # Get values of each field in `your_ticket` which starts with 'departure'.
    starts_with_departure: List[int] =[]
    for column, field_name in column_to_field.items():
        if field_name[0].startswith('departure'):
            print(column, field_name)
            starts_with_departure.append(your_ticket[column])

    # TODO: This gives 337940985703, which AOC says is too low.
    solution_2 = functools.reduce(operator.mul, starts_with_departure)
    s2: str = 'Part 2: The product of the fields on my ticket starting with'\
              f' \'departure\' is {solution_2}.'
    print(s2)


def get_field_ranges(s: str) -> List[Iterable[int]]:
    """Returns a list of all pairs of range values for the field."""
    # List of pairs of ints. Each pair defines inclusive bounds for one range.
    range_bounds: List[List[str]] = [
        map(int, pair.split('-')) for pair in re.findall(r'\d+-\d+', s)
    ]
    # The range's upper bound is `b + 1` because we want `b` to be in the range.
    return [range(a, b + 1) for a, b in range_bounds]


def get_ticket_values(ticket: str) -> List[int]:
    """Returns a list of the given ticket's values, in order of appearance."""
    return [int(n) for n in ticket.split(',')]


def is_valid_value(n: int, valid_ranges: List[Iterable[int]]) -> bool:
    """Checks whether the given integer is within any of the given ranges."""
    for r in valid_ranges:
        if n in r:
            return True
    return False


def is_valid_ticket(values: List[int], valid_ranges: List[Iterable[int]]) -> int:
    """
    Returns 0 if the ticket is valid; otherwise returns sum of invalid fields.
    """
    return sum(n for n in values if not is_valid_value(n, valid_ranges))


if __name__ == '__main__':
    main()
import itertools
import re

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
    your_ticket: List[int] = list(
        map(int, value) for value in notes[1].split('\n')[1:])

    # Create a list of lists of the values on each ticket.
    # Zeroth index contains string 'nearby tickets:', which we don't use.
    nearby_tickets: List[List[int]] = [
        get_ticket_values(ticket) for ticket in notes[2].split('\n')[1:]]
    
    # print(fields, your_ticket, nearby_tickets)

    # A list of all valid ranges, regardless of field.
    all_valid_ranges: List[Iterable[int]] = list(
        itertools.chain.from_iterable(ranges.values()))
    
    sum_of_invalid_values: int = 0
    for ticket in nearby_tickets:
        sum_of_invalid_values += is_valid_ticket(ticket, all_valid_ranges)

    s1: str = f'Part 1: The sum of invalid values is {sum_of_invalid_values}.'
    print(s1)


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
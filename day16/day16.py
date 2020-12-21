import re

from typing import Iterable, List


def main():

    notes: List[str] = []
    with open('input.txt') as input_file:
        notes = input_file.read().split('\n\n')

    fields: List[str] = notes[0].split('\n')
    ranges: List[Iterable[int]] = []
    for field in fields:
        ranges += get_field_ranges(field)
    # print(ranges)

    # First index contains string 'your ticket:', which we don't use.
    your_ticket: List[str] = notes[1].split('\n')[1:]

    # Zeroth index contains string 'nearby tickets:', which we don't use.
    nearby_tickets: List[str] = notes[2].split('\n')[1:]
    
    # print(fields, your_ticket, nearby_tickets)

    sum_of_invalid_values: int = 0
    for ticket in nearby_tickets:
        # print('ticket: ', ticket)
        # print('values: ', get_ticket_values(ticket))
        # print('is_valid_ticket: ', is_valid_ticket(ticket, ranges))
        sum_of_invalid_values += is_valid_ticket(ticket, ranges)

    print(sum_of_invalid_values)


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


def is_valid_value(n: int, ranges: List[Iterable[int]]) -> bool:
    """Checks whether the given integer is within any of the given ranges."""
    for r in ranges:
        if n in r:
            return True
    return False


def is_valid_ticket(ticket: str, ranges: List[Iterable[int]]) -> int:
    """
    Returns 0 if the ticket is valid; otherwise returns sum of invalid fields.
    """
    return sum(n for n in get_ticket_values(ticket) if not is_valid_value(n, ranges))


if __name__ == '__main__':
    main()
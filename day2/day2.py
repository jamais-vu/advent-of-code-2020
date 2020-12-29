import re

from typing import Callable, List, Tuple


def main():
    
    with open('input.txt') as fo:
        passwords = fo.read().split('\n')
    
    solution_1 = solve(passwords, is_valid_part_1)
    s1 = f'Part 1: There are {solution_1} valid passwords.'
    print(s1)

    solution_2 = solve(passwords, is_valid_part_2)
    s2 = f'Part 2: There are {solution_2} valid passwords.'
    print(s2)

    with open('solution2.txt', mode='w') as fo:
        fo.write(f'{s1}\n{s2}')


def tokenize(password_and_constraints: str) -> Tuple[int, int, str, str]:
    """Tokenizes a given password and constraints into a tuple.

    `password_and_constraints` is a string of the form:
        '{a}-{b} {letter}: {password}'
    where `a` and `b` are both integers, `letter` is a string, and `password` is
    a string.
    """
    split_string = re.split(r"[-: ]", password_and_constraints)

    a = int(split_string[0])
    b = int(split_string[1])
    letter = split_string[2]
    # `split_string[3]` is an empty string and not used.
    password = split_string[4]

    return (a, b, letter, password)


def is_valid_part_1(min_count: int, max_count: int, letter: str, 
    password: str) -> bool:
    """
    Checks if a given password meets the constraints of part 1:

    - the count of the letter in the password is within the range defined by 
      the min and max counts. 
    """
    return min_count <= password.count(letter) <= max_count


def is_valid_part_2(position_1: int, position_2: int, letter: str, 
    password: str) -> bool:
    """Checks if a given password meets the constraints of part 2:

    - the given letter appears in the password at one and ONLY one of the given
      positions
    - the given positions do not define the index but the order, i.e. 1 means 
      the first character, 2 means the second character, etc. 

    We use the xor operator (^) to check that the letter appears at one and only
    one position.
    The second constraint is why we subtract 1 from the index when checking.
    """
    return (password[position_1-1] == letter) ^ (password[position_2-1] == letter)


def solve(passwords: List[str], is_valid: Callable[[str], bool]) -> int:
    """Counts the number of valid passwords in the list.

    `is_valid` is a function which determines whether each password is valid.
    There are multiple functions which we may use to determine this.
    """
    count = 0
    for password_and_constraints in passwords:
        # We unpack the results of `tokenize(password_and_constraints)` for
        # calling `is_valid()`.
        if is_valid(*tokenize(password_and_constraints)):
            count += 1
    return count


if __name__ == '__main__':
    main()
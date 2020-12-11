import re

import sys

sys.path.append('..')

from utilities import read_from_file, write_to_file
from typing import Dict, List, Tuple

def main():

    raw_passports: str
    with open('input.txt') as input_file:
        raw_passports = input_file.read()

    # Each passport is separated by two newlines.
    # Each passport itself is a string of fields, separated by a newline or a 
    # space.
    passport_dicts: List[str] = raw_passports_to_dicts(raw_passports)

    # Each field has requirements to be considered valid:
    # 
    #   - byr (Birth Year) - four digits; at least 1920 and at most 2002.
    #   - iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    #   - eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    #   - hgt (Height) - a number followed by either cm or in:
    #       If cm, the number must be at least 150 and at most 193.
    #       If in, the number must be at least 59 and at most 76.
    #   - hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    #   - ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    #   - pid (Passport ID) - a nine-digit number, including leading zeroes.
    #   - cid (Country ID) - ignored, missing or not.
    #
    # Note that a valid passport must have at least 7 fields.

    # We do not include 'cid'.
    fields: List[str] = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    
    solution_part_1: int = 0
    solution_part_2: int = 0
    
    for passport_dict in passport_dicts:
            passport = Passport(passport_dict)
            if passport.is_valid_part_1():
                solution_part_1 += 1
                if passport.is_valid_part_2():
                    solution_part_2 += 1

    s1: str = f'Part 1: There are {solution_part_1} valid passports.'
    s2: str = f'Part 2: There are {solution_part_2} valid passports.'

    print(f'{s1}\n{s2}')
    write_to_file([s1, s2], 'solution.txt')

# TODO: Type hints for this
class Passport:
    def __init__(self, fields: Dict[str, str]):
        self.byr = fields.get('byr', None)
        self.iyr = fields.get('iyr', None)
        self.eyr = fields.get('eyr', None)
        self.hgt = fields.get('hgt', None)
        self.hcl = fields.get('hcl', None)
        self.ecl = fields.get('ecl', None)
        self.pid = fields.get('pid', None)
    
    def is_valid_part_1(self) -> bool:
        """Checks if each Passport field exists."""
        return(
            self.byr and
            self.iyr and
            self.eyr and
            self.hgt and
            self.hcl and
            self.ecl and
            self.pid
        )

    def is_valid_part_2(self) -> bool:
        """Checks if each Passport field satisfies the given constraints.

        Note: Any of validate_byr(), validate_iyr(), or validate_eyr() will 
        throw an error if any of those cannot be cast to int.
        """
        if self.is_valid_part_1():
            return(
                self.validate_byr() and 
                self.validate_iyr() and
                self.validate_eyr() and
                self.validate_hgt() and
                self.validate_hcl() and
                self.validate_ecl() and
                self.validate_pid()
            )
        else:
            return False

    def validate_byr(self) -> bool:
        """A valid birth year is at least 1920 and at most 2002."""
        return 1920 <= int(self.byr) <= 2002

    def validate_iyr(self) -> bool:
        """A valid issue year is at least 2010 and at most 2020."""
        return 2010 <= int(self.iyr) <= 2020

    def validate_eyr(self) -> bool:
        """A valid expieration year is at least 2020 and at most 2030."""
        return 2020 <= int(self.eyr) <= 2030

    def validate_hgt(self) -> bool:
        """A height is valid if it is a number followed by either 'cm' or 'in'.

        If 'cm', the number must be at least 150 and at most 193.
        If 'in', the number must be at least 59 and at most 76.
        """
        m = re.match(r'^(\d{2,3})(cm|in)$', self.hgt)
        if not m:
            return False
        else:
            height: int = int(m.group(1))
            unit: str = m.group(2)
            if unit == 'cm':
                return 150 <= height <= 193
            else:
                return 59 <= height <= 76 

    def validate_hcl(self) -> bool:
        """
        A hair color is valid if it is a '#' followed by exactly six characters.

        The characters must be 0-9 or a-f.
        """
        # Instead of checking length, we could have regex match end of string.
        return (re.match(r'#[0-9a-f]{6}', self.hcl)) and (len(self.hcl) == 7)

    def validate_ecl(self) -> bool:
        """
        An eye color is valid if it is exactly one of:
            'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'
        """
        valid_ecls: List[str] = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        return self.ecl in valid_ecls

    def validate_pid(self) -> bool:
        """A pid is valid if it is a nine-digit number, including leading zeros."""
        return (re.match(r'\d{9}', self.pid)) and (len(self.pid) == 9) 

def raw_passports_to_dicts(raw_passports: str) -> List[Dict[str, str]]:
    """
    Converts a single string representing the input file of passports into a
    list of dictionaries, where each dictionary represents a single passport,
    with keys as field names mapping to each fields' value.
    """
    return [passport_str_to_dict(passport) for passport in raw_passports.split('\n\n')]

def passport_str_to_dict(passport: str) -> Dict[str, str]:
    """Converts a str representing a passport into a dict of passport fields."""

    # A list of strings, where each string represent a field and value in the 
    # passport.
    # For example, the string :
    #  'ecl:gry pid:860033327 eyr:2020 hcl:#fffffd'
    # becomes the list:
    #  ['ecl:gry', 'pid:860033327', 'eyr:2020', 'hcl:#fffffd']
    split_passport: List[str] = re.split(r'[ \n]', passport)

    # A list of pairs of passport fields and their respective values.
    # The above example becomes the list:
    #  [['ecl', gry'], ['pid', '860033327'], ['eyr', '2020'], ['hcl','#fffffd']]
    field_value_pairs: List[List[str]] = [pair.split(':') for pair in split_passport]
    
    # Then each pair is turned into a key:value mapping in a dictionary.
    return {pair[0]:pair[1] for pair in field_value_pairs}

if __name__ == '__main__':
    main()
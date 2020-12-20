import itertools
import re

from typing import Dict, Generator, List, Tuple


def main():

    lines: List[List[str]]
    with open('input.txt') as input_file:
        lines = [line.split(' = ') for line in input_file.read().split('\n')]

    ##########
    # Part 1 #
    ##########

    # Keys: string indices we change. Values: digit we change each index to.
    mask: str = ''

    # Keys: memory addresses. Values: decimal value at each memory address.
    memory: Dict[int, int] = {} 

    for line in lines:
        instruction = line[0]
        value = line[1]

        if instruction == 'mask':
            mask = value

        else:
            # Note that `value` is only a 36-bit binary value if the instruction
            # was 'mask', otherwise it is given as a decimal value.
            binary_value = format(int(value), '036b') # Decimal to 36-bit binary
            address = get_memory_address(instruction)
            new_value = apply_mask(binary_value, mask, 'part 1')
            memory[address] = int(new_value, 2) # Write decimal value to memory

    solution_1: str = sum(memory.values())
    print(solution_1)

    ##########
    # Part 2 #
    ##########

    # Initialize `mask` and `memory` for Part 2.
    mask: str = ''
    memory: Dict[int, int] = {} 
    
    for line in lines:
        instruction = line[0]
        value = line[1]

        if instruction == 'mask':
            mask = value

        else:
            # The memory address is given as a decimal number.
            decimal_address = get_memory_address(instruction)
            # We convert that decimal number to a 36-bit binary number.
            binary_address = format(int(decimal_address), '036b')
            # We apply the mask to that binary number to obtain a new address. 
            # This new address is a 36-bit binary number and may contain 
            # floating bits.
            new_address = apply_mask(binary_address, mask, 'part 2')
            # Given a 36-bit binary address with floating bits, we add the value
            # to each possible address which fits it.
            for possible_address in get_all_memory_addresses(new_address):
                memory[possible_address] = int(value) # Write value to memory

    solution_2: str = sum(memory.values())
    print(solution_2)

    with open('solution.txt', mode='w') as output_file:
        output_file.write(f'Part 1: {solution_1}\nPart 2: {solution_2}')


def get_all_memory_addresses(floating_address: str) -> List[str]:
    """Given an address with floating bits, finds all possible addresses."""
    addresses: List[str] = []

    number_of_floating_bits: int = floating_address.count('X')
    
    # All permutations of '01', no repeats, with lengths equal to the number
    # of floating bits in the address.
    permutations: Generator[Tuple[int], None, None] = itertools.product(
        '01', repeat=number_of_floating_bits)

    # List of all indices in the string `floating_address` where 'X' occurs.
    indices: List[int] = [
        i for i in range(len(floating_address)) if floating_address[i] == 'X'
    ]

    for permutation in permutations:
        addresses += [
            replace_indices(indices, floating_address, list(permutation))]

    return addresses


def replace_indices(indices: List[int], s: str, replacements: List[str]) -> str:
    """
    Replaces the indices of the given string with the replacement characters.
    """
    result: str = ''
    replacements.reverse() # Use this to do replacements in given order.
    
    for i in range(len(s)):
        if i in indices:
            result += replacements.pop()
        else:
            result += s[i]

    return result


def apply_mask(value: str, mask: str, rule: str) -> str:
    """Applies a mask to a 36-bit value, using the rules from part 1 or 2.

    TODO: There's probably a smart bitwise operation solution here.

    Part 1 rules:
        - If the bitmask bit is 0 or 1, the corresponding value bit is 
          overwritten with 0 or 1 respectively.
        - If the bitmask bit is X, the corresponding value bit is unchanged.

    Part 2 rules:
        - If the bitmask bit is 0, the corresponding value bit is unchanged.
        - If the bitmask bit is 1, the corresponding value bit is overwritten 
          with 1.
        - If the bitmask bit is X, the corresponding value bit is floating 
          (written as 'X').
    """
    new_value: str = ''
    
    if rule.lower() == 'part 1':
        for i in range(0, len(mask)):
            if mask[i] == 'X':
                new_value += value[i]
            else:
                new_value += mask[i]
    
    elif rule.lower() == 'part 2':
        for i in range(0, len(mask)):
            if mask[i] == '0':
                new_value += value[i]
            elif mask[i] == '1':
                new_value += '1'
            else:
                new_value += 'X'
    
    return new_value


def get_memory_address(instruction: str) -> str:
    """Gets the memory address n specified by string of form 'mem[n]'."""
    return re.search(r'(?<=mem\[)\d+(?=\])', instruction)[0]


if __name__ == '__main__':
    main()
import re

from typing import Dict, List, Tuple

def main():

    lines: List[List[str]]
    with open('input.txt') as input_file:
        lines = [line.split(' = ') for line in input_file.read().split('\n')]

    print(lines)

    # Keys: memory addresses. Values: decimal value at each memory address.
    memory: Dict[int, int] = {} 

    # Keys: string indices we change. Values: digit we change each index to.
    mask: Dict[int, str] = {}

    for line in lines:
        instruction = line[0]
        value = line[1]

        if instruction == 'mask':
            mask = create_mask(value)
            # print('mask: ', mask)

        else:
            binary_value = format(int(value), '036b') # Decimal to 36-bit binary
            address = get_memory_address(instruction)
            # print(f'memory address: {address}\nvalue:     {binary_value}')
            new_value = apply_mask(binary_value, mask)
            # print(f'new value: {new_value}')
            # print(f'decimal:   {int(new_value, 2)}')
            memory[address] = int(new_value, 2) # Write decimal value to memory.

    print(memory)
    print(sum(memory.values()))


def create_mask(mask_as_str: str) -> Dict[int, str]:
    """TODO docstring"""
    mask: Dict[int, int] = {}
    for i in range(len(mask_as_str) - 1, -1, -1):
        if mask_as_str[i] != 'X':
            mask[i] = mask_as_str[i]
    return mask

def apply_mask(value: str, mask: str) -> str:
    """TODO docstring"""
    for index, digit in mask.items():
        value = value[0:index] + digit + value[index + 1:]
    return value

def get_memory_address(instruction: str) -> int:
    """Gets the memory address n specified by string of form 'mem[n]'."""
    return re.search(r'(?<=mem\[)\d+(?=\])', instruction)[0]

if __name__ == '__main__':
    main()
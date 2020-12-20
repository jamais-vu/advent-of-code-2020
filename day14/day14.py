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
    mask: str = ''

    for line in lines:
        instruction = line[0]
        value = line[1]

        if instruction == 'mask':
            mask = value

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

def apply_mask(value: str, mask: str) -> str:
    """TODO docstring"""
    new_value: str = ''
    for i in range(0, len(mask)):
        if mask[i] == 'X':
            new_value += value[i]
        else:
            new_value += mask[i]
    return new_value

def get_memory_address(instruction: str) -> int:
    """Gets the memory address n specified by string of form 'mem[n]'."""
    return re.search(r'(?<=mem\[)\d+(?=\])', instruction)[0]

if __name__ == '__main__':
    main()
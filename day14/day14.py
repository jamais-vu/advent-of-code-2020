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

    ##########
    # Part 1 #
    ##########
    for line in lines:
        instruction = line[0]
        value = line[1]

        if instruction == 'mask':
            mask = value

        else:
            binary_value = format(int(value), '036b') # Decimal to 36-bit binary
            address = get_memory_address(instruction)
            # print(f'memory address: {address}\nvalue:     {binary_value}')
            new_value = apply_mask(binary_value, mask, 'part 1')
            # print(f'new value: {new_value}')
            # print(f'decimal:   {int(new_value, 2)}')
            memory[address] = int(new_value, 2) # Write decimal value to memory.

    print(memory)
    print(sum(memory.values()))

    ##########
    # Part 2 #
    ##########
    for line in lines:
        instruction = line[0]
        value = line[1]


def apply_mask(value: str, mask: str, rule: str) -> str:
    """Applies a mask to a 36-bit value, using the rules from part 1 or 2.

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


def get_memory_address(instruction: str) -> int:
    """Gets the memory address n specified by string of form 'mem[n]'."""
    return re.search(r'(?<=mem\[)\d+(?=\])', instruction)[0]

if __name__ == '__main__':
    main()
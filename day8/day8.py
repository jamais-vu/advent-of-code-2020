from typing import List, Set

def main():

    input_text: List[str]
    with open('input.txt') as input_file:
        input_text = input_file.read().split('\n')

    solution_1: int = execute_code(input_text)
    s1: str = f'Part 1: The value of the accumulator is {solution_1}'

    print(s1)
    
    with open('solution.txt', mode='w') as output_file:
        output_file.write(s1)

def execute_code(code: List[str]) -> int:
    """TODO"""
    accumulator: int = 0
    # Line numbers of code we have already executed.
    already_executed: Set(int) = set() 

    i: int = 0

    while i not in already_executed:

        already_executed.add(i)

        instruction, value = code[i].split()
        value = int(value)
        
        if instruction == 'acc':
            # Increment the accumulator by the specified value
            accumulator += value
            i += 1
        
        if instruction == 'jmp':
            # We subtract 1 because i is incremented by 1 in each iteration of 
            # the for loop and we don't want to double-count.
            # For example, 'jmp +1' continues to the insturction immediately
            # below it, so setting `i += 1` would increment `i` by 1, then the
            # for loop increments `i` by 1 again, which means we actually
            # execute the instruction at code[i+2] rather than code[i+1]. 
            i += value

        if instruction == 'nop':
            i += 1 # nop stands for No OPeration. Next instruction is executed.

    return accumulator

if __name__ == '__main__':
    main()
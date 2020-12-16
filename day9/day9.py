import itertools

from typing import List

def main():

    numbers: List[int]
    with open('input.txt') as input_file:
        numbers = list(map(int, input_file.read().split('\n')))

    n: int = 25
    # Start at index n+1 to only check numbers after the first n.
    i: int = n + 1 
    # Sums of all pairs of the previous n numbers.
    sums: List[int] = list(map(sum, itertools.combinations(numbers[i-n:i], 2)))

    # ###### #
    # Part 1 #
    # ###### #
    while numbers[i] in sums:
        i += 1
        sums = list(map(sum, itertools.combinations(numbers[i-n:i], 2)))

    solution_1: int = numbers[i]
    s1: str = f'Part 1: {solution_1} is the first number which is not the sum'\
        f' of any two of the previous {n} numbers.'
    print(s1)

    # ###### #
    # Part 2 #
    # ###### #

    invalid_number: int = solution_1
    invalid_index: int = i

    # Since we know the invalid number is not the sum of any two numbers in the
    # previous n numbers, we start by checking if it is the sum of any three
    # contiguous numbers in the list.
    #
    # Note: Do we need to check if it's sum of any two numbers before the 
    # previous n? We'll be checking if it's the sum of any three in the total
    # preceding list, just in case.
    slice_length: int = 3
    contiguous_slice: List[int] = numbers[0:slice_length]
    
    while sum(contiguous_slice) != invalid_number:
        
        for i in range(0, invalid_index - slice_length):
            contiguous_slice = numbers[i:i+slice_length]
            
            if sum(contiguous_slice) == invalid_number:
                break

        slice_length += 1

    solution_2: str = min(contiguous_slice) + max(contiguous_slice)
    s2: str = f'Part 2: The sum of the smallest and largest numbers in the'\
        f' contiguous slice is {solution_2}.'
    print(s2)

    with open('solution.txt', mode='w') as output_file:
        output_file.write(f'{s1}\n{s2}')

if __name__ == '__main__':
    main()
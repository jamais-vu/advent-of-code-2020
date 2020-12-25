import itertools

from typing import List


def main():

    cups: List[int] = []
    with open('input.txt') as input_file:
        cups = list(map(int, input_file.read()))

    # We need a way to include slices which "wrap around", e.g. 
    # We can use modular arithmetic, for example if 
    # 
    # >>> li = list(range(10))
    # >>> li
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # >>> len(li)
    # 10
    # >>> res = [li[i % len(li)] for i in range(8, 11)]
    # >>> res
    # [8, 9, 0]

    length: int = len(cups)

    # We start by selecting the first cup in the list as the current cup.
    i: int = 0

    for move in range(1, 101): 
        current_cup: int = cups[i]
        print(f'\n-- move {move} --')
        print('cups: ' + ' '.join(map(str, cups[0:i])) + f' ({cups[i]}) '\
                           + ' '.join(map(str, cups[i+1:])))
        
        # The current cup has index i. We pick up the three cups to the right.
        picked_indices = list(map(lambda x: x % length, range(i + 1, i + 4)))
        picked_up: List[int] = [cups[j % length] for j in picked_indices]
        print(f'pick up:  {", ".join(map(str, picked_up))}')
        
        # We then consider the list of cups with the picked_up cups removed.
        cups = [cup for j, cup in enumerate(cups) if j not in picked_indices]
        # print(f'new cups: {", ".join(map(str, cups))}')
        
        # Find the destination cup.
        # We find the cup with the highest value less than the current cup; if no
        # such cup exists, then the destination cup is the cup with the highest 
        # value in the entire list.
        destination_cup: int = 0
        less_than_current_cup: List[int] = [cup for cup in cups if cup < current_cup]
        # print('less_than_current_cup', less_than_current_cup)
        if less_than_current_cup:
            destination_cup = max(less_than_current_cup)
        else:
            destination_cup = max(cups)

        print(f'destination: {destination_cup}')
        # We insert the picked up cups to the right of the destination cup
        insertion_index = (cups.index(destination_cup) + 1) % length
        for cup in reversed(picked_up):
            cups.insert(insertion_index, cup)

        # The new current cup is immediately to the right of the current cup.
        i = (cups.index(current_cup) + 1) % length

    print('\n-- final --')
    print('cups:' + ' '.join(map(str, cups[0:i])) + f' ({cups[i]}) ' 
          + ' '.join(map(str, cups[i+1:])))

    # We collect the cups' labels in order, starting after the cup with value 1.
    index_of_1: int = cups.index(1)
    in_order: List[int] = [cups[i % length] for i in range(index_of_1 + 1, index_of_1 + 1 + length)]
    # For some reason we don't include 1 in this. That's what the problem says.
    solution_1: str = ''.join(map(str, in_order[:-1]))
    print(solution_1)

if __name__ == '__main__':
    main()
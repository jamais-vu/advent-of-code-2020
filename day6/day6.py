import re
 
from typing import List, Set

def main():

    with open('input.txt') as input_file:
        # Each group is separated by two newlines, so we split up into a list
        # of strings, with each string being a full group's answers.
        groups: List[str] = re.split(r'\n{2}', input_file.read())

    # Each person within a group has their answer separated by one newline,
    # so after splitting by group, we split by person.
    # `answers[i][j]` is the answers for the jth person in the ith group.
    answers: List[List[str]] = [group.split('\n') for group in groups]

    group_unions: List[Set[str]] = []
    group_intersections: List[Set[str]] = []
    for group in answers:

        # Each group is a List[str] of each person's answers.
        # We create a List[Set[str]] the sets of each person's answer.
        group_answers_as_sets: List[Set[str]] = [set(person) for person in group]

        # Then, for the whole group, we take the union of answers, and the 
        # intersection of answers.
        group_unions +=  set.union(*group_answers_as_sets)
        group_intersections += set.intersection(*group_answers_as_sets)

    # Obtain the sum of the number of characters in each set of group answers.
    solution_1: int = sum(len(union) for union in group_unions)
    solution_2: int = sum(len(intersection) for intersection in group_intersections)
    
    s1: str = f'Part 1: The sum of the counts is {solution_1}.'
    s2: str = f'Part 2: The sum of the counts is {solution_2}.'
    
    print(f'{s1}\n{s2}')

    with open('solution.txt', mode='w') as output_file:
        output_file.write(f'{s1}\n{s2}')

if __name__ == '__main__':
    main()
import re
 
from typing import List, Set

def main():

    answers: List[List[str]]
    with open('input.txt') as input_file:
        # Each group is separated by two newlines, so we split up into a list
        # of strings, with each string being a full group's answers.
        # Each person within a group has their answer separated by one newline,
        # so after splitting by group, we split by person.
        # 
        #Example: 
        #   answers[i][j] is the answers for the jth person in the jth group.
        groups = re.split(r'\n{2}', input_file.read())

    answers = [group.split('\n') for group in groups]

    print(answers[0:10])

    # Convert each combined group answer string into a set of the characters.
    group_unions: List[Set[str]] = []
    for group in answers:
        group_unions +=  set.union(*[set(person) for person in group])

    # Obtain the sum of the number of characters in each set of group answers.
    solution = sum(len(union) for union in group_unions)
    
    print(solution)
    

if __name__ == '__main__':
    main()
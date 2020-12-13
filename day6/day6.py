import re
 
from typing import List, Set

def main():

    answers: List[str]
    with open('input.txt') as input_file:
        # Each group is separated by two newlines, so we split up into a list
        # of strings, with each string being a full group's answers.
        # Each person within a group has their answer separated by one newline,
        # after splitting by group, we remove single newlines.
        answers = [s.replace('\n', '') for s in re.split(r'\n{2}', input_file.read())]

    # Convert each combined group answer string into a set of the characters.
    answer_sets: List[Set[str]] = [set(answer) for answer in answers]

    # Obtain the sum of the number of characters in each set of group answers.
    solution = sum(len(answer_set) for answer_set in answer_sets)
    
    print(solution)
    

if __name__ == '__main__':
    main()
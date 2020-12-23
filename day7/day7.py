import re

from collections import defaultdict
from typing import DefaultDict, Dict, Iterable, List, Set

def main():

    input_text: List[str]
    with open('input.txt') as input_file:
        input_text = input_file.read().split('\n')

    bags: DefaultDict[str, Set[str]] = defaultdict(set)
    for line in input_text:
        # Split up the line into a List[str] of the outer bag, followed by
        # the number and colors of bags it contains, if any.
        split_line = list(filter(None, re.split(r' bags?[,.]? ?|contain ', line)))
        outer_bag = split_line[0]

        # We skip if the container bag contains no bags.
        # if split_line[1] == 'no other'
        if split_line[1] != 'no other':            
            for bag in split_line[1:]:
                # Split up the string into number and color of contained bag.
                number, inner_bag = re.split(r'(?<=\d) ', bag)                
                bags[outer_bag].add(inner_bag)

    path_exists: Dict[str, List[str]] = {}
    for bag in bags.keys():
        path_exists[bag] = find_path(bags, bag, 'shiny gold')

    valid_paths = [path for path in path_exists.values() if path is not None] 

    # We subtract 1 from the answer because `['shiny gold']` is a valid path,
    # but we want only paths which start with a different color bag.
    solution_1: str = f'Part 1: {len(valid_paths) - 1}.'
    print(solution_1)

    ##########
    # Part 2 #
    ##########
    # Outer dict mapping bag colors to an inner dict of contained bags and their
    # quantity.
    bags: DefaultDict[str, Dict[str, int]] = defaultdict(dict)
    for line in input_text:
        # Split up the line into a List[str] of the outer bag, followed by
        # the number and colors of bags it contains, if any.
        split_line = list(filter(None, re.split(r' bags?[,.]? ?|contain ', line)))
        outer_bag = split_line[0]

        # We skip if the container bag contains no bags.
        # if split_line[1] == 'no other'
        if split_line[1] != 'no other':            
            for bag in split_line[1:]:
                # Split up the string into number and color of contained bag.
                number, inner_bag = re.split(r'(?<=\d) ', bag)   
                # We merge the two dicts             
                bags[outer_bag] = {**bags[outer_bag], **{inner_bag:int(number)}}

    explored: List[str] = [] # List of all bags nested within shiny gold
    queue: List[str] = [] # List of bags we check nestings of
    color: str
    quantity: int
    for color, quantity in bags['shiny gold'].items():
        queue += [color] * quantity

    while queue:
        bag: str = queue.pop()
        explored.append(bag)
        for color, quantity in bags[bag].items():
            queue += [color] * quantity

    solution_2: str = f'Part 2: {len(explored)}.'
    print(solution_2)

    with open('solution.txt', mode='w') as output_file:
        output_file.write(f'{solution_1}\n{solution_2}')


def find_path(
    graph: Dict[str, Iterable[str]], 
    start_node: str, 
    end_node: str, 
    path: List[str] = [], 
    indent: int = -1, 
    debug: bool = False
    ) -> List[str]:
    """Finds a path from the start node to the end node in the given graph."""
    indent = indent + 1
    spaces = '  ' * indent
    if debug:
        print(spaces, 'start_node: ', start_node)
        print(spaces, 'end_node: ', end_node)
        print(spaces, 'path: ', path)
    path: List[str]  = path + [start_node]
    if debug:
        print(spaces, 'path = path + [start_node]: ', path)
    
    if start_node == end_node:
        if debug:
            print(spaces, '\tstart_node == end_node\n\treturning path', end='\n\n')
        return path

    # `graph` only contains keys for nodes with edges to other nodes, so a node 
    # with no outgoing edges is not in `graph`.
    elif start_node not in graph:
        if debug:
            print(f'{spaces}\tstart_node "{start_node}" not in graph\n\treturning None', end='\n\n')
        return None
    
    else:
        if debug:
            print(spaces, 'graph[start_node]: ', graph[start_node])
        for node in graph[start_node]:
            if node not in path:
                if debug:
                    print(f'{spaces}\tnode "{node}" not in path, calling find_path()', end='\n\n')
                new_path: List[str] = find_path(graph, node, end_node, path, indent)
                if new_path:
                    return new_path
            else:
                if debug:
                    print(f'{spaces}\tnode "{node}" in path\n\treturning None', end='\n\n')
                return None


if __name__ == '__main__':
    main()
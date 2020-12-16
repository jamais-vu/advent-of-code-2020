import pprint
import re
import traceback

from collections import defaultdict
from typing import DefaultDict, List, Set

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

    # print('path_exists:', pprint.pformat(path_exists), end='\n\n')

    valid_paths = [path for path in path_exists.values() if path is not None] 
    # print('valid paths:\n', pprint.pformat(valid_paths))

    # We subtract 1 from the answer because `['shiny gold']` is a valid path,
    # but we want only paths which start with a different color bag.
    print(f'[\'shiny gold\'] in valid_paths: {["shiny gold"] in valid_paths}')
    print('number of valid paths: ', len(valid_paths) - 1)   

def find_path(
    graph: DefaultDict[str, Set[str]], 
    start_node: str, 
    end_node: str, 
    path: List[str] = [], 
    indent: int = -1, 
    debug: bool = False):
    """TODO"""
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


# def find_paths(
#     bags: DefaultDict[str, Set[str]], 
#     color: str,
#     path: List[str] = []
#     ) -> List[str]:
#     """
#     Recursive method of finding all possible nestings of bags containing given color.

#     TODO
#     """
#     print('\ncalled `find_paths()`')
#     print('color: ', color)
#     print('path: ', path)

#     path += [color]
#     if color not in bags:
#         print('color NOT in bags: ', color)
#         return path    
#     else:
#         print(f'color \'{color}\' is contained in {bags[color]}')

#         paths = []

#         for container_bag_color in bags[color]:
#             print('container_bag_color: ', container_bag_color)
            
#             if color not in path:

#                 try:
#                     paths += find_paths(bags, container_bag_color, path, paths)
                
#                 except TypeError as e:
#                     print(f'\n{traceback.format_exc()}\nVALUES:')
#                     print('bags: ', pprint.pformat(bags))
#                     print('container_bag_color: ', container_bag_color)
#                     print('path: ', path)
#                     print('paths: ', pprint.pformat(paths))        
        
#         return paths


if __name__ == '__main__':
    main()
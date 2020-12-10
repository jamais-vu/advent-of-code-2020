# Some functions I reuse across several days. 

# To import this into a specific day, it is necessary to add the parent 
# directory, which `utilities.py` resides in, to the PYTHONPATH.
#
#   import sys
#   sys.path.append('..')
#   import utilities
# 
# Why not `import ..utilities`? Because it throws
#   ValueError: attempted relative import beyond top-level package

import os

def write_to_file(
        line_list,
        output_file,
        check_before_write = True,
        verbose = True):
    """Opens and writes a list of strings to the given file, in indexed order.

    Parameters:
        line_list : List[str]
            A list of strings.
        output_file : str
            The name of the file to write to.
        check_before_write : bool
            Whether to check if the file already exists. If the file exists, 
            the user will be prompted whether to overwrite the file.
        verbose : bool
            Whether to print additional details as the function executes.
    """
    if (check_before_write) and (os.path.exists(output_file)):
        # Warns the user the file they are trying to write to already exists, 
        # and asks if they want to overwrite it.
        print(f'\'{output_file}\' already exists. Enter Y to overwrite it; '
              ' any other key to skip.')
        user_choice = input()
        if user_choice[0].lower() != 'y': 
            print(f'Skipping \'{output_file}\'\n')
            return None
    
    if verbose: 
        print(f'Writing to \'{output_file}\'.')
    
    with open(output_file, mode='w', encoding='utf8') as fo:
        # Join `line_list` with newlines so it doesn't write all on one line
        fo.write('\n'.join(line_list))
    
    if verbose: 
        print('Write complete.\n')
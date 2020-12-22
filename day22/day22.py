from typing import List


def main():

    decks: List[str] = []
    with open('example_1.txt') as input_file:
        decks = input_file.read().split('\n\n')

    # We ignore the zeroth index because that only contains the player.
    deck_1: List[str] = [line for line in decks[0].split('\n')[1:]]
    deck_2: List[str] = [line for line in decks[1].split('\n')[1:]]


if __name__ == '__main__':
    main()
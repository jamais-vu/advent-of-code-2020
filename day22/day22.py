from collections import deque
from typing import Deque, List


def main():

    decks: List[str] = []
    with open('example_1.txt') as input_file:
        decks = input_file.read().split('\n\n')

    # We ignore the zeroth index because that only contains the player.
    # We use collections.deque because it has O(1) complexity for appending
    # and popping at both ends.
    deck_1: Deque[int] = deque(int(line) for line in decks[0].split('\n')[1:])
    deck_2: Deque[int] = deque(int(line) for line in decks[1].split('\n')[1:])

    number_of_rounds: int = 0
    while len(deck_1) > 0 and len(deck_2) > 0:
        # print(f'\n-- Round {number_of_rounds} --')
        play_round(deck_1, deck_2)
        number_of_rounds += 1

    print(f'Number of rounds: {number_of_rounds}')

    winning_deck: Deque[int] = deque()
    if len(deck_1) == 0:
        winning_deck = deck_2
    else:
        winning_deck = deck_1

    score: int = sum((i + 1) * v for i, v in enumerate(reversed(winning_deck)))
    
    print(score)


def play_round(deck_1: Deque[int], deck_2: Deque[int], verbose=False) -> None:
    """TODO docstring"""
    if verbose: print(f'Player 1\'s deck: {deck_1}\nPlayer 2\'s deck: {deck_2}')
    
    card_1: int = deck_1.popleft()
    card_2: int = deck_2.popleft()
    
    if verbose: print(f'Player 1 plays: {card_1}\nPlayer 2 plays: {card_2}')

    if card_1 > card_2:
        if verbose: print('Player 1 wins the round!')
        deck_1.extend([card_1, card_2]) # Add greater card first

    elif card_1 < card_2:
        if verbose: print('Player 2 wins the round!')
        deck_2.extend([card_2, card_1]) # Add greater card first


if __name__ == '__main__':
    main()
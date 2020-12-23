import itertools

from collections import deque
from typing import Deque, List, Set


def main():

    decks: List[str] = []
    with open('input.txt') as input_file:
        decks = input_file.read().split('\n\n')

    # We ignore the zeroth index because that only contains the player.
    # We use collections.deque because it has O(1) complexity for appending
    # and popping at both ends.
    deck_1: Deque[int] = deque(int(line) for line in decks[0].split('\n')[1:])
    deck_2: Deque[int] = deque(int(line) for line in decks[1].split('\n')[1:])

    ##########
    # Part 1 #
    ##########
    number_of_rounds: int = 0
    while len(deck_1) > 0 and len(deck_2) > 0:
        play_round(deck_1, deck_2)
        number_of_rounds += 1

    print(f'Number of rounds: {number_of_rounds}')

    winning_deck: Deque[int] = deque()
    if len(deck_1) == 0:
        winning_deck = deck_2
    else:
        winning_deck = deck_1

    s1: int = sum((i + 1) * v for i, v in enumerate(reversed(winning_deck)))
    
    print(f'Part 1: {s1}')

    ##########
    # Part 2 #
    ##########
    # Slow and messy but works.
    deck_1: Deque[int] = deque(int(line) for line in decks[0].split('\n')[1:])
    deck_2: Deque[int] = deque(int(line) for line in decks[1].split('\n')[1:])

    play_recursive_game(deck_1, deck_2, verbose = False)

    winning_deck: Deque[int] = deque()
    if len(deck_1) == 0:
        winning_deck = deck_2
    else:
        winning_deck = deck_1

    s2: int = sum((i + 1) * v for i, v in enumerate(reversed(winning_deck)))
    
    print(f'Part 2: {s2}')

    with open('solution.txt', mode='w') as output_file:
        output_file.write(f'Part 1: {s1}\nPart 2: {s2}')


def play_recursive_game(
    deck_1: Deque[int], 
    deck_2: Deque[int], 
    number_of_games: int = 1, 
    verbose: bool = True) -> int:
    """TODO docstring"""
    if verbose: print(f'\n=== Game {number_of_games} ===')
    # To track previously-played rounds, we add `str(deck_1) + str(deck_2)` to
    # the set previously_played. This is hashable, and preserves both the card
    # orders and which decks they were in. 
    previously_played : Set[str] = set()
    number_of_rounds: int = 0
    while len(deck_1) > 0 and len(deck_2) > 0:
        if str(deck_1) + str(deck_2) in previously_played:
            if verbose: print('previously played!')
            return 1
        else:
            previously_played.add(str(deck_1) + str(deck_2))
            number_of_rounds += 1
            play_recursive_round(deck_1, deck_2, number_of_games, number_of_rounds, verbose=verbose)

    if len(deck_1) == 0:
        return 2
    else:
        return 1



def play_recursive_round(
    deck_1: Deque[int], 
    deck_2: Deque[int], 
    number_of_games: int,
    number_of_rounds: int,
    verbose: bool = True) -> None:
    """TODO docstring

    Mutates deck_1 and deck_2.
    """
    if verbose: 
        print(f'\n-- Round {number_of_rounds} (Game {number_of_games}) --')
        print(f'Player 1\'s deck: {", ".join(str(x) for x in deck_1)}'\
              f'\nPlayer 2\'s deck: {", ".join(str(x) for x in deck_2)}')
    
    card_1: int = deck_1.popleft()
    card_2: int = deck_2.popleft()
    
    if verbose: print(f'Player 1 plays: {card_1}\nPlayer 2 plays: {card_2}')

    if (card_1 <= len(deck_1)) and (card_2 <= len(deck_2)):
        # If both players have at least as many cards remaining in their deck
        # as the value of the card they drew, they play a new recursive game.
        
        if verbose: print('Playing a sub-game to determine the winner...')
        
        # The sub-game is played with the first n cards of each deck, where
        # n is equal to the card just drawn. 
        new_deck_1: Deque[int] = deque(itertools.islice(deck_1, 0, card_1))
        new_deck_2: Deque[int] = deque(itertools.islice(deck_2, 0, card_2))
        winner = play_recursive_game(new_deck_1, new_deck_2, 
                                     number_of_games + 1, verbose)

        if winner == 1:
            if verbose: 
                print(f'Player 1 wins round {number_of_rounds}'\
                      f' of game {number_of_games}!')
                print('\n\n...anyway, back to game {number_of_games}.')
            deck_1.extend([card_1, card_2]) # Add winner's card first

        elif winner == 2:
            if verbose: 
                print(f'Player 2 wins round {number_of_rounds}'\
                      f' of game {number_of_games}!')
                print('\n\n...anyway, back to game {number_of_games}.')
            deck_2.extend([card_2, card_1]) # Add winner's card first

    else:
        if card_1 > card_2:
            if verbose: 
                print(f'Player 1 wins round {number_of_rounds}'\
                      f' of game {number_of_games}!')
            deck_1.extend([card_1, card_2]) # Add greater card first

        elif card_1 < card_2:
            if verbose: 
                print(f'Player 2 wins round {number_of_rounds}'\
                      f' of game {number_of_games}!')
            deck_2.extend([card_2, card_1]) # Add greater card first


def play_round(deck_1: Deque[int], deck_2: Deque[int], verbose=False) -> None:
    """TODO docstring

    Mutates deck_1 and deck_2.
    """
    if verbose: 
        print(f'Player 1\'s deck: {", ".join(str(x) for x in deck_1)}'\
              f'\nPlayer 2\'s deck: {", ".join(str(x) for x in deck_2)}')
    
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
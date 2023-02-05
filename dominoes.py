import random


def shuffled_full_set():
    """It creates 28 dominoes and put them in random order"""
    full_set = [[i, y] for y in range(0, 7) for i in range(y, 7)]
    random.shuffle(full_set)
    return full_set


def first_domino(game_set):
    """Function checks the set and return the highest double or [-1, -1], if there aren't double."""
    for i in range(6, 0, -1):
        if [i, i] in game_set:
            return [i, i]
    return [-1, -1]


def first_turn(player, computer):
    """Choose the highest double in sets and return it.
    Return turn index to determine who's going to have the first move
    :return highest double domino, turn_index"""
    if first_domino(player) > first_domino(computer):
        return [first_domino(player)], 1
    elif first_domino(player) < first_domino(computer):
        return [first_domino(computer)], 0
    else:
        return 0, 0


def info_output(stock, player, computer, snake, turn_index):
    """Output of information during the game"""
    status = ['It\'s your turn to make a move. Enter your command.',
              'Computer is about to make a move. Press Enter to continue...',
              'The game is over. The computer won!',
              'The game is over. You won!',
              "The game is over. It's a draw!"]
    print('=' * 70)
    print('Stock size:', len(stock))
    print('Computer pieces:', len(computer), '\n')
    # snake output, contracted when there are more than 6 elements
    if len(snake) <= 6:
        for i in range(0, len(snake)):
            print(snake[i], end='')
    else:
        print(snake[0], snake[1], snake[2], '...', snake[len(snake) - 3], snake[len(snake) - 2], snake[len(snake) - 1])
    # put players domino's pieces into column
    print('\n\nYour pieces:')
    for i in range(0, len(player)):
        print(f'{i + 1}:{player[i]}')
    print('\nStatus:', status[turn_index])


def removing(snake, game_set):
    """Piece removing from set"""
    for i in range(0, len(snake)):
        try:
            game_set.remove(snake[i])
        except ValueError:
            continue
    return game_set


def player_turn(player):
    while True:
        try:
            choice = int(input())
        except ValueError:
            print('Invalid input. Please try again.')
            continue
        if choice not in range(-len(player), len(player) + 1):
            print('Invalid input. Please try again.')
            continue
        if choice == 0:
            return 'stock', 1
        domino = player[abs(choice) - 1]
        side = int(choice / abs(choice))  # Receiving 1 or -1
        return domino, side


def add_from_stock(game_set, stock):
    if len(stock) == 0:
        return game_set, stock
    game_set.append(stock.pop(0))
    return game_set, stock


def add_to_snake(snake, domino, side):
    if side > 0 and snake[len(snake) - 1][1] == domino[0]:
        snake.append(domino)
    elif side > 0 and snake[len(snake) - 1][1] == domino[1]:
        domino.reverse()
        snake.append(domino)
    elif side < 0 and snake[0][0] == domino[0]:
        domino.reverse()
        snake.insert(0, domino)
    elif side < 0 and snake[0][0] == domino[1]:
        snake.insert(0, domino)
    else:
        print('Illegal move. Please try again.')
        return 'illegal move'


def turn(game_set, stock, snake, turn_index):
    while True:
        if turn_index == 0:
            domino, side = player_turn(game_set)
        else:
            domino, side = computer_turn(game_set, snake)
        if domino == 'stock':
            add_from_stock(game_set, stock)
            return game_set
        if add_to_snake(snake, domino, side) == 'illegal move':
            continue
        game_set.remove(domino)
        break


def computer_turn(computer, snake):
    input()
    # counting of numbers
    quantity = []
    for digit in range(7):
        quantity.append(sum(domino.count(digit) for domino in snake) + sum(domino.count(digit) for domino in computer))
    # evaluation of each domino and sorting
    scores = []
    for i in range(len(computer)):
        scores.append((computer[i], quantity[computer[i][0]] + quantity[computer[i][1]]))
    scores.sort(key=lambda score:score[1], reverse=True)
    scores = [scores[i][0] for i in range(0, len(scores))]
    # checking of turn possibility
    for domino in scores:
        for side in [-1, 1]:
            if side > 0 and snake[len(snake) - 1][1] == domino[0]:
                return domino, side
            elif side > 0 and snake[len(snake) - 1][1] == domino[1]:
                return domino, side
            elif side < 0 and snake[0][0] == domino[0]:
                return domino, side
            elif side < 0 and snake[0][0] == domino[1]:
                return domino, side
    return 'stock', 1


def domino_checker(snake, game_set):
    """The opportunity to put a domino is checked"""
    marker = [i for i in game_set for j in [0, 1] if snake[0][0] == i[j] or snake[len(snake) - 1][1] == i[j]]
    if marker:
        return True


def win_condition(snake, player, computer, stock, turn_index):
    if not computer or not player:
        return False, 'winner'
    if  len(snake) > 3:
        counter = sum(domino.count(snake[0][0]) for domino in snake)
        if counter == 8:
            return False, 'draw'
    if len(stock) == 0 and not domino_checker(snake, computer) and turn_index == 1:
        return False, 'winner'
    if len(stock) == 0 and not domino_checker(snake, player) and turn_index == 0:
        return False, 'winner'
    return True, 'continue'


def main():
    instructions = '\nYOUR TURN: \
                    \nDomino reverses on its own.\
                    \nPrint the number of the domino you want to play.\
                    \nUse "-" to move the domino to the left.\
                    \nPrint "0" to get one from the stock.'

    # Start of the game: shuffling, first turn and output
    while True:
        #  Dominoes splitting
        stock = shuffled_full_set()
        players_set = stock[:7]
        computers_set = stock[7:14]
        stock = stock[14:]
        #  First turn
        snake, turn_index = first_turn(players_set, computers_set)
        if not snake:
            continue
        if turn_index == 1:
            removing(snake, players_set)
        else:
            removing(snake, computers_set)
        info_output(stock, players_set, computers_set, snake, turn_index)
        break
    # The main part of the game
    text_flag = True
    flag = True
    while flag:
        if turn_index == 0 and text_flag:
            print(instructions)
            text_flag = False
        if turn_index == 0:
            turn(players_set, stock, snake, turn_index)
            turn_index = 1
        else:
            turn(computers_set, stock, snake, turn_index)
            turn_index = 0
        flag, draw_checker = win_condition(snake, players_set, computers_set, stock, turn_index)
        if draw_checker == 'winner':
            turn_index += 2 # to get a win message
        elif draw_checker == 'draw':
            turn_index = 4
        info_output(stock, players_set, computers_set, snake, turn_index)


if __name__ == '__main__':
    main()

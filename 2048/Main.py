from datetime import datetime
from GameBoard import GameBoard
from Agent import Agent
from Expectimax_Agent import ExpectimaxAgent

def check_win(board: GameBoard):
    return board.get_max_tile() >= 2048


int_to_string = ['UP', 'DOWN', 'LEFT', 'RIGHT']

if __name__ == '__main__':
    agent: Agent
    board: GameBoard
    # Configuracion final: Expectimax profundidad 3 con preset "smooth_heavy" probado en bench.
    SMOOTH_WEIGHTS = {
        "empty": 280,
        "monotonicity": 2.2,
        "corner": 25,
        "smoothness": 4.0,
        "merges": 50,
    }
    agent = ExpectimaxAgent(depth=3, weights=SMOOTH_WEIGHTS)
    board = GameBoard()
    done = False
    moves = 0
    board.render()
    start = datetime.now()
    while not done:
        action = agent.play(board)
        print('Next Action: "{}"'.format(
            int_to_string[action]), ',   Move: {}'.format(moves))
        done = board.play(action)
        done = done or check_win(board)
        board.render()
        moves += 1

    print('\nTotal time: {}'.format(datetime.now() - start))
    print('\nTotal Moves: {}'.format(moves))
    if check_win(board):
        print("WON THE GAME!!!!!!!!")
    else:
        print("BOOOOOOOOOO!!!!!!!!!")

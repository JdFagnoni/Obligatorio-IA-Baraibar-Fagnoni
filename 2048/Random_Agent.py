import numpy as np

from Agent import Agent
from GameBoard import GameBoard


class RandomAgent(Agent):
    """Agente baseline: elige un movimiento válido al azar."""

    def __init__(self):
        pass

    def play(self, board: GameBoard) -> int:
        moves = self.safe_get_available_moves(board)
        return int(np.random.choice(moves)) if moves else 0

    def heuristic_utility(self, board: GameBoard) -> float:
        return 0.0

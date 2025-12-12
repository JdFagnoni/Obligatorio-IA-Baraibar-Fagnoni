import math
from Agent import Agent
from GameBoard import GameBoard
from heuristics import evaluate


class ExpectimaxAgent(Agent):

    def __init__(self, depth: int = 3, weights: dict | None = None):
        self.depth = depth
        self.weights = weights

    def heuristic_utility(self, board: GameBoard) -> float:
        return evaluate(board, weights=self.weights)

    def _chance_value(self, board: GameBoard, depth: int) -> float:
        cells = board.get_available_cells()
        if not cells:
            return self.heuristic_utility(board)

        prob_cell = 1.0 / len(cells)
        value = 0.0
        for cell in cells:
            for tile, prob_tile in ((2, 0.9), (4, 0.1)):
                clone = board.clone()
                clone.insert_tile(cell, tile)
                value += prob_cell * prob_tile * self._expectimax(clone, depth - 1, is_chance=False)
        return value

    def _expectimax(self, board: GameBoard, depth: int, is_chance: bool) -> float:
        # corte por profundidad o sin movimientos
        moves = board.get_available_moves()
        if depth == 0 or not moves:
            return self.heuristic_utility(board)

        if is_chance:
            return self._chance_value(board, depth)

        best = -math.inf
        for move in moves:
            clone = board.clone()
            clone.move(move)
            best = max(best, self._expectimax(clone, depth - 1, is_chance=True))
        return best

    def play(self, board: GameBoard) -> int:
        moves = board.get_available_moves()
        if not moves:
            return 0  # sin movimientos; valor por defecto

        best_move = moves[0]
        best_value = -math.inf

        for move in moves:
            clone = board.clone()
            clone.move(move)
            val = self._expectimax(clone, self.depth - 1, is_chance=True)
            if val > best_value:
                best_value = val
                best_move = move

        return best_move

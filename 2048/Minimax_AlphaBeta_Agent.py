import math
from Agent import Agent
from GameBoard import GameBoard
from heuristics import evaluate


class MinimaxAlphaBetaAgent(Agent):
    """
    Agente Minimax con poda Alpha-Beta para 2048.
    Modela nodos MAX (jugador) y nodos MIN (colocacion de ficha adversarial).
    En nodos MIN, selecciona la peor insercion posible (minimiza el valor esperado del MAX).
    Si ``use_pruning`` es False, opera como minimax puro (sin podas) para comparar impacto de alpha-beta.
    """

    def __init__(self, depth: int = 3, weights: dict | None = None, use_pruning: bool = True):
        self.depth = depth
        self.weights = weights
        self.use_pruning = use_pruning

    def heuristic_utility(self, board: GameBoard) -> float:
        return evaluate(board, weights=self.weights)

    def _min_value(self, board: GameBoard, depth: int, alpha: float, beta: float) -> float:
        cells = board.get_available_cells()
        if not cells or depth == 0:
            return self.heuristic_utility(board)

        value = math.inf
        for cell in cells:
            for tile in (2, 4):
                clone = board.clone()
                clone.insert_tile(cell, tile)
                value = min(value, self._max_value(clone, depth - 1, alpha, beta))
                if self.use_pruning:
                    if value <= alpha:
                        return value  # poda alfa
                    beta = min(beta, value)
        return value

    def _max_value(self, board: GameBoard, depth: int, alpha: float, beta: float) -> float:
        moves = board.get_available_moves()
        if depth == 0 or not moves:
            return self.heuristic_utility(board)

        value = -math.inf
        for move in moves:
            clone = board.clone()
            clone.move(move)
            value = max(value, self._min_value(clone, depth - 1, alpha, beta))
            if self.use_pruning:
                if value >= beta:
                    return value  # poda beta
                alpha = max(alpha, value)
        return value

    def play(self, board: GameBoard) -> int:
        moves = board.get_available_moves()
        if not moves:
            return 0

        best_move = moves[0]
        best_value = -math.inf
        alpha, beta = -math.inf, math.inf

        for move in moves:
            clone = board.clone()
            clone.move(move)
            val = self._min_value(clone, self.depth - 1, alpha, beta)
            if val > best_value:
                best_value = val
                best_move = move
            if self.use_pruning:
                alpha = max(alpha, best_value)

        return best_move

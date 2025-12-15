from __future__ import annotations

import contextlib
from abc import ABC, abstractmethod

import numpy as np

from GameBoard import GameBoard


@contextlib.contextmanager
def preserve_numpy_rng():

    state = np.random.get_state()
    try:
        yield
    finally:
        np.random.set_state(state)


class Agent(ABC):
    """Interfaz común de agentes."""

    @abstractmethod
    def play(self, board: GameBoard) -> int:
        """Devuelve la acción (0..3) a ejecutar en el board."""

    @abstractmethod
    def heuristic_utility(self, board: GameBoard) -> float:
        """Evalúa un estado del tablero. Mayor = mejor para el jugador."""

    def safe_get_available_moves(self, board: GameBoard) -> list[int]:
        """Wrapper para evitar consumir RNG en get_available_moves()."""
        with preserve_numpy_rng():
            return board.get_available_moves()

    def safe_get_available_cells(self, board: GameBoard) -> list[tuple[int, int]]:
        """Wrapper simétrico; get_available_cells() no usa RNG."""
        return board.get_available_cells()

    def safe_clone(self, board: GameBoard) -> GameBoard:
        """Wrapper para evitar consumir RNG en clone()."""
        with preserve_numpy_rng():
            return board.clone()

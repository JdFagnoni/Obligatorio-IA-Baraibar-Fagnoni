import numpy as np
from GameBoard import GameBoard

# Heuristicas simples y combinables para evaluar un tablero 2048.
# Todas las funciones aceptan GameBoard o np.ndarray (shape 4x4).


def _as_grid(board_or_grid):
    """Devuelve una vista numpy 4x4 a partir de GameBoard o ndarray."""
    if isinstance(board_or_grid, GameBoard):
        return board_or_grid.grid
    return np.asarray(board_or_grid)


def count_empty(board_or_grid) -> int:
    """Cantidad de celdas vacias (valor 0)."""
    grid = _as_grid(board_or_grid)
    return int(np.sum(grid == 0))


def max_tile_in_corner(board_or_grid) -> int:
    """Devuelve el valor de la ficha maxima si esta en una esquina; si no, 0."""
    grid = _as_grid(board_or_grid)
    max_tile = int(np.max(grid))
    corners = [grid[0, 0], grid[0, -1], grid[-1, 0], grid[-1, -1]]
    return max_tile if max_tile in corners else 0


def monotonicity(board_or_grid) -> float:
    """
    Mide cuan monotono es el tablero por filas y columnas.
    Cuenta cuantas diferencias consecutivas mantienen la direccion (creciente o decreciente).
    """
    grid = _as_grid(board_or_grid)
    log_grid = np.log2(grid, where=grid > 0, out=np.zeros_like(grid))

    def line_score(line: np.ndarray) -> int:
        diffs = np.diff(line)
        inc = np.sum(diffs >= 0)
        dec = np.sum(diffs <= 0)
        return int(max(inc, dec))

    score = 0
    for row in log_grid:
        score += line_score(row)
    for col in log_grid.T:
        score += line_score(col)
    return float(score)


def smoothness(board_or_grid) -> float:
    """
    Penaliza diferencias grandes entre celdas adyacentes.
    Se calcula sobre log2 para que las potencias de 2 sean lineales.
    Devuelve un valor negativo (a mayor similitud, menos penalizacion).
    """
    grid = _as_grid(board_or_grid)
    log_grid = np.log2(grid, where=grid > 0, out=np.zeros_like(grid))
    penalty = 0.0
    for i in range(4):
        for j in range(4):
            if j + 1 < 4:
                penalty -= abs(log_grid[i, j] - log_grid[i, j + 1])
            if i + 1 < 4:
                penalty -= abs(log_grid[i, j] - log_grid[i + 1, j])
    return float(penalty)


def merges_possible(board_or_grid) -> int:
    """
    Cuenta pares adyacentes iguales (potencial inmediato de merge).
    """
    grid = _as_grid(board_or_grid)
    count = 0
    for i in range(4):
        for j in range(4):
            if j + 1 < 4 and grid[i, j] == grid[i, j + 1] and grid[i, j] != 0:
                count += 1
        if i + 1 < 4 and grid[i, j] == grid[i + 1, j] and grid[i, j] != 0:
            count += 1
    return count


def positional_weight(board_or_grid) -> float:
    """
    Favorece una disposicion serpenteada que coloca las fichas grandes en una esquina.
    Usa pesos decrecientes en forma de serpiente y pondera con log2 de las fichas.
    """
    grid = _as_grid(board_or_grid)
    log_grid = np.log2(grid, where=grid > 0, out=np.zeros_like(grid))
    weights = np.array([
        [65536, 32768, 16384, 8192],
        [4096,  2048,  1024,  512],
        [256,   128,    64,   32],
        [16,      8,     4,    2],
    ], dtype=float)
    return float(np.sum(log_grid * weights))


DEFAULT_WEIGHTS = {
    "empty": 250.0,          # prioriza espacio libre para evitar bloqueos
    "monotonicity": 1.5,     # impulsa cadenas ordenadas
    "corner": 25.0,          # incentiva mantener la ficha maxima en esquina
    "smoothness": 3.0,       # aplica a un valor negativo; peso positivo reduce penalizacion
    "merges": 50.0,          # incentiva tener merges inmediatos disponibles
    "positional": 0.1,       # pondera el peso posicional serpenteado
}


def evaluate(board_or_grid, weights: dict | None = None) -> float:
    """
    Combina varias heuristicas con pesos. Retorna un escalar a maximizar.
    Pesos por defecto pensados para busqueda expectimax/minimax superficial.
    """
    w = weights or DEFAULT_WEIGHTS
    components = {
        "empty": count_empty(board_or_grid),
        "monotonicity": monotonicity(board_or_grid),
        "corner": max_tile_in_corner(board_or_grid),
        "smoothness": smoothness(board_or_grid),
        "merges": merges_possible(board_or_grid),
        "positional": positional_weight(board_or_grid),
    }
    return float(sum(w.get(k, 0.0) * components[k] for k in components))

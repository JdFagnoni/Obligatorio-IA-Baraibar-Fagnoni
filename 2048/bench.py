import argparse
import csv
import time
from pathlib import Path

from GameBoard import GameBoard
from Expectimax_Agent import ExpectimaxAgent
from Minimax_AlphaBeta_Agent import MinimaxAlphaBetaAgent
from Random_Agent import RandomAgent

# Presets de pesos para no escribirlos en CLI
PRESET_WEIGHTS = {
    # baseline: similar a defaults de heuristics.py antes de tunear
    "baseline": {"empty": 250, "monotonicity": 1.5, "corner": 25, "smoothness": 3.0, "merges": 50},
    # tuned: preset que ya probamos
    "tuned": {"empty": 320, "monotonicity": 2.0, "corner": 35, "smoothness": 2.0, "merges": 70},
    # corner-heavy: enfatiza mantener la ficha maxima en esquina
    "corner_heavy": {"empty": 300, "monotonicity": 1.8, "corner": 60, "smoothness": 2.0, "merges": 60},
    # smooth-heavy: prioriza tableros suaves y ordenados
    "smooth_heavy": {"empty": 280, "monotonicity": 2.2, "corner": 25, "smoothness": 4.0, "merges": 50},
    # snake: agrega peso posicional tipo serpiente y refuerza vacios/esquinas
    "snake": {"empty": 320, "monotonicity": 2.0, "corner": 40, "smoothness": 2.5, "merges": 70, "positional": 0.5},
}


def check_win(board: GameBoard) -> bool:
    return board.get_max_tile() >= 2048


def play_episode(agent, render: bool = False) -> dict:
    board = GameBoard()
    moves = 0
    start = time.time()
    done = False

    if render:
        board.render()

    while not done:
        action = agent.play(board)
        done = board.play(action)
        done = done or check_win(board)
        moves += 1
        if render:
            board.render()

    duration = time.time() - start
    stats = {
        "moves": moves,
        "max_tile": int(board.get_max_tile()),
        "duration_sec": duration,
        "win": check_win(board),
        "grid_sum": float(board.grid.sum()),
    }
    return stats


def parse_weights(weights_str: str | None):
    """
    Parsea un string tipo 'empty=300,monotonicity=2,corner=30,smoothness=2,merges=70'
    y devuelve un dict. Si es None o vacio, retorna None.
    """
    if not weights_str:
        return None
    weights = {}
    for part in weights_str.split(","):
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        try:
            weights[k.strip()] = float(v)
        except ValueError:
            pass
    return weights if weights else None


def main():
    parser = argparse.ArgumentParser(description="Benchmark agents for 2048.")
    parser.add_argument("--episodes", type=int, default=5, help="Cantidad de partidas a correr")
    parser.add_argument("--agent", choices=["expectimax", "minimax", "random"], default="expectimax", help="Agente a evaluar")
    parser.add_argument("--depth", type=int, default=3, help="Profundidad de busqueda (expectimax/minimax)")
    parser.add_argument("--render", action="store_true", help="Imprime tableros en cada paso (lento)")
    parser.add_argument("--preset", choices=list(PRESET_WEIGHTS.keys()), help="Nombre de preset de pesos (ej: tuned)")
    parser.add_argument("--weights", type=str, default=None, help="Pesos custom: empty=320,monotonicity=2,corner=35,smoothness=2,merges=70 (prioridad sobre preset)")
    parser.add_argument("--output", type=str, default=None, help="Ruta CSV para guardar resultados por episodio")
    parser.add_argument("--no-pruning", action="store_true", help="Desactiva la poda alpha-beta en minimax para comparar")
    args = parser.parse_args()

    weights = parse_weights(args.weights) if args.weights else PRESET_WEIGHTS.get(args.preset)

    if args.agent == "expectimax":
        agent = ExpectimaxAgent(depth=args.depth, weights=weights)
    elif args.agent == "minimax":
        agent = MinimaxAlphaBetaAgent(depth=args.depth, weights=weights, use_pruning=not args.no_pruning)
    else:
        agent = RandomAgent()

    results = []
    for ep in range(args.episodes):
        stats = play_episode(agent, render=args.render)
        results.append(stats)
        print(f"Episodio {ep+1}/{args.episodes} -> max_tile={stats['max_tile']}, moves={stats['moves']}, win={stats['win']}, time={stats['duration_sec']:.2f}s")

    avg_moves = sum(r["moves"] for r in results) / len(results)
    avg_max = sum(r["max_tile"] for r in results) / len(results)
    win_rate = sum(1 for r in results if r["win"]) / len(results)
    avg_time = sum(r["duration_sec"] for r in results) / len(results)

    print("\nResumen:")
    print(f"  Agent: {args.agent} (depth={args.depth if args.agent!='random' else 'N/A'})")
    print(f"  Episodios: {args.episodes}")
    print(f"  Win rate: {win_rate*100:.1f}%")
    print(f"  Max tile promedio: {avg_max:.1f}")
    print(f"  Movimientos promedio: {avg_moves:.1f}")
    print(f"  Tiempo promedio: {avg_time:.2f}s")
    if args.agent == "minimax":
        print(f"  Poda alpha-beta: {'ON' if not args.no_pruning else 'OFF'}")
    if weights:
        print(f"  Pesos: {weights}")

    if args.output:
        path = Path(args.output)
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["episode", "agent", "depth", "win", "max_tile", "moves", "duration_sec", "grid_sum"])
            writer.writeheader()
            for idx, r in enumerate(results, start=1):
                writer.writerow({
                    "episode": idx,
                    "agent": args.agent,
                    "depth": args.depth if args.agent != "random" else None,
                    "win": r["win"],
                    "max_tile": r["max_tile"],
                    "moves": r["moves"],
                    "duration_sec": f"{r['duration_sec']:.4f}",
                    "grid_sum": f"{r['grid_sum']:.2f}",
                })
        print(f"Resultados guardados en {path}")


if __name__ == "__main__":
    main()

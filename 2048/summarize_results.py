"""
Consolida resultados CSV generados por bench.py.
Uso:
    python summarize_results.py --pattern "*.csv"
Agrupa por archivo (que codifica agent/preset) y muestra win%, max tile promedio,
movimientos promedio y tiempo promedio.
"""

import argparse
import csv
import glob
import statistics
from pathlib import Path


def parse_bool(value: str) -> bool:
    return value.lower() in ("true", "1", "yes")


def summarize_file(path: Path) -> dict:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return {}

    wins = [parse_bool(r["win"]) for r in rows]
    max_tiles = [int(r["max_tile"]) for r in rows]
    moves = [int(r["moves"]) for r in rows]
    times = [float(r["duration_sec"]) for r in rows]

    depth = rows[0].get("depth")  # puede ser None para random
    return {
        "file": path.name,
        "agent": path.name.split("_")[0],
        "preset": path.stem.split("_")[-1],
        "episodes": len(rows),
        "win_rate": sum(wins) / len(wins) * 100,
        "max_avg": statistics.mean(max_tiles),
        "moves_avg": statistics.mean(moves),
        "time_avg": statistics.mean(times),
        "depth": depth,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", default="*.csv", help="Glob para archivos CSV (por defecto *.csv)")
    args = parser.parse_args()

    summaries = []
    for path in glob.glob(args.pattern):
        info = summarize_file(Path(path))
        if info:
            summaries.append(info)

    summaries.sort(key=lambda x: (-x["win_rate"], -x["max_avg"]))

    print("agent,preset,depth,episodes,win%,max_avg,moves_avg,time_avg_s,file")
    for s in summaries:
        print(
            f"{s['agent']},{s['preset']},{s['depth']},{s['episodes']},"
            f"{s['win_rate']:.1f},{s['max_avg']:.1f},{s['moves_avg']:.1f},{s['time_avg']:.1f},{s['file']}"
        )


if __name__ == "__main__":
    main()

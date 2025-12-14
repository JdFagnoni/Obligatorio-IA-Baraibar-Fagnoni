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
import re
from pathlib import Path
import sys


def parse_bool(value: str) -> bool:
    return value.lower() in ("true", "1", "yes")


def parse_filename(stem: str) -> dict:
    """
    Intenta extraer metadata del nombre del archivo.
    Convención recomendada: agent_preset_dX[_variant].csv
    Ejemplos:
      - expectimax_smooth_heavy_d3.csv
      - minimax_smooth_heavy_d4_prune.csv
      - minimax_smooth_heavy_d4_noprune.csv
    """
    parts = stem.split("_")
    agent = parts[0] if parts else ""

    depth_from_name = None
    depth_idx = None
    for idx, part in enumerate(parts):
        if part.startswith("d") and part[1:].isdigit():
            depth_from_name = part[1:]
            depth_idx = idx
            break

    preset_parts = []
    variant_parts = []
    if depth_idx is not None:
        preset_parts = parts[1:depth_idx]
        variant_parts = parts[depth_idx + 1 :]
    else:
        preset_parts = parts[1:]

    preset = "_".join(preset_parts) if preset_parts else ""
    variant = "_".join(variant_parts) if variant_parts else ""

    return {"agent": agent, "preset": preset, "variant": variant, "depth_from_name": depth_from_name}


def summarize_file(path: Path) -> dict:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return {}

    required_fields = {"win", "max_tile", "moves", "duration_sec"}
    if not required_fields.issubset(rows[0].keys()):
        return {}

    wins = [parse_bool(r["win"]) for r in rows]
    max_tiles = [int(r["max_tile"]) for r in rows]
    moves = [int(r["moves"]) for r in rows]
    times = [float(r["duration_sec"]) for r in rows]

    depth = rows[0].get("depth")  # puede ser None para random
    meta = parse_filename(path.stem)
    if depth in (None, "", "None"):
        depth = meta["depth_from_name"]
    win_count = sum(wins)
    episodes = len(rows)
    max_sum = sum(max_tiles)
    moves_sum = sum(moves)
    time_sum = sum(times)
    return {
        "file": path.name,
        "agent": meta["agent"] or path.name.split("_")[0],
        "preset": meta["preset"] or "",
        "variant": meta["variant"] or "",
        "episodes": episodes,
        "wins": win_count,
        "win_rate": win_count / episodes * 100,
        "max_sum": max_sum,
        "moves_sum": moves_sum,
        "time_sum": time_sum,
        "max_avg": max_sum / episodes,
        "moves_avg": moves_sum / episodes,
        "time_avg": time_sum / episodes,
        "depth": depth,
    }


def strip_seed_suffix(text: str) -> str:
    if not text:
        return text
    text = re.sub(r"(?i)(?:_)?seed\d+$", "", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text


def aggregate_summaries(summaries: list[dict]) -> list[dict]:
    groups: dict[tuple[str, str, str, str | None], list[dict]] = {}
    for s in summaries:
        key = (
            s["agent"],
            strip_seed_suffix(s["preset"]),
            strip_seed_suffix(s["variant"]),
            s["depth"],
        )
        groups.setdefault(key, []).append(s)

    aggregated: list[dict] = []
    for (agent, preset, variant, depth), items in groups.items():
        episodes = sum(i["episodes"] for i in items)
        wins = sum(i["wins"] for i in items)
        max_sum = sum(i["max_sum"] for i in items)
        moves_sum = sum(i["moves_sum"] for i in items)
        time_sum = sum(i["time_sum"] for i in items)
        aggregated.append(
            {
                "agent": agent,
                "preset": preset,
                "variant": variant,
                "depth": depth,
                "runs": len(items),
                "episodes": episodes,
                "win_rate": (wins / episodes * 100) if episodes else 0.0,
                "max_avg": (max_sum / episodes) if episodes else 0.0,
                "moves_avg": (moves_sum / episodes) if episodes else 0.0,
                "time_avg": (time_sum / episodes) if episodes else 0.0,
                "files": ";".join(sorted(i["file"] for i in items)),
            }
        )

    aggregated.sort(key=lambda x: (-x["win_rate"], -x["max_avg"]))
    return aggregated


def write_csv(summaries: list[dict], out_f, *, aggregated: bool) -> None:
    writer = csv.writer(out_f, lineterminator="\n")
    if aggregated:
        writer.writerow(
            [
                "agent",
                "preset",
                "variant",
                "depth",
                "runs",
                "episodes",
                "win%",
                "max_avg",
                "moves_avg",
                "time_avg_s",
                "files",
            ]
        )
        for s in summaries:
            depth = s["depth"] if s.get("depth") not in (None, "") else "None"
            writer.writerow(
                [
                    s["agent"],
                    s["preset"],
                    s["variant"],
                    depth,
                    s["runs"],
                    s["episodes"],
                    f"{s['win_rate']:.1f}",
                    f"{s['max_avg']:.1f}",
                    f"{s['moves_avg']:.1f}",
                    f"{s['time_avg']:.1f}",
                    s["files"],
                ]
            )
        return

    writer.writerow(["agent", "preset", "variant", "depth", "episodes", "win%", "max_avg", "moves_avg", "time_avg_s", "file"])
    for s in summaries:
        depth = s["depth"] if s.get("depth") not in (None, "") else "None"
        writer.writerow(
            [
                s["agent"],
                s["preset"],
                s["variant"],
                depth,
                s["episodes"],
                f"{s['win_rate']:.1f}",
                f"{s['max_avg']:.1f}",
                f"{s['moves_avg']:.1f}",
                f"{s['time_avg']:.1f}",
                s["file"],
            ]
        )


def write_markdown(summaries: list[dict], out_f, *, aggregated: bool) -> None:
    if aggregated:
        header = ["agent", "preset", "variant", "depth", "runs", "episodes", "win%", "max_avg", "moves_avg", "time_avg_s"]
        out_f.write("| " + " | ".join(header) + " |\n")
        out_f.write("|---|---|---|---:|---:|---:|---:|---:|---:|---:|\n")
        for s in summaries:
            depth = s["depth"] if s.get("depth") not in (None, "") else "None"
            out_f.write(
                "| "
                + " | ".join(
                    [
                        str(s["agent"]),
                        str(s["preset"]),
                        str(s["variant"]),
                        str(depth),
                        str(s["runs"]),
                        str(s["episodes"]),
                        f"{s['win_rate']:.1f}",
                        f"{s['max_avg']:.1f}",
                        f"{s['moves_avg']:.1f}",
                        f"{s['time_avg']:.1f}",
                    ]
                )
                + " |\n"
            )
        return

    header = ["agent", "preset", "variant", "depth", "episodes", "win%", "max_avg", "moves_avg", "time_avg_s", "file"]
    out_f.write("| " + " | ".join(header) + " |\n")
    out_f.write("|---|---|---|---:|---:|---:|---:|---:|---:|---|\n")
    for s in summaries:
        depth = s["depth"] if s.get("depth") not in (None, "") else "None"
        out_f.write(
            "| "
            + " | ".join(
                [
                    str(s["agent"]),
                    str(s["preset"]),
                    str(s["variant"]),
                    str(depth),
                    str(s["episodes"]),
                    f"{s['win_rate']:.1f}",
                    f"{s['max_avg']:.1f}",
                    f"{s['moves_avg']:.1f}",
                    f"{s['time_avg']:.1f}",
                    str(s["file"]),
                ]
            )
            + " |\n"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", default="*.csv", help="Glob para archivos CSV (por defecto *.csv)")
    parser.add_argument(
        "--format",
        default="csv",
        choices=["csv", "md"],
        help="Formato de salida: csv (default) o md (tabla Markdown).",
    )
    parser.add_argument(
        "--aggregate",
        action="store_true",
        help="Agrupa corridas equivalentes (remueve sufijo _seedN de preset/variant) y agrega episodios.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help='Ruta de salida para guardar el resumen (por defecto imprime a stdout). Usa "-" para stdout.',
    )
    args = parser.parse_args()

    summaries = []
    for path in glob.glob(args.pattern):
        info = summarize_file(Path(path))
        if info:
            summaries.append(info)

    summaries.sort(key=lambda x: (-x["win_rate"], -x["max_avg"]))

    if args.aggregate:
        summaries = aggregate_summaries(summaries)

    out_f = sys.stdout
    close_out = False
    if args.output and args.output != "-":
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_f = out_path.open("w", newline="")
        close_out = True

    try:
        if args.format == "md":
            write_markdown(summaries, out_f, aggregated=args.aggregate)
        else:
            write_csv(summaries, out_f, aggregated=args.aggregate)
    finally:
        if close_out:
            out_f.close()


if __name__ == "__main__":
    main()

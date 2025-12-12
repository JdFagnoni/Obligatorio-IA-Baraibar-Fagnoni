## MEC – Resumen de agentes y pruebas (2048)

### Técnicas implementadas
- **Expectimax**: búsqueda con nodos de azar (2/4 con prob. 0.9/0.1), profundidad configurable.
- **Minimax + Alpha-Beta**: nodos MIN adversariales (colocan 2/4), poda alfa-beta activa.

### Heurísticas / funciones de evaluación
Componentes: celdas vacías, monotonicidad (filas/columnas), smoothness (penaliza diferencias), merges posibles, ficha máxima en esquina, peso posicional “serpiente”. Se prueban combinaciones via presets en `bench.py`:
- baseline, tuned, corner_heavy, smooth_heavy, snake (con peso posicional).

### Benchmark (5 partidas por combo, depth indicados)
Formato CSV: `agent`, `preset`, `depth`, `win`, `max_tile`, `moves`, `duration_sec`, `grid_sum`. Resumen de los que corrimos:
- **Expectimax d3**:
  - smooth_heavy: 20% win, max tile prom. ≈1126, tiempo prom. ≈74s.
  - baseline: 20% win, max tile prom. ≈1126, tiempo prom. ≈94s.
  - corner_heavy: 20% win, max tile prom. ≈1024, tiempo prom. ≈83s.
  - snake: 20% win, max tile prom. ≈1075, tiempo prom. ≈162s.
  - tuned: 0% win.
- **Minimax d4**:
  - snake: 20% win, max tile prom. ≈870, tiempo prom. ≈191s.
  - Otros presets: 0% win, max tile prom. < ~615, tiempos > ~175s.

Conclusión operativa:
- Expectimax con preset **smooth_heavy** (o baseline) rinde mejor que Minimax y con menos tiempo; usamos esa configuración por defecto (ver `Main.py`).
- Minimax con poda funciona pero queda por debajo en calidad/tiempo; lo mantenemos para comparación en el informe y para cumplir la consigna de analizar α-β.

### Protocolo de experimentación (para informe)
- Agente y profundidad: Expectimax d3; Minimax d4 (poda α-β). Opcional: Expectimax d4 si el tiempo lo permite.
- Presets probados: baseline, smooth_heavy, corner_heavy, snake, tuned (para mostrar que no todos mejoran).
- Métricas por episodio: win (llega a 2048), `max_tile`, `moves`, `duration_sec`, `grid_sum`.
- Repeticiones: 5–10 episodios por combinación; guardar CSV con `--output`.
- Registro/consumo de resultados: usar `summarize_results.py --pattern "*.csv"` para consolidar win%, max tile prom., tiempo prom. y elegir la mejor combinación. Incluir tabla en el informe.

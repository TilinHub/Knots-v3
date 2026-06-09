"""Verificacion de 4_1 (seccion 11): que significa verificar 4_1 en esta version.

Corre las 13 verificaciones de la seccion 11 sobre un diagrama de nudo y imprime
el reporte esperado. El programa no demuestra que el nudo sea 4_1: verifica que
los datos declarados sean internamente consistentes.

Uso:
    python verify_4_1.py                              # usa el 4_1 por defecto
    python verify_4_1.py examples/figure8_4_1_manual.json

Este script es provisional. La version definitiva del reporte la producira
knot_diagram_report (Modulo 5), apoyandose en knot_diagram.py y crossings.py.
Codigo de salida: 0 si pasan las 13 verificaciones, 1 si alguna falla.
"""

import os
import sys

from csdraw.io_json import load_diagram
from csdraw.length import total_length
from csdraw.render_svg import write_svg


def _start_end(cs, piece_id):
    piece = cs.segments.get(piece_id) or cs.arcs.get(piece_id)
    if piece is None:
        raise ValueError(f"Unknown piece: {piece_id}")
    return piece.start, piece.end


def verify(json_path: str) -> bool:
    cs = load_diagram(json_path)
    pids = cs.piece_ids()

    # Las 13 verificaciones de la seccion 11.
    c1 = cs.meta.get("type") == "knot_diagram"
    c2 = cs.meta.get("knot_label") == "4_1"
    c3 = len(cs.crossings) == 4
    ids = [c.id for c in cs.crossings]
    c4 = len(ids) == len(set(ids))
    c5 = all(c.over_piece and c.under_piece for c in cs.crossings)
    c6 = all(c.over_piece in pids and c.under_piece in pids for c in cs.crossings)
    c7 = all(c.over_piece != c.under_piece for c in cs.crossings)
    c8 = len(cs.components) == 1

    if cs.components:
        comp = cs.components[0]
        c9 = all(p in pids for p in comp)
        c10 = sorted(comp) == sorted(pids)
        c11 = all(
            _start_end(cs, comp[i])[1] == _start_end(cs, comp[(i + 1) % len(comp)])[0]
            for i in range(len(comp))
        )
    else:
        comp, c9, c10, c11 = [], False, False, False

    try:
        length = total_length(cs)
        c12 = 0.0 < length < float("inf")
    except Exception:
        c12 = False

    svg_path = os.path.splitext(json_path)[0] + ".svg"
    try:
        write_svg(cs, svg_path)
        c13 = os.path.isfile(svg_path)
    except Exception:
        c13 = False

    checks = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13]

    # Lineas agregadas del reporte.
    crossing_ids_valid = c3 and c4
    crossing_pieces_valid = c6
    over_under_valid = c5 and c7
    crossings_valid = crossing_ids_valid and crossing_pieces_valid and over_under_valid

    print(f"knot label: {cs.meta.get('knot_label')}")
    print(f"number of crossings: {len(cs.crossings)}")
    print(f"number of components: {len(cs.components)}")
    print(f"component pieces valid: {c9}")
    print(f"all pieces used exactly once: {c10}")
    print(f"component closed: {c11}")
    print(f"crossing ids valid: {crossing_ids_valid}")
    print(f"crossing pieces valid: {crossing_pieces_valid}")
    print(f"over/under valid: {over_under_valid}")
    print(f"crossings valid: {crossings_valid}")
    print(f"length valid: {c12}")

    all_ok = all(checks)
    print()
    print(f"13 verificaciones: {sum(checks)}/13   ->   {'OK' if all_ok else 'ERROR'}")
    if not all_ok:
        labels = [
            "type knot_diagram", "knot_label 4_1", "4 cruces", "ids unicos",
            "over y under presentes", "over/under existen", "over != under",
            "una componente", "componente usa piezas existentes",
            "cada pieza una vez", "componente cerrada", "longitud computable",
            "SVG exportable",
        ]
        fallan = [labels[i] for i, v in enumerate(checks) if not v]
        print("Fallan:", ", ".join(fallan))
    print(f"SVG written to: {svg_path}")
    return all_ok


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "examples/figure8_4_1_manual.json"
    ok = verify(path)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()

"""Punto de entrada de csdraw.

Dia 1 (motor cs basico): lee un diagrama cs desde JSON, reporta su estructura,
calcula la longitud total y exporta un SVG.

Uso:
    python main.py examples/stadium_2.json
"""

import os
import sys

from csdraw.io_json import load_diagram
from csdraw.length import total_length
from csdraw.render_svg import write_svg


def run(json_path: str):
    # Pipeline completo (seccion 6):
    #   input -> puntos -> longitud -> SVG -> componentes -> cruces -> 4_1
    #   -> rolling -> reducido -> descenso -> variables -> validacion -> optimizacion
    # main.py cubre hoy el tramo vivo: input -> puntos -> longitud -> SVG.
    # Las etapas siguientes son stubs declarados y se conectan en sus puntos.
    cs = load_diagram(json_path)
    meta = cs.meta

    print(f"Diagram: {meta.get('name')}")
    print(f"Type: {meta.get('type')}")
    print(f"Number of disks: {len(cs.disks)}")
    print(f"Number of labels: {len(cs.labels)}")
    print(f"Number of segments: {len(cs.segments)}")
    print(f"Number of arcs: {len(cs.arcs)}")
    print(f"Number of components: {len(cs.components)}")
    print(f"Number of crossings: {len(cs.crossings)}")
    print(f"Total length: {total_length(cs)}")

    svg_path = os.path.splitext(json_path)[0] + ".svg"
    write_svg(cs, svg_path)
    print(f"SVG written to: {svg_path}")


def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo.json>")
        raise SystemExit(2)
    run(sys.argv[1])


if __name__ == "__main__":
    main()

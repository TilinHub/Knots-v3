"""Modulo de dibujo: render_svg.

Exporta un diagrama cs a un archivo SVG. Dibuja los discos como circulos de
contexto, los segmentos como lineas rectas y los arcos como polilineas
muestreadas a lo largo de la orientacion declarada.
"""

import math

from .cs_geometry import CSRealization

R = 1.0
TWO_PI = 2.0 * math.pi
_ARC_SAMPLES = 48


def _arc_points(cs: CSRealization, a):
    disk = cs.disk(a.disk)
    cx, cy = disk.center
    theta_s = cs.label(a.start).theta
    theta_e = cs.label(a.end).theta
    if a.orientation == "cw":
        sweep = (theta_s - theta_e) % TWO_PI
        sign = -1.0
    elif a.orientation == "ccw":
        sweep = (theta_e - theta_s) % TWO_PI
        sign = 1.0
    else:
        raise ValueError(f"Invalid arc orientation: {a.orientation}")
    pts = []
    for i in range(_ARC_SAMPLES + 1):
        t = i / _ARC_SAMPLES
        theta = theta_s + sign * sweep * t
        pts.append((cx + R * math.cos(theta), cy + R * math.sin(theta)))
    return pts


def write_svg(cs: CSRealization, path: str, scale: float = 100.0, margin: float = 0.5):
    # Caja delimitadora a partir de los discos (incluye su radio).
    xs, ys = [], []
    for disk in cs.disks.values():
        cx, cy = disk.center
        xs += [cx - R, cx + R]
        ys += [cy - R, cy + R]
    xmin, xmax = min(xs) - margin, max(xs) + margin
    ymin, ymax = min(ys) - margin, max(ys) + margin

    width = (xmax - xmin) * scale
    height = (ymax - ymin) * scale

    def tx(x):
        return (x - xmin) * scale

    def ty(y):
        # SVG tiene el eje y hacia abajo; lo invertimos.
        return (ymax - y) * scale

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width:.1f}" height="{height:.1f}" '
        f'viewBox="0 0 {width:.1f} {height:.1f}">',
        '<rect width="100%" height="100%" fill="white"/>',
    ]

    # Discos de contexto.
    for disk in cs.disks.values():
        cx, cy = disk.center
        lines.append(
            f'<circle cx="{tx(cx):.2f}" cy="{ty(cy):.2f}" r="{R * scale:.2f}" '
            f'fill="none" stroke="#cccccc" stroke-width="1"/>'
        )

    # Segmentos.
    for s in cs.segments.values():
        ax, ay = cs.point(s.start)
        bx, by = cs.point(s.end)
        lines.append(
            f'<line x1="{tx(ax):.2f}" y1="{ty(ay):.2f}" '
            f'x2="{tx(bx):.2f}" y2="{ty(by):.2f}" '
            f'stroke="#1f4fff" stroke-width="2"/>'
        )

    # Arcos.
    for a in cs.arcs.values():
        pts = _arc_points(cs, a)
        poly = " ".join(f"{tx(x):.2f},{ty(y):.2f}" for x, y in pts)
        lines.append(
            f'<polyline points="{poly}" fill="none" '
            f'stroke="#1f4fff" stroke-width="2"/>'
        )

    lines.append("</svg>")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    return path

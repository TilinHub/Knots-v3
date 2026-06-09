"""Modulo 2: length.

Calcula la longitud de un diagrama cs.

    Len = sum_{s: alpha->beta} ||p_beta - p_alpha||
        + sum_{a: alpha->beta} Delta_a(theta_alpha, theta_beta).

Disco de radio R = 1, por lo que la longitud de un arco es R veces el barrido
angular: arc_length = R * sweep.
"""

import math

from .cs_geometry import CSRealization

R = 1.0
TWO_PI = 2.0 * math.pi


def segment_length(cs: CSRealization, s) -> float:
    """ell_s = ||p_beta - p_alpha||."""
    if isinstance(s, str):
        s = cs.segment(s)
    ax, ay = cs.point(s.start)
    bx, by = cs.point(s.end)
    return math.hypot(bx - ax, by - ay)


def arc_length(cs: CSRealization, a) -> float:
    """ell_a = R * (barrido angular de theta_start a theta_end en la orientacion).

    cw  -> angulo decreciente: sweep = (theta_start - theta_end) mod 2pi.
    ccw -> angulo creciente:   sweep = (theta_end - theta_start) mod 2pi.
    """
    if isinstance(a, str):
        a = cs.arc(a)
    theta_s = cs.label(a.start).theta
    theta_e = cs.label(a.end).theta
    if a.orientation == "cw":
        sweep = (theta_s - theta_e) % TWO_PI
    elif a.orientation == "ccw":
        sweep = (theta_e - theta_s) % TWO_PI
    else:
        raise ValueError(f"Invalid arc orientation: {a.orientation}")
    return R * sweep


def total_length(cs: CSRealization) -> float:
    """Len = suma de longitudes de segmentos mas longitudes de arcos."""
    total = 0.0
    for s in cs.segments.values():
        total += segment_length(cs, s)
    for a in cs.arcs.values():
        total += arc_length(cs, a)
    return total


def length_report(cs: CSRealization) -> dict:
    """Reporte por pieza y total."""
    seg = {sid: segment_length(cs, s) for sid, s in cs.segments.items()}
    arc = {aid: arc_length(cs, a) for aid, a in cs.arcs.items()}
    return {
        "segments": seg,
        "arcs": arc,
        "total": total_length(cs),
    }

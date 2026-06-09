"""Modulo de entrada/salida: io_json.

Lee un diagrama cs desde un archivo JSON y construye una CSRealization.

Campos esperados del JSON:
    type, name
    disks:    id, center
    labels:   name, disk, theta
    segments: id, start, end
    arcs:     id, start, end, disk, orientation
    contacts: [[i, j], ...]
    components, crossings (metadata del diagrama)
"""

import json

from .cs_geometry import (
    Disk,
    Label,
    SegmentPiece,
    ArcPiece,
    Crossing,
    CSRealization,
)


def _require(d: dict, key: str, where: str):
    if key not in d:
        raise ValueError(f"Missing field '{key}' in {where}")
    return d[key]


def load_diagram(path: str) -> CSRealization:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    disks = {}
    for raw in _require(data, "disks", "diagram"):
        did = _require(raw, "id", "disk")
        center = _require(raw, "center", f"disk {did}")
        disks[did] = Disk(id=did, center=(float(center[0]), float(center[1])))

    labels = {}
    for raw in _require(data, "labels", "diagram"):
        name = _require(raw, "name", "label")
        disk = _require(raw, "disk", f"label {name}")
        theta = _require(raw, "theta", f"label {name}")
        if disk not in disks:
            raise ValueError(f"Unknown disk id: {disk}")
        labels[name] = Label(name=name, disk=disk, theta=float(theta))

    # Cada pieza (segmento o arco) debe tener un id unico, ya que esos ids se
    # usan para declarar componentes y cruces.
    piece_ids = set()

    segments = {}
    for raw in data.get("segments", []):
        sid = _require(raw, "id", "segment")
        if sid in piece_ids:
            raise ValueError(f"Duplicate piece id: {sid}")
        start = _require(raw, "start", f"segment {sid}")
        end = _require(raw, "end", f"segment {sid}")
        if start not in labels or end not in labels:
            raise ValueError("Segment endpoint does not exist")
        piece_ids.add(sid)
        segments[sid] = SegmentPiece(id=sid, start=start, end=end)

    arcs = {}
    for raw in data.get("arcs", []):
        aid = _require(raw, "id", "arc")
        if aid in piece_ids:
            raise ValueError(f"Duplicate piece id: {aid}")
        start = _require(raw, "start", f"arc {aid}")
        end = _require(raw, "end", f"arc {aid}")
        disk = _require(raw, "disk", f"arc {aid}")
        orientation = _require(raw, "orientation", f"arc {aid}")
        if start not in labels or end not in labels:
            raise ValueError("Segment endpoint does not exist")
        if disk not in disks:
            raise ValueError(f"Unknown disk id: {disk}")
        piece_ids.add(aid)
        arcs[aid] = ArcPiece(
            id=aid, start=start, end=end, disk=disk, orientation=orientation
        )

    contacts = []
    for raw in data.get("contacts", []):
        valid = (
            isinstance(raw, (list, tuple))
            and len(raw) == 2
            and raw[0] in disks
            and raw[1] in disks
        )
        if not valid:
            shown = list(raw) if isinstance(raw, (list, tuple)) else raw
            raise ValueError(f"Invalid contact: {shown}")
        contacts.append([raw[0], raw[1]])

    # Datos de diagrama de nudo. Las componentes se guardan como el recorrido
    # declarado de piezas; no se reconstruyen desde los cruces. Los cruces se
    # parsean a estructura; su validez (over/under, existencia de piezas) la
    # comprueba crossings.py, no este lector.
    components = [list(comp) for comp in data.get("components", [])]

    crossings = []
    for raw in data.get("crossings", []):
        cid = _require(raw, "id", "crossing")
        over = _require(raw, "over_piece", f"crossing {cid}")
        under = _require(raw, "under_piece", f"crossing {cid}")
        point = _require(raw, "point", f"crossing {cid}")
        crossings.append(
            Crossing(
                id=cid,
                over_piece=over,
                under_piece=under,
                point=tuple(point),
            )
        )

    meta = {
        "type": data.get("type"),
        "name": data.get("name"),
        "knot_label": data.get("knot_label"),
    }

    return CSRealization(
        disks=disks,
        labels=labels,
        segments=segments,
        arcs=arcs,
        contacts=contacts,
        components=components,
        crossings=crossings,
        meta=meta,
    )

"""Modulo 1: cs_geometry.

Define la geometria cs: discos, labels, segmentos, arcos y la realizacion cs.

La funcion central es point(label_name), que calcula

    p_alpha = c_{k(alpha)} + (cos theta_alpha, sin theta_alpha).

Disco de radio R = 1.
"""

from dataclasses import dataclass, field
from typing import Dict, List
import math


@dataclass
class Disk:
    id: int
    center: tuple  # (x, y)


@dataclass
class Label:
    name: str
    disk: int
    theta: float


@dataclass
class SegmentPiece:
    id: str
    start: str  # nombre de label inicial
    end: str    # nombre de label final


@dataclass
class ArcPiece:
    id: str
    start: str         # nombre de label inicial
    end: str           # nombre de label final
    disk: int
    orientation: str   # "cw" o "ccw"


@dataclass
class CSRealization:
    """Realizacion geometrica de un diagrama cs.

    Guarda discos, labels, segmentos, arcos y contactos, mas la metadata del
    diagrama (type, name, components, crossings) cuando esta disponible.
    """

    disks: Dict[int, Disk]
    labels: Dict[str, Label]
    segments: Dict[str, SegmentPiece]
    arcs: Dict[str, ArcPiece]
    contacts: List[list] = field(default_factory=list)
    meta: dict = field(default_factory=dict)

    # ---- acceso seguro a los datos ----

    def disk(self, disk_id: int) -> Disk:
        if disk_id not in self.disks:
            raise ValueError(f"Unknown disk id: {disk_id}")
        return self.disks[disk_id]

    def label(self, label_name: str) -> Label:
        if label_name not in self.labels:
            raise ValueError(f"Unknown label: {label_name}")
        return self.labels[label_name]

    def segment(self, piece_id: str) -> SegmentPiece:
        if piece_id not in self.segments:
            raise ValueError(f"Unknown piece: {piece_id}")
        return self.segments[piece_id]

    def arc(self, piece_id: str) -> ArcPiece:
        if piece_id not in self.arcs:
            raise ValueError(f"Unknown piece: {piece_id}")
        return self.arcs[piece_id]

    def piece(self, piece_id: str):
        """Acceso generico a una pieza (segmento o arco)."""
        if piece_id in self.segments:
            return self.segments[piece_id]
        if piece_id in self.arcs:
            return self.arcs[piece_id]
        raise ValueError(f"Unknown piece: {piece_id}")

    # ---- geometria ----

    def point(self, label_name: str) -> tuple:
        """p_alpha = c_{k(alpha)} + (cos theta_alpha, sin theta_alpha)."""
        lab = self.label(label_name)
        disk = self.disk(lab.disk)
        cx, cy = disk.center
        return (cx + math.cos(lab.theta), cy + math.sin(lab.theta))

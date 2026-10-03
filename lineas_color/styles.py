# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""JSON-safe edge styles stored on their ONE native group, never on subgroups."""
from copy import deepcopy
import math
import re

from PySide6.QtGui import QMatrix4x4, QVector3D

KEY = "lineas_color"
DEFAULT_WIDTH = 1.0
MIN_WIDTH, MAX_WIDTH = 1.0, 12.0
DEFAULT_PATTERN = "solid"
PATTERNS = (
    ("solid", "Continua", ()),
    ("dotted", "Punteada", (1, 3)),
    ("dashed", "Interrumpida", (6, 3)),
    ("long_dash", "Raya larga", (12, 4)),
    ("dash_dot", "Punto y raya", (8, 3, 1, 3)),
    ("dash_dot_dot", "Dos puntos y raya", (8, 3, 1, 3, 1, 3)),
)
PATTERN_LENGTHS = {key: lengths for key, _label, lengths in PATTERNS}


def validated_color(value):
    if not isinstance(value, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
        raise ValueError("El color debe tener el formato #RRGGBB.")
    return value.lower()


def validated_width(value):
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or not MIN_WIDTH <= value <= MAX_WIDTH):
        raise ValueError("El grosor debe estar entre 1 y 12 píxeles.")
    return float(value)


def validated_pattern(value):
    if not isinstance(value, str) or value not in PATTERN_LENGTHS:
        raise ValueError("El estilo de línea no es válido.")
    return value


def read_style(data):
    if not isinstance(data, dict):
        return None
    try:
        color = validated_color(data.get("color"))
    except ValueError:
        return None
    try:
        width = validated_width(data.get("width_px", DEFAULT_WIDTH))
    except ValueError:
        width = DEFAULT_WIDTH
    try:
        pattern = validated_pattern(data.get("pattern", DEFAULT_PATTERN))
    except ValueError:
        pattern = DEFAULT_PATTERN
    return color, width, pattern


def style_data(style):
    return dict(zip(("color", "width_px", "pattern"), style))


def group_style(group):
    return read_style((getattr(group, "ext", None) or {}).get(KEY))


def contains_segment(a, b, p, q):
    delta = b - a
    length2 = delta.lengthSquared()
    if length2 < 1e-16:
        return False
    tolerance = max(1e-6, math.sqrt(length2) * 1e-6)
    for point in (p, q):
        t = QVector3D.dotProduct(point - a, delta) / length2
        if not -1e-6 <= t <= 1 + 1e-6 or (point - (a + delta * t)).length() > tolerance:
            return False
    return True


def record_segments(data):
    out = []
    for item in data.get("edges", ()):
        style = read_style(item)
        if style is None:
            continue
        try:
            a, b = QVector3D(*item["a"]), QVector3D(*item["b"])
            if not all(math.isfinite(x) for p in (a, b) for x in p.toTuple()):
                continue
        except (KeyError, TypeError, ValueError):
            continue
        out.append((a, b, style))
    return out


def write_edge_styles(group, styles):
    data = deepcopy(group.ext or {})
    own = deepcopy(data.get(KEY, {}))
    own["edges"] = [{"a": list(e.a.toTuple()), "b": list(e.b.toTuple()), **style_data(styles[e])}
                    for e in group.mesh.edges if e in styles and styles[e]]
    data[KEY] = own
    group.ext = data


# Runtime identity keeps styles through native vertex moves and edge deletions.
# Persisted endpoint records survive IGZ, copies and mesh reorderings. Group-edit
# transitions reconcile records in world coordinates when the host bakes a mesh.
_tracked = {}


def edge_styles(group):
    data = (group.ext or {}).get(KEY, {})
    default = group_style(group)
    if not isinstance(data, dict) or "edges" not in data:
        _tracked.pop(group, None)
        return {e: default for e in group.mesh.edges if default}
    state = _tracked.get(group)
    records = record_segments(data)
    identities = {}
    if state and state["data"] == data:
        if state["mesh"] is group.mesh:
            identities = state["styles"]
        else:
            old_matrix = state["matrix"] or QMatrix4x4()
            inverse, ok = (group.xform or QMatrix4x4()).inverted()
            if ok:
                change = inverse * old_matrix
                records = [(change.map(a), change.map(b), style)
                           for a, b, style in state["records"]]
    styles = {}
    for edge in group.mesh.edges:
        style = identities.get(edge)
        if style is None:
            style = next((s for a, b, s in records
                          if contains_segment(a, b, edge.a, edge.b)), default)
        if style:
            styles[edge] = style
    # Retain identities for native undo resurrecting an erased edge.
    remembered = dict(identities)
    remembered.update(styles)
    write_edge_styles(group, styles)
    _tracked[group] = {"mesh": group.mesh, "matrix": QMatrix4x4(group.xform) if group.xform is not None else None,
                       "styles": remembered, "records": [(QVector3D(e.a), QVector3D(e.b), s)
                                                          for e, s in styles.items()],
                       "data": deepcopy(group.ext[KEY])}
    return styles


def sync_scene_styles(scene):
    alive = set()

    def walk(group):
        alive.add(group)
        edge_styles(group)
        for child in group.children:
            walk(child)

    for group in scene.groups:
        walk(group)
    # Detached groups may still be owned by undo commands; keep their state
    # until another document is opened (the controller clears it then).
    return alive


def install_edit_sync(scene):
    """Catch the native world/local bake even when saving without repainting."""
    if getattr(scene, "_lineas_color_edit_sync", False):
        return
    for name in ("begin_group_edit", "_leave_level"):
        original = getattr(scene, name)

        def wrapped(*args, _original=original, **kwargs):
            sync_scene_styles(scene)
            result = _original(*args, **kwargs)
            sync_scene_styles(scene)
            return result

        setattr(scene, name, wrapped)
    scene._lineas_color_edit_sync = True

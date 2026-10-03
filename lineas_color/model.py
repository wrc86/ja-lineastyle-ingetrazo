# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""Native shared meshes: welded lines, planar faces and reversible styles."""
from copy import deepcopy
from types import SimpleNamespace

from PySide6.QtGui import QMatrix4x4, QVector3D
from core.group import Group, transformed_mesh
from core.history import Command
from core.mesh import Edge, Mesh, edge_flags, stamp_edge_flags
from .styles import (KEY, DEFAULT_WIDTH, MIN_WIDTH, MAX_WIDTH, DEFAULT_PATTERN,
                     validated_color, validated_width, validated_pattern,
                     group_style, edge_styles, write_edge_styles, contains_segment)


def group_color(group):
    style = group_style(group)
    return style[0] if style else None


def group_width(group):
    style = group_style(group)
    return style[1] if style else DEFAULT_WIDTH


def group_pattern(group):
    style = group_style(group)
    return style[2] if style else DEFAULT_PATTERN


def is_line_group(group):
    return (isinstance(group, Group)
            and not group.billboard and not group.text3d
            and all(is_line_group(child) for child in group.children)
            and bool(group.mesh.edges or group.children))


def make_line(a, b, color, layer=None, flags=None, width_px=DEFAULT_WIDTH, pattern=DEFAULT_PATTERN):
    color = validated_color(color)
    width_px = validated_width(width_px)
    pattern = validated_pattern(pattern)
    if (QVector3D(b) - QVector3D(a)).length() < 1e-8:
        raise ValueError("La línea debe tener una longitud mayor que cero.")
    mesh = Mesh()
    edge = mesh.add_edge(QVector3D(a), QVector3D(b))
    if flags is not None:
        stamp_edge_flags(edge, flags)
    group = Group(mesh, name="Línea de color")
    group.layer = layer
    group.ext = {KEY: {"color": color, "width_px": width_px, "pattern": pattern}}
    return group


def set_color(group, color, width_px=None, pattern=None):
    data = deepcopy(group.ext or {})
    if color is None:
        marker = bool(data.get(KEY, {}).get("drawing_mesh"))
        data.pop(KEY, None)
        if marker:
            data[KEY] = {"drawing_mesh": True}
    else:
        style = deepcopy(data.get(KEY, {}))
        style["color"] = validated_color(color)
        if width_px is not None:
            style["width_px"] = validated_width(width_px)
        if pattern is not None:
            style["pattern"] = validated_pattern(pattern)
        for item in style.get("edges", ()):
            item["color"] = validated_color(color)
            if width_px is not None:
                item["width_px"] = validated_width(width_px)
            if pattern is not None:
                item["pattern"] = validated_pattern(pattern)
        data[KEY] = style
    group.ext = data or None


def is_legacy_container(group):
    """Only the previous plugin's segment containers qualify for migration."""
    return (group is not None and group.name in ("JA LineaStyle", "LineaStyle", "Líneas de colores")
            and not group.mesh.edges and bool(group.children)
            and all(not child.children and not child.mesh.faces and group_color(child)
                    for child in group.children))


class CreateLine(Command):
    def __init__(self, a, b, color, layer=None, width_px=DEFAULT_WIDTH):
        self.group = make_line(a, b, color, layer, width_px=width_px)
        self.owner = None

    def do(self, scene):
        if self.owner is None:
            context = scene.edit_group
            self.owner = context.children if context is not None else scene.groups
            if context is not None and context.xform is not None:
                inv, ok = context.xform.inverted()
                if not ok:
                    raise ValueError("El grupo abierto tiene una transformación singular.")
                self.group.mesh = transformed_mesh(self.group.mesh, inv)
        self.owner.append(self.group)
        # Drawing keeps the new line's own colour visible. Picking it later
        # uses the host's standard orange selection highlight.
        scene.selection.clear()
        scene.version += 1

    def undo(self, scene):
        if self.group in self.owner:
            self.owner.remove(self.group)
        scene.selection.discard(self.group)
        scene.version += 1


class DrawingSession:
    """One selectable container for the lifetime of the drawing tool."""
    def __init__(self, viewport):
        self.scene = viewport.scene
        self.history = viewport.history
        self.context = self.scene.edit_group
        self.owner = self.context.children if self.context is not None else self.scene.groups
        # An open plugin group is already the shared drawing mesh. No child
        # container is needed: drawing here can extend its existing planes.
        self.group = (self.context if self.context is not None and
                      (group_color(self.context) or (self.context.ext or {}).get(KEY, {}).get("drawing_mesh"))
                      or is_legacy_container(self.context)
                      else Group(name="JA LineaStyle"))
        self.attached = self.group is self.context
        if not self.attached:
            self.group.xform = QMatrix4x4()
            self.group.component = False
        self.first_command = None

    def can_continue(self, viewport):
        if (viewport.scene is not self.scene or viewport.history is not self.history
                or viewport.scene.edit_group is not self.context):
            return False
        owner = self.context.children if self.context is not None else self.scene.groups
        if owner is not self.owner:
            return False
        if self.attached:
            return True
        # Undoing all the segments leaves an empty, detached container. It
        # can be reused until its redo history is cleared or the document changes.
        return (self.first_command is None or self.group in self.owner
                or self.first_command in self.history.redo_stack)


class AddSessionSegment(Command):
    def __init__(self, session, a, b, color, width_px=DEFAULT_WIDTH, pattern=DEFAULT_PATTERN, eye=None):
        self.session = session
        self.group = session.group
        self.a, self.b = QVector3D(a), QVector3D(b)
        if (self.b - self.a).length() < 1e-8:
            raise ValueError("La línea debe tener una longitud mayor que cero.")
        self.style = validated_color(color), validated_width(width_px), validated_pattern(pattern)
        self.eye = eye
        self.before = self.after = None

    def do(self, scene):
        session = self.session
        if self.after is None:
            from core.edits import build_add_edge, build_add_edges
            group = self.group
            before_styles = edge_styles(group)
            old_segments = [(QVector3D(e.a), QVector3D(e.b), s) for e, s in before_styles.items()]
            self.before = group.mesh.capture_state(), deepcopy(group.ext), list(group.children)
            legacy = []
            if is_legacy_container(group):
                for child in group.children:
                    child_styles = edge_styles(child)
                    for edge, style in child_styles.items():
                        p, q = edge.a, edge.b
                        if child.xform is not None:
                            p, q = child.xform.map(p), child.xform.map(q)
                        legacy.append((QVector3D(p), QVector3D(q), style, edge.layer, edge_flags(edge)))
                old_segments.extend((p, q, style) for p, q, style, _layer, _flags in legacy)
            matrix = group.xform or QMatrix4x4()
            if not session.attached and session.context is not None and session.context.xform is not None:
                matrix = session.context.xform * matrix
            inverse, ok = matrix.inverted()
            if not ok:
                raise ValueError("El grupo tiene una transformación singular.")
            a, b = inverse.map(self.a), inverse.map(self.b)
            # Native planner handles shared vertices, crossings and planar
            # cycles on this mesh. Its commands never see the surrounding mesh.
            proxy = SimpleNamespace(mesh=group.mesh, edges=group.mesh.edges,
                                    faces=group.mesh.faces, selection=set(), version=scene.version,
                                    active_ifc=getattr(scene, "active_ifc", None))
            try:
                eye = inverse.map(self.eye) if self.eye is not None else None
                native = (build_add_edges(proxy, [(p, q) for p, q, *_ in legacy] + [(a, b)], eye=eye)
                          if legacy else build_add_edge(proxy, a, b, detect_faces=True, eye=eye))
                native.do(proxy)
                styles = {}
                for e in group.mesh.edges:
                    styles[e] = (self.style if contains_segment(a, b, e.a, e.b) else
                                 before_styles.get(e) or next((s for p, q, s in old_segments
                                                              if contains_segment(p, q, e.a, e.b)), self.style))
                    if legacy:
                        old = next((item for item in legacy if contains_segment(item[0], item[1], e.a, e.b)), None)
                        if old:
                            e.layer = old[3]
                            stamp_edge_flags(e, old[4])
                if legacy:
                    group.children.clear()
                set_color(group, group_color(group) or self.style[0])
                if "width_px" not in group.ext[KEY]:
                    group.ext[KEY].update(width_px=self.style[1], pattern=self.style[2])
                group.ext[KEY]["drawing_mesh"] = True
                write_edge_styles(group, styles)
                self.after = group.mesh.capture_state(), deepcopy(group.ext), list(group.children)
            except Exception:
                group.mesh.restore_state(self.before[0])
                group.ext = deepcopy(self.before[1])
                group.children[:] = self.before[2]
                raise
        else:
            self.group.mesh.restore_state(self.after[0])
            self.group.ext = deepcopy(self.after[1])
            self.group.children[:] = self.after[2]
        if not session.attached and session.group not in session.owner:
            session.owner.append(session.group)
        if session.first_command is None:
            session.first_command = self
        scene.selection.clear()
        scene.version += 1

    def undo(self, scene):
        container = self.session.group
        container.mesh.restore_state(self.before[0])
        container.ext = deepcopy(self.before[1])
        container.children[:] = self.before[2]
        if (not self.session.attached and not container.children and not container.mesh.edges
                and container in self.session.owner):
            self.session.owner.remove(container)
        scene.selection.discard(container)
        scene.selection.discard(self.group)
        scene.version += 1


class ColorSelection(Command):
    """Recolour line groups; isolate loose wires without changing any face."""
    def __init__(self, scene, color, width_px=None, pattern=None):
        self.color = None if color is None else validated_color(color)
        self.width_px = None if width_px is None else validated_width(width_px)
        self.pattern = None if pattern is None else validated_pattern(pattern)
        self.groups = []
        self.edges = []
        self.direct_edges = []
        context = scene.edit_group
        self.edge_group = context if context is not None and (group_color(context) or
                          (context.ext or {}).get(KEY, {}).get("drawing_mesh")) else None
        for entity in scene.selection:
            if isinstance(entity, Group):
                if not is_line_group(entity):
                    raise ValueError("Seleccione líneas libres o grupos que contengan solo líneas.")
                self._collect_groups(entity)
            elif isinstance(entity, Edge) and entity in scene.mesh.edges:
                if self.edge_group is not None:
                    self.direct_edges.append(entity)
                elif entity.faces:
                    raise ValueError("Esta versión no colorea por separado las aristas de una cara.")
                else:
                    self.edges.append(entity)
            else:
                raise ValueError("Seleccione líneas libres o grupos que contengan solo líneas.")
        if not self.groups and not self.edges and not self.direct_edges:
            raise ValueError("Seleccione primero las líneas que desea colorear.")
        if color is None:
            self.edges = []
        self.direct_styles = edge_styles(self.edge_group) if self.edge_group else {}
        for g in self.groups:
            edge_styles(g)
        self.before_ext = {g: deepcopy(g.ext) for g in self.groups}
        if self.direct_edges:
            self.before_ext[self.edge_group] = deepcopy(self.edge_group.ext)
        self.before_mesh = scene.mesh.capture_state()
        context = scene.edit_group
        self.owner = context.children if context is not None else scene.groups
        self.created = []
        if self.edges:
            group = Group(name="JA LineaStyle")
            group.xform = QMatrix4x4()
            group.component = False
            styles = {}
            for e in self.edges:
                copied = group.mesh.add_edge(e.a, e.b)
                stamp_edge_flags(copied, edge_flags(e))
                styles[copied] = self.color, self.width_px or DEFAULT_WIDTH, self.pattern or DEFAULT_PATTERN
            group.layer = self.edges[0].layer if all(e.layer == self.edges[0].layer for e in self.edges) else None
            set_color(group, self.color, self.width_px or DEFAULT_WIDTH, self.pattern or DEFAULT_PATTERN)
            group.ext[KEY]["drawing_mesh"] = True
            write_edge_styles(group, styles)
            self.created = [group]
        if context is not None and context.xform is not None:
            inv, ok = context.xform.inverted()
            if not ok:
                raise ValueError("El grupo abierto tiene una transformación singular.")
            for group in self.created:
                group.mesh = transformed_mesh(group.mesh, inv)
        self.after_mesh = None

    def _collect_groups(self, group):
        if group not in self.groups:
            self.groups.append(group)
            for child in group.children:
                self._collect_groups(child)

    @property
    def changed(self):
        return bool(self.edges or self.direct_edges or any(
            group_color(g) != self.color
            or (self.width_px is not None and group_width(g) != self.width_px)
            or (self.pattern is not None and group_pattern(g) != self.pattern)
            or any(s[0] != self.color or (self.width_px is not None and s[1] != self.width_px)
                   or (self.pattern is not None and s[2] != self.pattern) for s in edge_styles(g).values())
            or (self.color is None and bool(group_color(g))) for g in self.groups))

    def do(self, scene):
        try:
            for group in self.groups:
                set_color(group, self.color, self.width_px, self.pattern)
            if self.direct_edges:
                styles = dict(self.direct_styles)
                for edge in self.direct_edges:
                    previous = styles.get(edge, (self.color, DEFAULT_WIDTH, DEFAULT_PATTERN))
                    # Reset selected edges to the group's default. A full
                    # group reset removes every plugin property at once.
                    styles[edge] = (group_style(self.edge_group) if self.color is None else
                                    (self.color, self.width_px or previous[1], self.pattern or previous[2]))
                write_edge_styles(self.edge_group, styles)
            if self.edges:
                if self.after_mesh is None:
                    for edge in self.edges:
                        scene.mesh.remove_edge(edge)
                    self.after_mesh = scene.mesh.capture_state()
                else:
                    scene.mesh.restore_state(self.after_mesh)
                self.owner.extend(self.created)
            scene.selection.clear()
            scene.version += 1
        except Exception:
            self._restore(scene)
            raise

    def _restore(self, scene):
        for group, ext in self.before_ext.items():
            group.ext = deepcopy(ext)
        for group in self.created:
            if group in self.owner:
                self.owner.remove(group)
        if self.edges:
            scene.mesh.restore_state(self.before_mesh)

    def undo(self, scene):
        self._restore(scene)
        scene.selection.clear()
        scene.version += 1


def styled_segments(scene, interactive=True, highlight=False):
    """Live endpoints; parent transforms, tags, hiding and selection included."""
    out = {}

    def walk(group, parent_matrix=None, inherited=None, selected=False):
        if not scene.entity_visible(group):
            return
        matrix = group.xform
        if parent_matrix is not None:
            matrix = parent_matrix * matrix if matrix is not None else parent_matrix
        own_color = group_color(group)
        style = group_style(group) if own_color else inherited
        per_edge = edge_styles(group)
        selected = selected or group in scene.selection
        if style and not (interactive and selected and not highlight):
            for edge in group.mesh.edges:
                if edge.hidden or edge.soft or not scene.entity_visible(edge):
                    continue
                edge_selected = selected or edge in scene.selection
                if interactive and edge_selected and not highlight:
                    continue
                a, b = edge.a, edge.b
                if matrix is not None:
                    a, b = matrix.map(a), matrix.map(b)
                edge_style = per_edge.get(edge, style)
                if interactive and edge_selected:
                    edge_style = ("#f27329", edge_style[1], edge_style[2])
                out.setdefault(edge_style, []).append((QVector3D(a), QVector3D(b)))
        for child in group.children:
            walk(child, matrix, style, selected)

    for group in scene.groups:
        walk(group)
    return out


def color_segments(scene, interactive=True):
    """Compatibility helper for consumers that do not need the width."""
    out = {}
    for (color, _width, _pattern), segments in styled_segments(scene, interactive).items():
        out.setdefault(color, []).extend(segments)
    return out

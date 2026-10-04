# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""Depth-tested colour pass for the IngeTrazo 0.5.7 viewport.

API 2 has only screen overlays, so this narrowly scoped adapter wraps the
viewport's preview pass while its native shader and scene FBO are bound.
It reuses the scratch preview buffer; the actual preview refills it afterwards.
No host source file is modified. Raster render_image also uses this pass.
"""
from array import array
from inspect import signature
import logging
import math

from PySide6.QtGui import QColor
from .model import styled_segments
from .styles import group_style
from .patterns import patterned_segments

log = logging.getLogger("ingetrazo.plugins.lineas_color")


def width_offsets(pixels, width, height):
    """Screen-space disc: works on drivers that only support 1-px GL lines."""
    if pixels <= 1.0:
        return [(0.0, 0.0)]
    radius = (pixels - 1.0) / 2.0
    count = math.ceil(pixels)
    values = [-radius + 2.0 * radius * i / (count - 1) for i in range(count)]
    offsets = [(0.0, 0.0)]
    for dx in values:
        for dy in values:
            if dx * dx + dy * dy <= radius * radius + 0.51 and (dx or dy):
                offsets.append((2.0 * dx / max(width, 1), 2.0 * dy / max(height, 1)))
    return offsets


class ColorRenderer:
    def __init__(self, viewport):
        self.viewport = viewport
        self.original = viewport._draw_rubber_band
        self.chunk = viewport._group_chunk
        self.eligible = viewport._instanced_eligible
        self.placements = viewport._placements
        self.sync = viewport._sync_edges
        self.hover = viewport._upload_hover_edge
        self.pick = viewport._pick_index
        # The shipped macOS 0.5.7 binary predates the optional `near` query
        # present in the newer source with that same application version.
        self._pick_with_near = "near" in signature(self.pick).parameters
        self._picking = 0
        self.failed = False
        self.sources = {}
        self.inherited = {}

    def install(self):
        self.viewport._draw_rubber_band = self.draw
        self.viewport._group_chunk = self.filtered_chunk
        self.viewport._instanced_eligible = self.filtered_eligible
        self.viewport._placements = self.styled_placements
        self.viewport._sync_edges = self.filtered_sync
        self.viewport._upload_hover_edge = self.filtered_hover
        self.viewport._pick_index = self.picking_index
        # Discard any index made with a filtered draw chunk before installation.
        self.viewport._pick_index_cache = None
        self.viewport._pick_block = None

    def styled_placements(self):
        placements = self.placements()
        proxies = getattr(self.viewport, "_placement_proxies", {})
        self.sources, self.inherited = {}, {}

        def walk(group, inherited=None):
            own = group_style(group) or inherited
            self.inherited[id(group)] = own
            proxy = proxies.get(id(group))
            if proxy is not None:
                self.sources[id(proxy)] = group
                self.inherited[id(proxy)] = own
            for child in group.children:
                walk(child, own)

        for root in self.viewport.scene.groups:
            walk(root)
        return placements

    def has_style(self, group):
        source = self.sources.get(id(group), group)
        return not self.failed and bool(group_style(source) or self.inherited.get(id(group)))

    def filtered_chunk(self, group):
        chunk = self.chunk(group)
        if not self._picking and self.has_style(group):
            # Hide the continuous underlay only while building DRAW buffers.
            # The host also reads this array to build its snap/pick index.
            return dict(chunk, edges=b"")
        return chunk

    def picking_index(self, near=None):
        """Let native picking use full edges, including visual pattern gaps."""
        self._picking += 1
        try:
            if self._pick_with_near:
                return self.pick(near=near)
            return self.pick()
        finally:
            self._picking -= 1

    def filtered_eligible(self, group):
        return False if self.has_style(group) else self.eligible(group)

    def styled_edge(self, edge):
        return any(self.has_style(g) and edge in g.mesh.edges
                   for g in self.viewport._placements())

    def filtered_sync(self):
        scene = self.viewport.scene
        selection = scene.selection
        # Native selection boxes/edge cues could join the pattern's gaps.
        # Our pass draws the same styled segments in selection orange.
        from core.group import Group
        from core.mesh import Edge
        self.styled_placements()
        mask_key = tuple((id(g), self.has_style(g)) for g in self.viewport._placements())
        if mask_key != getattr(self, "mask_key", None):
            self.mask_key = mask_key
            self.viewport._edge_groups_cache = None
            self.viewport._edges_version = -1
            self.viewport._inst_pool = None
        scene.selection = {e for e in selection
                           if not (isinstance(e, Group) and self.has_style(e))
                           and not (isinstance(e, Edge) and self.styled_edge(e))}
        try:
            self.sync()
        finally:
            scene.selection = selection

    def filtered_hover(self, edge):
        return 0 if self.styled_edge(edge) else self.hover(edge)

    def draw(self):
        if not self.failed:
            try:
                self.draw_colors()
            except Exception:
                self.failed = True
                self.viewport._edges_version = -1
                self.viewport._edge_groups_cache = None
                self.viewport.update()
                log.exception("JA LineaStyle: se desactivó el pase de color.")
                self.viewport.flash_status(
                    "JA LineaStyle: el renderizador no es compatible; las líneas se conservan.",
                    8000)
        tool = self.viewport.active_tool
        if self.failed or not getattr(tool, "is_color_line_tool", False):
            self.original()
        else:
            # Our preview uses the same chosen width as committed lines.
            self.viewport._overlay_rubber = None

    def draw_colors(self):
        from views.viewport import (GL_DEPTH_TEST, GL_FALSE, GL_TRUE, GL_LEQUAL,
                                    GL_LINES, _shifted_mvp)
        vp = self.viewport
        style = vp._frame_style
        interactive = vp._export_size is None
        batches = (styled_segments(vp.scene, interactive=interactive, highlight=True)
                   if style.edges or style.face_mode == "wireframe" else {})
        tool = vp.active_tool
        if interactive and getattr(tool, "is_color_line_tool", False):
            preview = tool.rubber_band_lines()
            if preview:
                batches.setdefault((tool.controller.color, tool.controller.width_px,
                                    tool.controller.pattern), []).extend(preview)
        if not batches:
            return
        # paintGL disables depth testing immediately before this hook for
        # ordinary drawing tools. Restore that exact expected state afterwards.
        preview_depth = bool(getattr(vp.active_tool, "wireframe_depth_tested", False))
        mvp = vp.camera.projection_matrix() * vp.camera.view_matrix()
        width, height = vp._export_size or vp._fb_size()
        scale = vp.devicePixelRatioF() if interactive else width / max(vp.width(), 1)
        vp._gl.glEnable(GL_DEPTH_TEST)
        vp._gl.glDepthFunc(GL_LEQUAL)
        vp._gl.glDepthMask(GL_FALSE)
        vp._set_section_clip(True)
        try:
            for (color, line_width, pattern), segments in batches.items():
                pixels = line_width * scale
                if not interactive:
                    pixels = max(pixels, float(vp._export_edge_px))
                offsets = width_offsets(pixels, width, height)
                segments = patterned_segments(segments, pattern, mvp, width, height, pixels)
                data = array("f")
                for a, b in segments:
                    data.extend((*a.toTuple(), *b.toTuple()))
                raw = data.tobytes()
                vp._rubber_vbo.bind()
                vp._rubber_vbo.allocate(raw, len(raw))
                vp._rubber_vbo.release()
                c = QColor(color)
                vp._set_color(c.redF(), c.greenF(), c.blueF(), 1.0)
                vp._rubber_vao.bind()
                try:
                    for dx, dy in offsets:
                        vp._program.setUniformValue(vp._loc_mvp, _shifted_mvp(mvp, dx, dy))
                        vp._gl.glDrawArrays(GL_LINES, 0, len(data) // 3)
                finally:
                    vp._rubber_vao.release()
        finally:
            vp._program.setUniformValue(vp._loc_mvp, mvp)
            vp._set_section_clip(False)
            vp._gl.glDepthMask(GL_TRUE)
            if not preview_depth:
                vp._gl.glDisable(GL_DEPTH_TEST)

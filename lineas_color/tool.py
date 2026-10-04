# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""Reuse native line snapping, axis locks, chains and typed lengths."""
from tools.line import LineTool
from .model import AddSessionSegment, DrawingSession


class ColorLineTool(LineTool):
    shortcut = None
    wireframe_depth_tested = True
    is_color_line_tool = True
    icon = None

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.session = None

    @property
    def name(self):
        return self.controller.tr("JA LineaStyle · Línea")

    @property
    def description(self):
        return self.controller.tr("Dibujar líneas conectadas y planos con color, grosor y estilo.")

    @property
    def vcb_label(self):
        return self.controller.tr("Longitud")

    def on_activate(self, viewport):
        super().on_activate(viewport)
        self.session = None

    def on_deactivate(self, viewport):
        super().on_deactivate(viewport)
        self.session = None

    @property
    def qt_cursor(self):
        from .cursor import pencil_cursor
        viewport = self.controller.app.viewport
        return pencil_cursor(self.controller.color, viewport.devicePixelRatioF())

    @property
    def wireframe_color(self):
        from PySide6.QtGui import QColor
        color = QColor(self.controller.color)
        return (color.redF(), color.greenF(), color.blueF(), 1.0)

    def _commit_edge(self, viewport, start, end):
        if self.session is None or not self.session.can_continue(viewport):
            self.session = DrawingSession(viewport)
        return AddSessionSegment(self.session, start, end, self.controller.color,
                                 self.controller.width_px, self.controller.pattern,
                                 eye=viewport.camera.eye())

    def rubber_band_lines(self):
        if self.controller.app.viewport._export_size is not None:
            return []
        return super().rubber_band_lines()

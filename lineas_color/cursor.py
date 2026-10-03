# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""A coloured pencil whose precise tip is the native mouse hotspot."""
from functools import lru_cache
import math

from PySide6.QtCore import Qt, QLineF, QRectF
from PySide6.QtGui import QColor, QCursor, QPainter, QPainterPath, QPen, QPixmap

from .styles import validated_color

CURSOR_SIZE = 32
PENCIL_TIP = (4, 28)


def pencil_cursor(color, device_pixel_ratio=1.0):
    """Logical 32-px cursor; draw at the display's physical resolution."""
    dpr = float(device_pixel_ratio)
    if not math.isfinite(dpr) or dpr <= 0:
        dpr = 1.0
    return _pencil_cursor(validated_color(color), round(max(1.0, dpr), 3))


@lru_cache(maxsize=64)
def _pencil_cursor(color, dpr):
    pixels = round(CURSOR_SIZE * dpr)
    art = QPixmap(pixels, pixels)
    art.setDevicePixelRatio(pixels / CURSOR_SIZE)
    art.fill(Qt.GlobalColor.transparent)
    ink = QColor(color)
    outline = QColor("#263238")
    painter = QPainter(art)
    try:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(*PENCIL_TIP)
        painter.rotate(-45)

        shape = QPainterPath()
        shape.moveTo(0, 0)
        shape.lineTo(6, -3.5)
        shape.lineTo(29, -3.5)
        shape.quadTo(31, -3.5, 31, -1.5)
        shape.lineTo(31, 1.5)
        shape.quadTo(31, 3.5, 29, 3.5)
        shape.lineTo(6, 3.5)
        shape.closeSubpath()
        # Two outlines keep black and white pencils readable on either
        # a light model background or a dark face.
        painter.setPen(QPen(QColor("#ffffff"), 3, Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.setBrush(ink)
        painter.drawPath(shape)
        painter.setPen(QPen(outline, 1, Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.drawPath(shape)

        painter.setPen(QPen(QColor(255, 255, 255, 100), 0.9))
        painter.drawLine(QLineF(8, -1.8, 24, -1.8))
        painter.setPen(QPen(outline, 0.8))
        painter.setBrush(QColor("#cbd5dd"))
        painter.drawRect(QRectF(25.5, -3.5, 2, 7))

        wood = QPainterPath()
        wood.moveTo(0, 0)
        wood.lineTo(6, -3.5)
        wood.lineTo(6, 3.5)
        wood.closeSubpath()
        painter.setBrush(QColor("#f2d2a5"))
        painter.drawPath(wood)
        tip = QPainterPath()
        tip.moveTo(0, 0)
        tip.lineTo(2.7, -1.55)
        tip.lineTo(2.7, 1.55)
        tip.closeSubpath()
        painter.setBrush(ink)
        painter.drawPath(tip)
    finally:
        painter.end()
    return QCursor(art, *PENCIL_TIP)

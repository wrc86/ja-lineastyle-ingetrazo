# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""Split ONLY the display pass into pixel-sized dashes; geometry stays whole."""
import math

from PySide6.QtGui import QVector4D
from .styles import PATTERN_LENGTHS


def patterned_segments(segments, pattern, mvp, width, height, unit):
    lengths = PATTERN_LENGTHS[pattern]
    if not lengths:
        return segments
    lengths = tuple(value * unit for value in lengths)
    period = sum(lengths)
    out = []
    for a, b in segments:
        ca, cb = mvp.map(QVector4D(a, 1)), mvp.map(QVector4D(b, 1))
        # Homogeneous frustum clipping bounds work before perspective divide.
        # It bounds processing even for a line millions of pixels off screen,
        # and safely handles lines crossing the eye/near plane.
        lo, hi = 0.0, 1.0
        for f in (lambda c: c.w() - c.x(), lambda c: c.w() + c.x(),
                  lambda c: c.w() - c.y(), lambda c: c.w() + c.y(),
                  lambda c: c.w() - c.z(), lambda c: c.w() + c.z(),
                  lambda c: c.w() - 1e-7):
            fa, fb = f(ca), f(cb)
            if fa < 0 and fb < 0:
                hi = -1
                break
            if fa < 0:
                lo = max(lo, fa / (fa - fb))
            elif fb < 0:
                hi = min(hi, fa / (fa - fb))
        if lo >= hi:
            continue
        c0, c1 = ca + (cb - ca) * lo, ca + (cb - ca) * hi
        x0, y0 = c0.x() / c0.w() * width / 2, c0.y() / c0.w() * height / 2
        x1, y1 = c1.x() / c1.w() * width / 2, c1.y() / c1.w() * height / 2
        distance = math.hypot(x1 - x0, y1 - y0)
        if distance < 1e-6:
            continue
        phase = 0.0
        if ca.w() > 1e-7:
            phase = math.hypot(x0 - ca.x() / ca.w() * width / 2,
                               y0 - ca.y() / ca.w() * height / 2) % period
        # Projective interpolation: equal screen distances are NOT equal
        # world fractions when the segment runs towards/away from the eye.
        def at(pixel):
            u = min(1.0, max(0.0, pixel / distance))
            t = u * c0.w() / ((1 - u) * c1.w() + u * c0.w())
            return a + (b - a) * (lo + (hi - lo) * t)

        cursor = -phase
        while cursor < distance:
            for i, length in enumerate(lengths):
                end = cursor + length
                if i % 2 == 0 and end > 0 and cursor < distance:
                    out.append((at(max(0.0, cursor)), at(min(distance, end))))
                cursor = end
    return out

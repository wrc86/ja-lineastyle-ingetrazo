# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""JA LineaStyle 3D for IngeTrazo's extension API 2."""

__version__ = "0.1.2"
__license__ = "GPL-3.0-or-later"
__author__ = "Julio Angulo"
__plugin_name__ = "JA LineaStyle"


def setup(app):
    if getattr(app, "api_version", 0) < 2:
        raise RuntimeError("JA LineaStyle requiere la API de extensiones 2.")
    controllers = getattr(app.window, "_lineas_color_controllers", None)
    if controllers is None:
        controllers = app.window._lineas_color_controllers = {}
    if app.key in controllers:
        return controllers[app.key]
    from .controller import Controller
    controller = Controller(app)
    controller.install()
    controllers[app.key] = controller
    return controller

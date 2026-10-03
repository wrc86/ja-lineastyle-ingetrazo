# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
from pathlib import Path
from PySide6.QtCore import QEvent, QObject, QTimer, QSize
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (QColorDialog, QComboBox, QDoubleSpinBox, QGridLayout, QLabel, QPushButton,
                               QTabBar, QVBoxLayout, QWidget)
from .model import ColorSelection, DEFAULT_WIDTH, MIN_WIDTH, MAX_WIDTH, validated_color
from .render import ColorRenderer
from .styles import (PATTERNS, DEFAULT_PATTERN, validated_pattern, install_edit_sync,
                     sync_scene_styles)

PALETTE = (("Rojo", "#e53935"), ("Naranja", "#fb8c00"),
           ("Amarillo", "#fdd835"), ("Verde", "#43a047"),
           ("Azul", "#1e88e5"), ("Violeta", "#8e24aa"),
           ("Negro", "#20252b"), ("Blanco", "#ffffff"))


class _PanelTabIcon(QObject):
    """Qt dock tabs require their own icon, including after relayout."""
    def __init__(self, window, dock, icon):
        super().__init__(dock)
        self.window, self.dock, self.icon = window, dock, icon
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.update_icon)
        window.installEventFilter(self)
        dock.installEventFilter(self)
        dock.visibilityChanged.connect(self.queue_update)
        dock.dockLocationChanged.connect(self.queue_update)
        self.queue_update()

    def queue_update(self, *_args):
        if not self.timer.isActive():
            self.timer.start(0)

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Type.ChildAdded, QEvent.Type.LayoutRequest,
                            QEvent.Type.Show, QEvent.Type.ParentChange):
            self.queue_update()
        return False

    def update_icon(self):
        for bar in self.window.findChildren(QTabBar):
            for index in range(bar.count()):
                if (bar.tabText(index) == self.dock.windowTitle()
                        and bar.tabIcon(index).cacheKey() != self.icon.cacheKey()):
                    bar.setTabIcon(index, self.icon)


class Controller:
    def __init__(self, app):
        self.app = app
        self.color = "#e53935"
        self.width_px = DEFAULT_WIDTH
        self.pattern = DEFAULT_PATTERN
        self.tool = None
        self.renderer = None

    def install(self):
        vp = self.app.viewport
        needed = ("_draw_rubber_band", "_set_section_clip", "_line_jitter", "_fb_size",
                  "_group_chunk", "_instanced_eligible", "_placements", "_sync_edges", "_upload_hover_edge",
                  "_pick_index")
        if not all(callable(getattr(vp, method, None)) for method in needed):
            raise RuntimeError("Esta versión de IngeTrazo no admite el renderizador de JA LineaStyle.")
        self.panel = QWidget()
        layout = QVBoxLayout(self.panel)
        intro = QLabel("Elija un color y dibuje una línea en el modelo 3D.")
        intro.setWordWrap(True)
        layout.addWidget(intro)
        grid = QGridLayout()
        for index, (name, color) in enumerate(PALETTE):
            button = QPushButton(name)
            button.setToolTip(color)
            ink = "#20252b" if name in ("Blanco", "Amarillo") else "white"
            button.setStyleSheet(f"background-color: {color}; color: {ink}; padding: 6px;")
            button.clicked.connect(lambda _checked=False, c=color: self.choose(c))
            grid.addWidget(button, index // 2, index % 2)
        layout.addLayout(grid)
        self.custom_button = QPushButton("Otro color…")
        self.custom_button.clicked.connect(self.choose_custom)
        layout.addWidget(self.custom_button)
        self.current_label = QLabel()
        layout.addWidget(self.current_label)
        width_grid = QGridLayout()
        width_grid.addWidget(QLabel("Grosor visual:"), 0, 0)
        self.width_spin = QDoubleSpinBox()
        self.width_spin.setRange(MIN_WIDTH, MAX_WIDTH)
        self.width_spin.setDecimals(1)
        self.width_spin.setSingleStep(0.5)
        self.width_spin.setSuffix(" px")
        self.width_spin.setValue(self.width_px)
        self.width_spin.setToolTip("Grosor en pantalla. Se guarda con la línea; no añade espesor físico.")
        self.width_spin.valueChanged.connect(self.choose_width)
        width_grid.addWidget(self.width_spin, 0, 1)
        layout.addLayout(width_grid)
        pattern_grid = QGridLayout()
        pattern_grid.addWidget(QLabel("Estilo de línea:"), 0, 0)
        self.pattern_combo = QComboBox()
        for key, label, _lengths in PATTERNS:
            self.pattern_combo.addItem(label, key)
        self.pattern_combo.currentIndexChanged.connect(self.choose_pattern)
        pattern_grid.addWidget(self.pattern_combo, 0, 1)
        layout.addLayout(pattern_grid)
        self.draw_button = QPushButton("Dibujar línea de color")
        self.draw_button.clicked.connect(self.start_drawing)
        layout.addWidget(self.draw_button)
        self.apply_button = QPushButton("Aplicar a la selección")
        self.apply_button.clicked.connect(lambda: self.apply())
        layout.addWidget(self.apply_button)
        reset = QPushButton("Restaurar estilo")
        reset.clicked.connect(lambda: self.apply(reset=True))
        layout.addWidget(reset)
        help_text = QLabel("Dos clics crean un segmento. Puede escribir su longitud. "
                           "Esc termina el tramo. Todas las líneas quedan en el mismo grupo "
                           "mientras siga activa esta herramienta.\n\n"
                           "Los segmentos comparten vértices. Cerrar un contorno coplanar crea una cara. "
                           "Abra el grupo con doble clic para continuar sobre sus planos.\n\n"
                           "Tome referencias en extremos, puntos medios, cruces y aristas visibles. "
                           "Después del primer clic, pase sobre una arista y pulse ↓ para "
                           "fijar una paralela; pulse ↓ otra vez para una perpendicular.\n\n"
                           "Para cambiar color, grosor y estilo: seleccione líneas o su grupo "
                           "y pulse Aplicar.")
        help_text.setWordWrap(True)
        layout.addWidget(help_text)
        layout.addStretch(1)
        self.dock = self.app.add_panel("LineaStyle", self.panel)
        # Menu pixmaps do not depend on the host's optional SVG icon engine.
        self.icon = QIcon()
        for size in (16, 32, 64, 128):
            self.icon.addFile(str(Path(__file__).parent / "icons" / f"ja_lineastyle_{size}.png"),
                              QSize(size, size))
        self.dock.setWindowIcon(self.icon)
        self.tab_icon = _PanelTabIcon(self.app.window, self.dock, self.icon)
        self.menu_action = self.app.add_menu_action("JA LineaStyle…", lambda: self.app.show_panel(self.dock),
                                                    tip="Dibujar y recolorear líneas del modelo 3D.")
        if self.menu_action is not None:
            self.menu_action.setIcon(self.icon)
            self.menu_action.setIconVisibleInMenu(True)
        self.app.add_context_menu(self.context_menu)
        self.renderer = ColorRenderer(vp)
        self.renderer.install()
        install_edit_sync(vp.scene)
        self.app.on_document_changed(lambda: sync_scene_styles(vp.scene))
        self.choose(self.color)

    def choose(self, color):
        self.color = validated_color(color)
        self.current_label.setText(f"Color actual: {self.color.upper()}")
        vp = self.app.viewport
        if (self.tool is not None and vp.active_tool is self.tool and vp.nav_mode is None
                and vp._last_pos is None and vp._look_drag is None):
            vp._apply_tool_cursor()
        vp.update()

    def choose_width(self, value):
        self.width_px = float(value)
        self.app.viewport.update()

    def choose_pattern(self, _index):
        self.pattern = validated_pattern(self.pattern_combo.currentData())
        self.app.viewport.update()

    def choose_custom(self):
        color = QColorDialog.getColor(QColor(self.color), self.app.window,
                                       "Color de la línea", QColorDialog.DontUseNativeDialog)
        if color.isValid():
            self.choose(color.name())

    def start_drawing(self):
        from .tool import ColorLineTool
        if self.tool is None:
            self.tool = ColorLineTool(self)
        self.app.viewport.set_active_tool(self.tool)
        self.app.viewport.setFocus()
        self.app.viewport.flash_status("Línea de color: indique el punto inicial y el final.", 4000)

    def apply(self, reset=False, include_width=True):
        vp = self.app.viewport
        try:
            command = ColorSelection(vp.scene, None if reset else self.color,
                                     None if reset or not include_width else self.width_px,
                                     None if reset or not include_width else self.pattern)
            if not command.changed:
                vp.flash_status("La selección ya tiene ese estilo.", 3000)
                return
            vp.history.execute(command)
            if vp.history.last_error:
                vp.flash_status(vp.history.last_error, 8000)
                return
            vp.notify_scene_changed()
            vp.update()
            vp.flash_status("Estilo restaurado." if reset else "Propiedades aplicadas a las líneas.", 4000)
        except ValueError as exc:
            vp.flash_status(str(exc), 6000)

    def context_menu(self, menu, selection):
        if not selection:
            return
        submenu = menu.addMenu("JA LineaStyle")
        submenu.setIcon(self.icon)
        submenu.menuAction().setIconVisibleInMenu(True)
        for name, color in PALETTE:
            action = submenu.addAction(name)
            action.triggered.connect(lambda _checked=False, c=color:
                                     QTimer.singleShot(0, lambda: self.apply_color(c)))
        action = submenu.addAction("Restaurar estilo")
        action.triggered.connect(lambda _checked=False:
                                 QTimer.singleShot(0, lambda: self.apply(reset=True)))

    def apply_color(self, color):
        self.choose(color)
        self.apply(include_width=False)

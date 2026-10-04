# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
from pathlib import Path
from PySide6.QtCore import QEvent, QObject, QTimer, QSize
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (QColorDialog, QComboBox, QDialog, QDoubleSpinBox, QGridLayout, QLabel, QPushButton,
                               QTabBar, QVBoxLayout, QWidget)
from .model import ColorSelection, DEFAULT_WIDTH, MIN_WIDTH, MAX_WIDTH, validated_color
from .i18n import HELP, LANGUAGES, Translator
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
        self.translator = Translator()

    def tr(self, source, **values):
        return self.translator.tr(source, **values)

    def install(self):
        vp = self.app.viewport
        needed = ("_draw_rubber_band", "_set_section_clip", "_line_jitter", "_fb_size",
                  "_group_chunk", "_instanced_eligible", "_placements", "_sync_edges", "_upload_hover_edge",
                  "_pick_index")
        if not all(callable(getattr(vp, method, None)) for method in needed):
            raise RuntimeError(self.tr("Esta versión de IngeTrazo no admite el renderizador de JA LineaStyle."))
        self.panel = QWidget()
        layout = QVBoxLayout(self.panel)
        language_grid = QGridLayout()
        self.language_label = QLabel()
        language_grid.addWidget(self.language_label, 0, 0)
        self.language_combo = QComboBox()
        for code, name in LANGUAGES:
            self.language_combo.addItem(name, code)
        self.language_combo.setCurrentIndex(self.language_combo.findData(self.translator.language))
        self.language_combo.currentIndexChanged.connect(self.choose_language)
        language_grid.addWidget(self.language_combo, 0, 1)
        layout.addLayout(language_grid)
        self.intro = QLabel()
        self.intro.setWordWrap(True)
        layout.addWidget(self.intro)
        grid = QGridLayout()
        self.palette_buttons = []
        for index, (name, color) in enumerate(PALETTE):
            button = QPushButton(name)
            self.palette_buttons.append((button, name))
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
        self.width_label = QLabel()
        width_grid.addWidget(self.width_label, 0, 0)
        self.width_spin = QDoubleSpinBox()
        self.width_spin.setRange(MIN_WIDTH, MAX_WIDTH)
        self.width_spin.setDecimals(1)
        self.width_spin.setSingleStep(0.5)
        self.width_spin.setSuffix(" px")
        self.width_spin.setValue(self.width_px)
        self.width_spin.valueChanged.connect(self.choose_width)
        width_grid.addWidget(self.width_spin, 0, 1)
        layout.addLayout(width_grid)
        pattern_grid = QGridLayout()
        self.pattern_label = QLabel()
        pattern_grid.addWidget(self.pattern_label, 0, 0)
        self.pattern_combo = QComboBox()
        self.pattern_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.pattern_combo.setMinimumContentsLength(12)
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
        self.reset_button = QPushButton()
        self.reset_button.clicked.connect(lambda: self.apply(reset=True))
        layout.addWidget(self.reset_button)
        self.help_label = QLabel()
        self.help_label.setWordWrap(True)
        layout.addWidget(self.help_label)
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
                                                    tip=self.tr("Dibujar y recolorear líneas del modelo 3D."))
        if self.menu_action is not None:
            self.menu_action.setIcon(self.icon)
            self.menu_action.setIconVisibleInMenu(True)
        self.app.add_context_menu(self.context_menu)
        self.renderer = ColorRenderer(vp, translate=self.tr)
        self.renderer.install()
        install_edit_sync(vp.scene)
        self.app.on_document_changed(lambda: sync_scene_styles(vp.scene))
        self.retranslate()
        self.choose(self.color)

    def choose_language(self, _index):
        self.translator.select(self.language_combo.currentData())
        self.retranslate()
        # Updating captions must preserve the active drawing chain and mesh.
        if self.tool is not None and self.app.viewport.active_tool is self.tool:
            refresh = getattr(self.app.window, "_refresh_vcb", None)
            if callable(refresh):
                refresh()
        self.app.viewport.update()

    def retranslate(self):
        self.language_label.setText(self.tr("Idioma:"))
        self.language_combo.setToolTip(self.tr("Idioma del panel y de los mensajes de LineaStyle."))
        self.intro.setText(self.tr("Elija un color y dibuje una línea en el modelo 3D."))
        for button, name in self.palette_buttons:
            button.setText(self.tr(name))
        self.custom_button.setText(self.tr("Otro color…"))
        self.current_label.setText(self.tr("Color actual: {color}", color=self.color.upper()))
        self.width_label.setText(self.tr("Grosor visual:"))
        self.width_spin.setToolTip(self.tr("Grosor en pantalla. Se guarda con la línea; no añade espesor físico."))
        self.pattern_label.setText(self.tr("Estilo de línea:"))
        for index, (_key, label, _lengths) in enumerate(PATTERNS):
            self.pattern_combo.setItemText(index, self.tr(label))
        self.draw_button.setText(self.tr("Dibujar línea de color"))
        self.apply_button.setText(self.tr("Aplicar a la selección"))
        self.reset_button.setText(self.tr("Restaurar estilo"))
        self.help_label.setText(self.tr(HELP))
        if self.menu_action is not None:
            self.menu_action.setStatusTip(self.tr("Dibujar y recolorear líneas del modelo 3D."))

    def choose(self, color):
        self.color = validated_color(color)
        self.current_label.setText(self.tr("Color actual: {color}", color=self.color.upper()))
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

    def create_color_dialog(self):
        dialog = QColorDialog(QColor(self.color), self.app.window)
        dialog.setOption(QColorDialog.DontUseNativeDialog)
        dialog.setWindowTitle(self.tr("Color de la línea"))
        self.translator.localize_color_dialog(dialog)
        return dialog

    def choose_custom(self):
        dialog = self.create_color_dialog()
        try:
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.choose(dialog.selectedColor().name())
        finally:
            dialog.deleteLater()

    def start_drawing(self):
        from .tool import ColorLineTool
        if self.tool is None:
            self.tool = ColorLineTool(self)
        self.app.viewport.set_active_tool(self.tool)
        self.app.viewport.setFocus()
        self.app.viewport.flash_status(self.tr("Línea de color: indique el punto inicial y el final."), 4000)

    def apply(self, reset=False, include_width=True):
        vp = self.app.viewport
        try:
            command = ColorSelection(vp.scene, None if reset else self.color,
                                     None if reset or not include_width else self.width_px,
                                     None if reset or not include_width else self.pattern)
            if not command.changed:
                vp.flash_status(self.tr("La selección ya tiene ese estilo."), 3000)
                return
            vp.history.execute(command)
            if vp.history.last_error:
                vp.flash_status(self.translator.error(vp.history.last_error), 8000)
                return
            vp.notify_scene_changed()
            vp.update()
            vp.flash_status(self.tr("Estilo restaurado." if reset else "Propiedades aplicadas a las líneas."), 4000)
        except ValueError as exc:
            vp.flash_status(self.translator.error(str(exc)), 6000)

    def context_menu(self, menu, selection):
        if not selection:
            return
        submenu = menu.addMenu("JA LineaStyle")
        submenu.setIcon(self.icon)
        submenu.menuAction().setIconVisibleInMenu(True)
        for name, color in PALETTE:
            action = submenu.addAction(self.tr(name))
            action.triggered.connect(lambda _checked=False, c=color:
                                     QTimer.singleShot(0, lambda: self.apply_color(c)))
        action = submenu.addAction(self.tr("Restaurar estilo"))
        action.triggered.connect(lambda _checked=False:
                                 QTimer.singleShot(0, lambda: self.apply(reset=True)))

    def apply_color(self, color):
        self.choose(color)
        self.apply(include_width=False)

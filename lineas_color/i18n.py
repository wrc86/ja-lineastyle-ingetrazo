# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julio Angulo
"""Plugin translations; the document and the host language stay independent."""
from PySide6.QtCore import QCoreApplication, QSettings

LANGUAGES = (("es", "Español"), ("en", "English"), ("fr", "Français"))
SETTINGS_KEY = "lineas_color/language"
HELP = ("Dos clics crean un segmento. Puede escribir su longitud. "
        "Esc termina el tramo. Todas las líneas quedan en el mismo grupo "
        "mientras siga activa esta herramienta.\n\n"
        "Los segmentos comparten vértices. Cerrar un contorno coplanar crea una cara. "
        "Abra el grupo con doble clic para continuar sobre sus planos.\n\n"
        "Tome referencias en extremos, puntos medios, cruces y aristas visibles. "
        "Después del primer clic, pase sobre una arista y pulse ↓ para "
        "fijar una paralela; pulse ↓ otra vez para una perpendicular.\n\n"
        "Para cambiar color, grosor y estilo: seleccione líneas o su grupo "
        "y pulse Aplicar.")

# Spanish source strings keep older error messages readable and translatable.
TRANSLATIONS = {
    "Idioma:": ("Language:", "Langue :"),
    "Idioma del panel y de los mensajes de LineaStyle.":
        ("Language of the LineaStyle panel and messages.", "Langue du panneau et des messages de LineaStyle."),
    "Elija un color y dibuje una línea en el modelo 3D.":
        ("Choose a colour and draw a line in the 3D model.", "Choisissez une couleur et tracez une ligne dans le modèle 3D."),
    "Rojo": ("Red", "Rouge"), "Naranja": ("Orange", "Orange"),
    "Amarillo": ("Yellow", "Jaune"), "Verde": ("Green", "Vert"),
    "Azul": ("Blue", "Bleu"), "Violeta": ("Violet", "Violet"),
    "Negro": ("Black", "Noir"), "Blanco": ("White", "Blanc"),
    "Otro color…": ("Other colour…", "Autre couleur…"),
    "Color actual: {color}": ("Current colour: {color}", "Couleur actuelle : {color}"),
    "Grosor visual:": ("Visual weight:", "Épaisseur à l’écran :"),
    "Grosor en pantalla. Se guarda con la línea; no añade espesor físico.":
        ("On-screen weight. Saved with the line; adds no physical thickness.",
         "Épaisseur à l’écran. Enregistrée avec la ligne ; sans épaisseur physique."),
    "Estilo de línea:": ("Line style:", "Style de ligne :"),
    "Continua": ("Solid", "Continue"), "Punteada": ("Dotted", "Pointillée"),
    "Interrumpida": ("Dashed", "Tirets"), "Raya larga": ("Long dash", "Tirets longs"),
    "Punto y raya": ("Dash-dot", "Trait mixte"),
    "Dos puntos y raya": ("Dash-dot-dot", "Trait mixte à deux points"),
    "Dibujar línea de color": ("Draw coloured line", "Tracer une ligne de couleur"),
    "Aplicar a la selección": ("Apply to selection", "Appliquer à la sélection"),
    "Restaurar estilo": ("Restore style", "Rétablir le style"),
    "Dibujar y recolorear líneas del modelo 3D.":
        ("Draw and recolour lines in the 3D model.", "Tracer et recolorer les lignes du modèle 3D."),
    "Color de la línea": ("Line colour", "Couleur de la ligne"),
    "Línea de color: indique el punto inicial y el final.":
        ("Coloured line: pick the start and end points.", "Ligne de couleur : indiquez le point de départ et le point d’arrivée."),
    "La selección ya tiene ese estilo.":
        ("The selection already has this style.", "La sélection possède déjà ce style."),
    "Estilo restaurado.": ("Style restored.", "Style rétabli."),
    "Propiedades aplicadas a las líneas.":
        ("Properties applied to the lines.", "Propriétés appliquées aux lignes."),
    "JA LineaStyle · Línea": ("JA LineaStyle · Line", "JA LineaStyle · Ligne"),
    "Dibujar líneas conectadas y planos con color, grosor y estilo.":
        ("Draw connected lines and faces with colour, weight and style.",
         "Tracer des lignes reliées et des faces avec couleur, épaisseur et style."),
    "Longitud": ("Length", "Longueur"),
    "JA LineaStyle requiere la API de extensiones 2.":
        ("JA LineaStyle requires extension API 2.", "JA LineaStyle nécessite l’API d’extensions 2."),
    "Esta versión de IngeTrazo no admite el renderizador de JA LineaStyle.":
        ("This version of IngeTrazo does not support the JA LineaStyle renderer.",
         "Cette version d’IngeTrazo ne prend pas en charge le rendu de JA LineaStyle."),
    "JA LineaStyle: el renderizador no es compatible; las líneas se conservan.":
        ("JA LineaStyle: the renderer is incompatible; the lines are preserved.",
         "JA LineaStyle : le rendu est incompatible ; les lignes sont conservées."),
    "El color debe tener el formato #RRGGBB.":
        ("The colour must use the #RRGGBB format.", "La couleur doit respecter le format #RRGGBB."),
    "El grosor debe estar entre 1 y 12 píxeles.":
        ("The weight must be between 1 and 12 pixels.", "L’épaisseur doit être comprise entre 1 et 12 pixels."),
    "El estilo de línea no es válido.":
        ("The line style is invalid.", "Le style de ligne n’est pas valide."),
    "La línea debe tener una longitud mayor que cero.":
        ("The line length must be greater than zero.", "La longueur de la ligne doit être supérieure à zéro."),
    "El grupo abierto tiene una transformación singular.":
        ("The open group has a singular transformation.", "Le groupe ouvert possède une transformation singulière."),
    "El grupo tiene una transformación singular.":
        ("The group has a singular transformation.", "Le groupe possède une transformation singulière."),
    "Seleccione líneas libres o grupos que contengan solo líneas.":
        ("Select loose lines or groups containing only lines.", "Sélectionnez des lignes isolées ou des groupes ne contenant que des lignes."),
    "Esta versión no colorea por separado las aristas de una cara.":
        ("This version cannot colour individual edges of an ungrouped face.",
         "Cette version ne colore pas séparément les arêtes d’une face non groupée."),
    "Seleccione primero las líneas que desea colorear.":
        ("First select the lines you want to colour.", "Sélectionnez d’abord les lignes à colorer."),
    HELP: (
        "Two clicks create a segment. You can type its length. Esc ends the chain. "
        "All lines stay in the same group while this tool remains active.\n\n"
        "Segments share vertices. Closing a coplanar outline creates a face. "
        "Double-click the group to continue drawing on its faces.\n\n"
        "Snap to endpoints, midpoints, intersections and visible edges. "
        "After the first click, hover over an edge and press ↓ to lock a parallel direction; "
        "press ↓ again for a perpendicular direction.\n\n"
        "To change colour, weight and style, select lines or their group and click Apply.",
        "Deux clics créent un segment. Vous pouvez saisir sa longueur. Échap termine la chaîne. "
        "Toutes les lignes restent dans le même groupe tant que cet outil est actif.\n\n"
        "Les segments partagent leurs sommets. Fermer un contour coplanaire crée une face. "
        "Double-cliquez sur le groupe pour continuer à tracer sur ses faces.\n\n"
        "Utilisez les accrochages aux extrémités, milieux, intersections et arêtes visibles. "
        "Après le premier clic, survolez une arête et appuyez sur ↓ pour verrouiller une parallèle ; "
        "appuyez à nouveau sur ↓ pour une perpendiculaire.\n\n"
        "Pour changer la couleur, l’épaisseur et le style, sélectionnez les lignes ou leur groupe "
        "et cliquez sur Appliquer."),
}

COLOR_DIALOG_TEXT = {
    "&Basic colors": ("Colores &básicos", "&Basic colours", "Couleurs de &base"),
    "&Custom colors": ("Colores &personalizados", "&Custom colours", "Couleurs &personnalisées"),
    "Hu&e:": ("&Tono:", "Hu&e:", "&Teinte :"),
    "&Sat:": ("&Saturación:", "&Sat:", "&Saturation :"),
    "&Val:": ("&Valor:", "&Val:", "&Valeur :"),
    "&Red:": ("&Rojo:", "&Red:", "&Rouge :"),
    "&Green:": ("&Verde:", "&Green:", "V&ert :"),
    "Bl&ue:": ("&Azul:", "Bl&ue:", "B&leu :"),
    "A&lpha channel:": ("Canal al&fa:", "A&lpha channel:", "Canal al&pha :"),
    "&HTML:": ("&HTML:", "&HTML:", "&HTML :"),
    "&Pick Screen Color": ("Elegir color de &pantalla", "&Pick Screen Colour", "Prélever une couleur à l’&écran"),
    "&Add to Custom Colors": ("&Añadir a colores personalizados", "&Add to Custom Colours", "&Ajouter aux couleurs personnalisées"),
    "OK": ("Aceptar", "OK", "OK"),
    "Cancel": ("Cancelar", "Cancel", "Annuler"),
}


def normalized_language(value):
    code = str(value or "").lower().replace("_", "-").split("-")[0]
    return code if code in {code for code, _name in LANGUAGES} else None


class Translator:
    def __init__(self):
        from core.i18n import current_language
        self.language = (normalized_language(QSettings().value(SETTINGS_KEY))
                         or normalized_language(current_language()) or "es")

    def select(self, language):
        code = normalized_language(language)
        if code is None:
            raise ValueError("Unsupported LineaStyle language")
        self.language = code
        QSettings().setValue(SETTINGS_KEY, code)

    def tr(self, source, **values):
        text = source
        if self.language != "es" and source in TRANSLATIONS:
            text = TRANSLATIONS[source][0 if self.language == "en" else 1]
        return text.format(**values) if values else text

    def error(self, message):
        # History prefixes model errors with the command class name.
        for source in TRANSLATIONS:
            if message == source or message.endswith(": " + source):
                return message[:-len(source)] + self.tr(source)
        return message

    def localize_color_dialog(self, dialog):
        from PySide6.QtWidgets import QAbstractButton, QLabel
        aliases = {}
        index = {"es": 0, "en": 1, "fr": 2}[self.language]
        for source, texts in COLOR_DIALOG_TEXT.items():
            aliases[source] = texts[index]
            for context in ("QColorDialog", "QPlatformTheme", "QDialogButtonBox"):
                aliases[QCoreApplication.translate(context, source)] = texts[index]
        for widget in (*dialog.findChildren(QLabel), *dialog.findChildren(QAbstractButton)):
            text = aliases.get(widget.text())
            if text is not None:
                widget.setText(text)

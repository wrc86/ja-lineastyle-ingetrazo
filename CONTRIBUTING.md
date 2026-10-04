# Contribuir a JA LineaStyle

**Alcance de esta separación:** este repositorio contiene el plugin, su documentación y el ZIP instalable. Los comandos de pruebas y empaquetado descritos abajo pertenecen al entorno o paquete de fuentes original; sus carpetas `tests/`, `scripts/` y `.reference/` no se incluyen aquí. No se presentan como comandos ejecutables desde esta copia.


JA LineaStyle 0.1.2 es un plugin de código abierto bajo **GPL-3.0-or-later**.
Las contribuciones se distribuyen bajo esa misma licencia. Véase `LICENSE`.

## Preparar el entorno

Descomprima `JA_LineaStyle_v0.1.2_source.zip` y trabaje desde su raíz. Requiere
Python 3.10 o posterior, Git y las dependencias de IngeTrazo. El programa
anfitrión se descarga por separado; no forma parte del paquete del plugin.

```sh
git clone https://github.com/ingelibre/ingetrazo.git .reference/ingetrazo
git -C .reference/ingetrazo checkout 6be29fe437a7cd992d4e079f71720821b25216b9
python3 -m venv dev-env
dev-env/bin/python -m pip install -r .reference/ingetrazo/requirements.txt
dev-env/bin/python -m pytest tests/test_ja_lineastyle.py -q
dev-env/bin/python scripts/render_ja_lineastyle_icon.py
dev-env/bin/python scripts/preview_ja_lineastyle.py
dev-env/bin/python scripts/build_ja_lineastyle_release.py
```

En Windows sustituya `dev-env/bin/python` por `dev-env/Scripts/python.exe`.
Las pruebas usan una configuración Qt y una carpeta de autoguardado aisladas.
Para verificar píxeles en macOS, use:

```sh
QT_QPA_PLATFORM=cocoa dev-env/bin/python -m pytest tests/test_ja_lineastyle.py -q
QT_QPA_PLATFORM=cocoa dev-env/bin/python scripts/preview_ja_lineastyle.py
```

Las pruebas de OpenGL se omiten cuando el entorno no ofrece un contexto
gráfico. En Linux use un escritorio gráfico y `QT_QPA_PLATFORM=xcb` cuando
esté disponible. Una captura de desarrollo no sustituye una prueba manual
de instalación y reinicio en el binario de IngeTrazo.

## Proponer cambios

- Incluya la versión de IngeTrazo y pasos para reproducir el problema.
- Mantenga las operaciones reversibles y las identidades de la geometría.
- Conserve el identificador `lineas_color` para leer modelos anteriores,
  actualizar la instalación y conservar la identidad del panel.
- Mantenga los estilos visuales separados de la topología: los huecos de un
  patrón no deben romper aristas, inferencias ni caras.
- Añada pruebas relevantes para cambios en geometría, transformaciones,
  historial, persistencia o renderizado. Verifique las capturas cuando cambie la UI.
- Actualice la versión en `lineas_color/__init__.py` y el historial al preparar
  una nueva versión. El empaquetador lee la versión directamente de ese archivo.

## Distribuir

El script genera un ZIP instalable y un ZIP de fuentes en `dist/`. Distribuya
ambos, para que cada versión incluya su código fuente, junto con `LICENSE`,
`NOTICES.md`, las instrucciones y las pruebas correspondientes.
El empaquetador utiliza una lista explícita de archivos y excluye el entorno
Python, el código del anfitrión, copias de seguridad, cachés y datos locales.

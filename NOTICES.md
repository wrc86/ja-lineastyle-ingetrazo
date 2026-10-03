# Autoría y dependencias

**JA LineaStyle — Copyright (C) 2026 Julio Angulo.**

El código, el icono SVG y sus variantes PNG, la documentación, las pruebas, las herramientas de distribución y
el modelo de ejemplo de JA LineaStyle se ofrecen bajo **GPL-3.0-or-later**.
Los archivos Python incluyen su identificador SPDX. El texto íntegro de la
licencia se distribuye en `LICENSE` y en `lineas_color/LICENSE`.

JA LineaStyle es un plugin para [IngeTrazo](https://github.com/ingelibre/ingetrazo),
desarrollado por Marco Sumari Tellez y sus colaboradores bajo GPL-3.0-or-later.
Utiliza sus API, herramientas y planificador de geometría, y requiere que el
anfitrión esté instalado. Los paquetes de JA LineaStyle contienen únicamente
los archivos propios del plugin; IngeTrazo se obtiene por separado.

Las dependencias de ejecución —Python, PySide6/Qt y las utilizadas por el
anfitrión— conservan las licencias y los avisos de sus respectivos proyectos.
Sus binarios no se incluyen en estos ZIP. Pytest se utiliza para desarrollo.

El nombre visible es **JA LineaStyle**. El identificador interno `lineas_color`,
la clave de datos `.igz` y la identidad del panel se conservan para actualizar
instalaciones anteriores sin crear una segunda extensión y para mantener
los modelos y las preferencias existentes.

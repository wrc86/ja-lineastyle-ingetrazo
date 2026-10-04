# JA LineaStyle · IngeTrazo

Versión 0.1.2. Extensión para dibujar líneas 3D con color, grosor y estilo,
en una malla compartida por sesión de dibujo. Cerrar contornos coplanares forma caras.
Probada con IngeTrazo 0.5.7 y la API de extensiones 2. Incluye un icono SVG propio
en la opción **Extensiones → JA LineaStyle…** y en el menú contextual.
La pestaña de los paneles muestra **LineaStyle** con su icono.

## Instalación

1. Descomprima `JA_LineaStyle_v0.1.2.zip`.
2. En IngeTrazo, abra **Extensiones → Abrir carpeta de plugins**.
3. Si tiene una versión anterior de Líneas de colores, sustituya su carpeta existente.
   Copie la carpeta **`lineas_color` completa** a esa ubicación.
4. Reinicie IngeTrazo. Abra **Extensiones → JA LineaStyle…**.

Abra `Ejemplo_JA_LineaStyle.igz`, incluido en el ZIP, para ver los seis estilos y
dos caras conectadas, todo dentro de un único grupo sin subgrupos por segmento.

No instale el ZIP como un `.rbz`: esta es una extensión Python de IngeTrazo.

## Muestrario de estilos de línea

![Patrones, colores y grosores de línea](../docs/images/lineastyle-muestrario.png)

La imagen de referencia aportada por Julio Angulo reúne patrones continuos, punteados e interrumpidos y combinaciones de puntos y rayas en la fila superior, variaciones de color y gris en el centro y una progresión de grosores rojos abajo. El recuadro negro muestra el contraste sobre fondo oscuro.

Úsala para comparar el aspecto de los trazos; no representa una escala numérica de grosores. La extensión ofrece seis estilos y un grosor visual de 1 a 12 px.

## Uso

- Elija un color de la paleta o **Otro color…**, un **Grosor visual**, de 1 a 12 px,
  y un **Estilo de línea**: continua, punteada, interrumpida, raya larga,
  punto y raya, o dos puntos y raya.
- Pulse **Dibujar línea de color** y marque el inicio y el final. Puede encadenar
  segmentos, usar las inferencias y bloqueos del dibujo nativo, o escribir una longitud.
  **Esc** termina el tramo y permite empezar otro en el mismo grupo.
- El cursor es un lápiz del color seleccionado; su punta marca el punto de dibujo.
  Cambiar el color actualiza el lápiz de inmediato, también con **Otro color…**.
- Puede tomar referencias en **extremos, puntos medios, cruces y puntos sobre aristas**,
  tanto de líneas nativas como de líneas con cualquiera de los seis estilos, incluyendo
  los huecos visuales del patrón. También funcionan los grupos y componentes girados
  o anidados, y las líneas recién dibujadas en la misma sesión.
  Después del primer clic, pase el cursor sobre una arista y pulse **↓** para fijar una
  dirección paralela; pulse **↓** otra vez para una perpendicular y otra vez para liberarla.
  Las flechas de los ejes y **Shift** conservan los bloqueos del dibujo nativo.
- Todas las líneas quedan dentro de un único grupo mientras siga activa la herramienta,
  incluso al cambiar las propiedades, cerrar un recorrido o volver a pulsar Dibujar.
  Cada arista conserva sus propiedades dentro de la **misma malla**, sin subgrupos.
  Los extremos coincidentes se unen; los cruces dividen las aristas y un contorno
  cerrado y coplanar crea una cara. Una diagonal puede dividir un plano en dos caras.
- Abra el grupo con doble clic para continuar dibujando en su malla y modificar sus
  planos. La herramienta utiliza directamente ese grupo y no crea un grupo hijo.
  Dentro del grupo, también puede seleccionar aristas individuales y aplicarles propiedades.
- **Espacio** vuelve a Seleccionar. Al cambiar de herramienta y volver a Dibujar comienza
  un grupo nuevo. Cambiar de documento o de contexto de edición también inicia otro grupo.
- Para cambiar las propiedades, seleccione el grupo o líneas libres existentes
  y pulse **Aplicar a la selección**. El menú de colores con clic derecho cambia solo el
  color y conserva el grosor y el patrón de cada arista.
- Las líneas libres seleccionadas se reúnen en **un solo grupo**, conservando sus
  extremos y etiquetas.
- **Restaurar estilo**, aplicado al grupo, elimina sus propiedades visuales del plugin
  y conserva la malla y sus caras. Aplicado a aristas dentro del grupo, recupera las
  propiedades predeterminadas del grupo.
- Los grupos por sesión de la versión 1.1.0 se unifican al abrirlos con doble clic y
  continuar dibujando con esta herramienta. Sus colores y grosores se conservan;
  deshacer ese primer segmento devuelve los subgrupos anteriores.
- Guardar como `.igz` conserva la geometría, los grupos y las propiedades. Crear, aplicar y restaurar
  admiten deshacer y rehacer. Mover, rotar, escalar, copiar, seleccionar y borrar utilizan
  las herramientas nativas del modelo.

## Alcance y compatibilidad

El grosor se mide en píxeles de pantalla y se mantiene al hacer zoom. Se ve tanto durante
la previsualización como en las líneas terminadas, y se escala en las imágenes raster.
El patrón usa distancias visuales proporcionales al grosor; el zoom no cambia su tamaño
en pantalla. **Los huecos son únicamente visuales**: cada arista sigue completa y puede
participar en caras, inferencias y selección. Los segmentos son geometría 3D nativa,
sin grosor físico. Las caras ocultan las líneas
de atrás; se respetan las etiquetas ocultas y los cortes de sección. El color se muestra
en la vista 3D y en las imágenes generadas mediante el renderizador raster del modelo.
La selección mantiene el resaltado naranja, el grosor y el patrón; deseleccione para ver el color.

Se pueden aplicar propiedades a grupos con caras sin cambiar sus materiales. Las
aristas de caras del modelo suelto requieren agrupar la geometría primero. Los contornos
no coplanares no forman superficies automáticamente. Explotar un grupo elimina sus
propiedades específicas del plugin. Restaurar el estilo no desagrupa la geometría.

Las propiedades son datos de la extensión guardados en `group.ext`, no materiales de caras.
Las propiedades por arista se guardan junto con sus extremos; no requieren entidades
separadas. Se necesita el plugin instalado para mostrarlas. Los estilos personalizados
no se transfieren a `.skp`, DXF, Blender ni a láminas con renderizador vectorial.
Una lámina renderizada como imagen utiliza las propiedades del plugin.

La API pública 2 no expone un pase 3D para colores de aristas. El plugin adapta el pase
de previsualización y filtra las matrices de dibujo de aristas del viewport 0.5.7,
para que los huecos no contengan una línea continua debajo. Mantiene intacta la
geometría utilizada para caras, inferencias y selección. Al construir el índice de
referencias, proporciona las aristas completas al detector nativo, incluso si su patrón
tiene huecos. Respeta la geometría oculta y la ocultación del entorno al editar un grupo,
sin editar archivos del programa. Una versión
futura de IngeTrazo puede necesitar actualizar este adaptador. Si el pase falla, se
desactiva y las líneas siguen disponibles con el color normal del estilo.

## Verificación

Las 72 pruebas del plugin utilizan el cargador, las herramientas, el planificador de caras y el
códec `.igz` reales de IngeTrazo 0.5.7. Verifican sesiones, caras conectadas, cruces,
propiedades por arista, edición dentro del grupo, migración de sesiones antiguas,
deshacer/rehacer, copia, movimiento y guardado/reapertura. También verifican el color
del lápiz, su punta, pantallas de distinta densidad y el cambio a otras herramientas.
Las pruebas de referencias recorren la detección real desde posiciones de pantalla:
extremos, puntos medios, aristas, cruces, grupos girados y anidados, bloqueo paralelo
y perpendicular, caras cerradas con referencias y exclusión de geometría oculta.
Las pruebas con OpenGL
real verifican colores, grosores, huecos de los seis estilos, selección, restauración
del renderizador nativo, ocultación detrás de caras y recorte de sección.

## Código abierto

JA LineaStyle se distribuye bajo **GPL-3.0-or-later**. El código fuente, la documentación,
las pruebas y el modelo de ejemplo se pueden estudiar, modificar y redistribuir bajo
esa licencia. El texto completo está en [LICENSE](LICENSE).

El paquete `JA_LineaStyle_v0.1.2_source.zip` incluye el código y las herramientas para
reproducir las pruebas y generar ambos ZIP. Consulte [CONTRIBUTING.md](CONTRIBUTING.md),
[CHANGELOG.md](CHANGELOG.md) y [NOTICES.md](NOTICES.md).

El nombre visible es **JA LineaStyle**. La carpeta y el identificador interno
`lineas_color` se mantienen para actualizar instalaciones, conservar las preferencias
y leer los estilos guardados en modelos de las versiones anteriores.

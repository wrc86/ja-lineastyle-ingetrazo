# Historial de JA LineaStyle

## 0.1.4 — 2026-10-04

- Añadidos inglés y francés al español existente, con selector en el panel y preferencia persistente.
- Traducción de colores, seis patrones, controles, ayuda, mensajes de estado y errores del plugin, y selector de color.
- El cambio de idioma conserva la herramienta, los segmentos, la longitud pendiente y las propiedades de dibujo.
- Cinco pruebas nuevas: idioma inicial, preferencia guardada y cambios en una sesión activa con los diálogos traducidos.
- El empaquetador genera también el ZIP de una sola carpeta requerido por el catálogo de IngeTrazo.

## 0.1.3 — 2026-10-04

- Corregido el bloqueo de navegación y dibujo desde el arranque al instalar 0.1.2
  en el paquete macOS de IngeTrazo 0.5.7. Ese binario utiliza `_pick_index()` sin
  el parámetro `near` presente en el código más reciente con la misma versión.
- La extensión comprueba la firma de la función nativa una vez y utiliza la
  llamada compatible; conserva las referencias sobre las líneas con estilo.
- Dos pruebas de regresión para ambas firmas: arranque, órbita, desplazamiento,
  zoom, dibujo encadenado con referencias, deshacer y rehacer.
- Prueba aislada contra `/Applications/IngeTrazo.app`: reproducido el error de
  0.1.2 y comprobados ocho controles de funcionamiento con 0.1.3, incluido OpenGL.

## 0.1.2 — 2026-10-03

- Corregida la pérdida de referencias sobre líneas con estilo: el filtro visual
  también quitaba sus aristas del índice de detección del modelo.
- El índice nativo vuelve a recibir las aristas completas, conservando extremos,
  puntos medios, puntos sobre aristas, cruces y referencias paralelas y perpendiculares,
  incluso en los huecos de una línea punteada o interrumpida.
- Referencias y selección en grupos y componentes girados o anidados, y referencias
  sobre líneas creadas en la sesión actual. Se conserva la exclusión de geometría oculta.
- Instrucciones de referencias en el panel y 13 pruebas de regresión con posiciones
  reales de pantalla, incluido el cierre de caras con líneas tomadas como referencia.

## 0.1.1 — 2026-10-03

- Pestaña de panel llamada **LineaStyle**, con el icono del plugin.
- Cursor de lápiz con el color seleccionado para dibujar; se actualiza al
  cambiar el color de la paleta o elegir un color personalizado.
- Punta del lápiz como punto preciso del clic y dibujo nítido en pantallas HiDPI.
- Contorno claro y oscuro para mantener visibles los lápices blancos y negros.
- Recuperación del cursor al volver al modelo, terminar un tramo o finalizar
  una navegación temporal; uso del cursor nativo al cambiar de herramienta.

## 0.1.0 — 2026-10-03

Primera versión de código abierto bajo el nombre **JA LineaStyle**.

- Color por arista, paleta y selección de un color personalizado.
- Grosor visual de 1 a 12 píxeles.
- Seis estilos: continua, punteada, interrumpida, raya larga, punto y raya,
  y dos puntos y raya.
- Una malla compartida por sesión, sin subgrupos por segmento; vértices unidos,
  división de cruces y formación de caras al cerrar contornos coplanares.
- Edición dentro del grupo, propiedades por arista, deshacer y rehacer.
- Persistencia `.igz` y lectura de los modelos del plugin Líneas de colores.
- Unión reversible de los contenedores por segmento de las versiones anteriores.
- Panel, menú y herramienta con la marca JA LineaStyle.
- Icono SVG propio en el menú de Extensiones, el menú contextual y el panel.
- Licencia GPL-3.0-or-later, avisos de autoría, instrucciones para contribuir y
  distribución de código fuente con pruebas y scripts reproducibles.

Las versiones 1.0.0, 1.1.0 y 1.2.0 de **Líneas de colores** fueron versiones de
desarrollo previas al cambio de nombre. La numeración de JA LineaStyle empieza
en 0.1.0; conserva las funciones y los datos de la versión de desarrollo 1.2.0.

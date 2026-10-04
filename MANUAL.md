# JA LineaStyle · Manual de usuario / User manual / Manuel d’utilisation

**Versión / Version 0.1.4 · IngeTrazo 0.5.7 (API de extensiones 2) · Julio Angulo · GPL-3.0-or-later**

[Español](#español) · [English](#english) · [Français](#français)

---

## Español

### 1. ¿Qué es JA LineaStyle?

JA LineaStyle es una herramienta para **dibujar líneas 3D con color, grosor y estilo
de trazo** dentro de IngeTrazo, y para cambiar esas propiedades en líneas existentes.
Sirve para:

- resaltar ejes, cotas de referencia, recorridos o límites de propiedad;
- diferenciar instalaciones (agua, eléctrica, gas) por color;
- dibujar líneas ocultas, de proyección o de eje con su trazo convencional;
- bocetar en 3D con lápices de colores.

Las líneas son geometría 3D real: se unen en los vértices, se dividen en los cruces
y **un contorno cerrado y plano forma una cara**, como con la herramienta Línea nativa.

![Muestrario de JA LineaStyle: estilos de trazo, colores y grosores](docs/estilos.png)

*Arriba: los seis estilos de trazo en distintos grosores y colores, también sobre fondo
oscuro. Centro: paleta y colores personalizados. Abajo: progresión de grosores en pantalla.*

### 2. Instalación

1. Descarga `ja_lineastyle-0.1.4-plugin.zip` desde el catálogo de IngeTrazo o desde
   [las versiones del repositorio](https://github.com/wrc86/ja-lineastyle-ingetrazo/releases).
2. Descomprímelo. Obtendrás una carpeta llamada **`lineas_color`**
   (es el nombre interno; se conserva para actualizar versiones anteriores).
3. En IngeTrazo abre **Extensiones → Abrir carpeta de plugins**.
4. Copia allí la carpeta `lineas_color` completa. Si tenías «Líneas de colores»,
   reemplaza la carpeta existente.
5. Reinicia IngeTrazo.

**Desinstalar:** cierra IngeTrazo y borra la carpeta `lineas_color`.

### 3. Abrir el panel

- Menú **Extensiones → JA LineaStyle…**, o
- clic derecho en la vista 3D → **JA LineaStyle**.

El panel aparece como pestaña **LineaStyle** con su icono:

![Pestaña LineaStyle](docs/pestana.png)

![Panel de JA LineaStyle](docs/panel.png)

### 4. Controles del panel

| Control | Qué hace |
|---|---|
| **Idioma** | Español, English o Français. Cambia al instante y recuerda la elección al reiniciar. |
| **Paleta de colores** | Rojo, Naranja, Amarillo, Verde, Azul, Violeta, Negro y Blanco. |
| **Otro color…** | Abre el selector para cualquier color. |
| **Color actual** | Muestra el código del color activo (por ejemplo `#E53935`, el rojo de la paleta). |
| **Grosor visual** | De **1 a 12 px**. Es grosor en pantalla: se mantiene igual al hacer zoom y no añade espesor físico. |
| **Estilo de línea** | **Continua**, **Punteada**, **Interrumpida**, **Raya larga**, **Punto y raya**, **Dos puntos y raya**. |
| **Dibujar línea de color** | Activa la herramienta de dibujo. |
| **Aplicar a la selección** | Aplica color, grosor y estilo actuales a las líneas o grupos seleccionados. |
| **Restaurar estilo** | Quita el estilo del plugin y vuelve al aspecto normal. |

Debajo de los botones, el panel recuerda las reglas básicas: dos clics crean un
segmento, Esc termina el tramo, todo queda en el mismo grupo y, para cambiar estilos,
se selecciona y se pulsa **Aplicar**.

#### Cuándo usar cada estilo (convención sugerida)

| Estilo | Uso habitual en dibujo arquitectónico |
|---|---|
| **Continua** | Contornos visibles, bordes, recorridos. |
| **Punteada** | Elementos ocultos o proyectados de poca importancia, límites de vegetación. |
| **Interrumpida** | Aristas ocultas, elementos por encima del plano de corte (aleros, voladizos). |
| **Raya larga** | Proyecciones, límites de zonas o áreas de influencia. |
| **Punto y raya** | Ejes, ejes de simetría, líneas de centro. |
| **Dos puntos y raya** | Límites de propiedad, linderos, retiros. |

### 5. Dibujar

1. Elige color, grosor y estilo.
2. Pulsa **Dibujar línea de color**. El cursor se convierte en un **lápiz del color
   elegido**; la punta del lápiz es el punto exacto del clic.
3. Haz clic en el punto inicial y luego en el final. Puedes seguir encadenando segmentos.
4. Puedes **escribir una longitud** mientras dibujas y usar las inferencias y los
   bloqueos de eje del dibujo nativo.
5. **Esc** termina el tramo actual (puedes empezar otro en el mismo grupo).
6. **Espacio** vuelve a la herramienta Seleccionar.

**Cómo se agrupa:** todo lo que dibujas mientras la herramienta sigue activa queda en
**un solo grupo**, aunque cambies de color o estilo. Cada arista guarda su propio
color, grosor y estilo. Si cambias a otra herramienta y vuelves, se crea un grupo nuevo.

**Caras:** cerrar un contorno en un mismo plano crea una cara; una diagonal puede dividir
un plano en dos caras. Los contornos que no son planos no forman superficies.

**Seguir dibujando en un grupo:** haz **doble clic** en el grupo para abrirlo y vuelve
a **Dibujar**: las líneas nuevas se agregan a esa misma malla, sin crear subgrupos.

**Referencias al dibujar:** acerca la punta del cursor a extremos, puntos medios,
cruces o cualquier punto de una arista visible. Funcionan las líneas nativas y los
seis estilos de JA LineaStyle, también en los huecos del patrón, en grupos girados
o anidados y sobre las líneas recién dibujadas. Después del primer clic, pasa por una
arista y pulsa **↓** para fijar una dirección paralela, otra vez para una perpendicular
y otra vez para liberarla. **Shift** mantiene una inferencia activa; las otras flechas
bloquean los ejes nativos. La geometría oculta no ofrece referencias.

### 6. Cambiar el estilo de líneas existentes

1. Selecciona un grupo dibujado con JA LineaStyle, o abre el grupo y selecciona aristas sueltas.
2. Elige el nuevo color, grosor o estilo.
3. Pulsa **Aplicar a la selección**.

- **Clic derecho → colores:** cambia solo el color y conserva el grosor y el patrón de cada arista.
- **Líneas sueltas del modelo:** al aplicarles estilo se reúnen en **un solo grupo**.
- **Aristas de caras sueltas:** agrupa primero la geometría (herramientas nativas).
- **Restaurar estilo** sobre el grupo quita todas sus propiedades visuales (la malla y las
  caras se conservan); sobre aristas dentro del grupo, les devuelve el estilo por defecto del grupo.

> Mientras una línea está seleccionada se ve con el resaltado naranja de IngeTrazo.
> Deselecciona para ver su color.

### 7. Guardar, deshacer y exportar

- Crear, aplicar y restaurar se pueden **deshacer y rehacer**.
- Mover, rotar, escalar, copiar y borrar usan las herramientas nativas.
- Guarda como **.igz** para conservar las líneas y sus estilos.
- Los colores se ven en la vista 3D y en **imágenes raster** generadas por el modelo
  (también en láminas renderizadas como imagen).
- Los estilos **no** se exportan a `.skp`, DXF, Blender ni a láminas vectoriales:
  allí las líneas salen con el estilo normal.
- **Explotar** un grupo elimina sus estilos del plugin.
- Para ver los estilos en otro computador se necesita la extensión instalada.

Abre `Ejemplo_JA_LineaStyle.igz` (incluido en el repositorio) para ver los seis
estilos y dos caras conectadas dentro de un único grupo.

### 8. Detalles técnicos útiles

- Los huecos de las líneas punteadas son **solo visuales**: cada arista sigue completa
  para caras, inferencias y selección.
- Las caras ocultan las líneas que quedan detrás; se respetan etiquetas ocultas y planos de sección.
- Si una versión futura de IngeTrazo no admite el renderizador del plugin, el panel lo avisa
  y las líneas siguen visibles con el color normal.
- La interfaz ofrece español, inglés y francés; el selector del panel es independiente del idioma de IngeTrazo.

### 9. Problemas frecuentes

| Problema | Solución |
|---|---|
| No veo el color de una línea | Puede estar seleccionada (naranja). Haz clic en vacío para deseleccionar. |
| «La selección ya tiene ese estilo» | No hay cambios que aplicar; elige otro color, grosor o estilo. |
| No puedo aplicar estilo a aristas de una caja | Agrupa primero la geometría y vuelve a aplicar. |
| El estilo se perdió | ¿Exploté el grupo o exporté a DXF/SKP? Esos formatos no guardan el estilo. Usa **Deshacer** o abre el .igz. |
| No aparece en el menú | Verifica que la carpeta se llame `lineas_color` y contenga `__init__.py`; reinicia IngeTrazo. |

### Autor

**Julio Eduardo Angulo** — arquitecto colombiano, fundador y director de diseño de
**[Línea Prima](https://lineaprima.co)**, estudio de arquitectura, diseño y construcción
en Bogotá. Desde 2009 proyecta y construye, con 77 proyectos en Colombia, Puerto Rico
y Estados Unidos, bajo un modelo *Design & Build*: un mismo equipo del concepto a la obra
terminada. Línea Prima hace «arquitectura para durar»: atmósfera, materia honesta y
precisión. Estas extensiones nacen de su práctica diaria con BIM y herramientas digitales.

- Web: [lineaprima.co](https://lineaprima.co) · Perfil: [lineaprima.co/julio-eduardo-angulo](https://lineaprima.co/julio-eduardo-angulo/)
- Correo: info@lineaprima.co · Instagram: [@buskua.co](https://instagram.com/buskua.co)
- Código y reportes de errores: [github.com/wrc86/ja-lineastyle-ingetrazo](https://github.com/wrc86/ja-lineastyle-ingetrazo/issues)

---

## English

### 1. What is JA LineaStyle?

JA LineaStyle is a tool to **draw 3D lines with colour, weight and line style** in
IngeTrazo, and to restyle existing lines. Use it to highlight axes, paths or property
limits, colour-code services (water, power, gas), draw hidden/projection/centre lines
with their conventional pattern, or sketch in 3D with coloured pencils.

Lines are real 3D geometry: they join at vertices, split at crossings and
**a closed planar outline becomes a face**, just like the native Line tool.

![JA LineaStyle sample sheet: line styles, colours and weights](docs/estilos.png)

*Top: the six line styles at several weights and colours, also on a dark background.
Middle: palette and custom colours. Bottom: on-screen weight progression.*

Choose **English** in the panel’s **Language** selector. Controls, help and messages change immediately; the choice is remembered after restarting. The selector also offers Español and Français.

### 2. Installation

1. Download `ja_lineastyle-0.1.4-plugin.zip` from the IngeTrazo catalog or the
   [repository releases](https://github.com/wrc86/ja-lineastyle-ingetrazo/releases).
2. Unzip it. You get a folder named **`lineas_color`** (internal name, kept for upgrades).
3. In IngeTrazo open **Extensions → Open plugins folder** and copy the folder there.
4. Restart IngeTrazo.

**Uninstall:** close IngeTrazo and delete the `lineas_color` folder.

### 3. Opening the panel

**Extensions → JA LineaStyle…** or right-click in the 3D view → **JA LineaStyle**.
It appears as a **LineaStyle** panel tab:

![LineaStyle tab](docs/pestana.png)

![JA LineaStyle panel](docs/panel.png)

### 4. Panel controls

| Control | What it does |
|---|---|
| **Language** | Español, English or Français. Applies immediately and is remembered after restarting. |
| **Palette** | Red, Orange, Yellow, Green, Blue, Violet, Black, White. |
| **Other colour…** (*Otro color…*) | Opens a colour picker. |
| **Current colour** (*Color actual*) | Shows the active colour code, e.g. `#E53935` (palette red). |
| **Visual weight** (*Grosor visual*) | **1–12 px** on screen; constant when zooming, no physical thickness. |
| **Line style** (*Estilo de línea*) | Solid (*Continua*), Dotted (*Punteada*), Dashed (*Interrumpida*), Long dash (*Raya larga*), Dash-dot (*Punto y raya*), Dash-dot-dot (*Dos puntos y raya*). |
| **Draw coloured line** (*Dibujar línea de color*) | Starts the drawing tool. |
| **Apply to selection** (*Aplicar a la selección*) | Applies current colour, weight and style to the selected lines/groups. |
| **Restore style** (*Restaurar estilo*) | Removes the plugin style. |

#### Suggested use of each style

| Style | Typical architectural use |
|---|---|
| **Solid** | Visible outlines, edges, paths. |
| **Dotted** | Minor hidden/projected elements, planting limits. |
| **Dashed** | Hidden edges, elements above the cut plane (eaves, overhangs). |
| **Long dash** | Projections, zone limits. |
| **Dash-dot** | Axes, centre lines, symmetry lines. |
| **Dash-dot-dot** | Property lines, boundaries, setbacks. |

### 5. Drawing

1. Pick colour, weight and style, then press **Draw coloured line**. The cursor becomes
   a **pencil in the chosen colour**; its tip is the exact click point.
2. Click a start point and an end point; keep clicking to chain segments. You can **type a
   length** and use native inferences and axis locks.
3. **Esc** ends the current run; **Space** returns to Select.

Everything drawn while the tool stays active goes into **one group**, even if you change
colour or style; each edge keeps its own properties. Switching tools and coming back
starts a new group. **Double-click** a group to open it and keep drawing in the same mesh.
Closing a planar outline creates a face; non-planar outlines do not.

**Drawing references:** aim the pencil tip at endpoints, midpoints, intersections
or any point on a visible edge. Native lines and all six JA LineaStyle patterns work,
including visual gaps, rotated or nested groups and lines drawn in the current session.
After the first click, hover an edge and press **↓** to lock parallel to it, again for
perpendicular and again to release. **Shift** holds the current inference; the other
arrows lock native axes. Hidden geometry does not attract references.

### 6. Restyling existing lines

Select a JA LineaStyle group (or open it and select edges), choose new properties and
press **Apply to selection**. Right-click → colours changes only the colour. Loose model
lines are gathered into **one group** when styled; edges of loose faces must be grouped
first. **Restore style** on a group removes all plugin styling (mesh and faces stay).
Selected lines show IngeTrazo's orange highlight — deselect to see their colour.

### 7. Saving, undo and export

- Create, apply and restore support **undo/redo**; move/rotate/scale/copy/delete are native.
- Save as **.igz** to keep styles. Colours show in the 3D view and in **raster** images/sheets.
- Styles are **not** exported to `.skp`, DXF, Blender or vector sheets.
- **Exploding** a group removes its plugin styles. Other computers need the extension installed.

Open `Ejemplo_JA_LineaStyle.igz` (in the repository) to see all six styles.

### 8. Troubleshooting

| Problem | Fix |
|---|---|
| Line colour not visible | It may be selected (orange). Click empty space. |
| "Selection already has that style" | Nothing to change; pick a different property. |
| Can't style edges of a box | Group the geometry first. |
| Style lost | Exploded the group or exported to DXF/SKP? Use **Undo** or reopen the .igz. |
| Not in the menu | Folder must be named `lineas_color` and contain `__init__.py`; restart IngeTrazo. |

### Author

**Julio Eduardo Angulo** — Colombian architect, founder and design director of
**[Línea Prima](https://lineaprima.co)**, an architecture, design and construction studio
in Bogotá. Designing and building since 2009, with 77 projects in Colombia, Puerto Rico
and the United States under a *Design & Build* model: one team from concept to finished
building. Línea Prima makes "architecture to last": atmosphere, honest materials and
precision. These extensions come from his daily practice with BIM and digital tools.

- Web: [lineaprima.co](https://lineaprima.co) · Profile: [lineaprima.co/julio-eduardo-angulo](https://lineaprima.co/julio-eduardo-angulo/)
- Email: info@lineaprima.co · Instagram: [@buskua.co](https://instagram.com/buskua.co)
- Code and bug reports: [github.com/wrc86/ja-lineastyle-ingetrazo](https://github.com/wrc86/ja-lineastyle-ingetrazo/issues)


---

## Français

### 1. Présentation

JA LineaStyle permet de tracer des **lignes 3D avec une couleur, une épaisseur et un style de ligne** dans IngeTrazo, puis de modifier ces propriétés sur des lignes existantes. Les segments partagent leurs sommets, se divisent aux intersections et forment une face lorsqu’un contour fermé est coplanaire.

### 2. Installation et langue

1. Téléchargez `ja_lineastyle-0.1.4-plugin.zip` depuis le [catalogue d’IngeTrazo](https://ingetrazo.com/extensiones) ou les [versions du projet](https://github.com/wrc86/ja-lineastyle-ingetrazo/releases).
2. Décompressez le ZIP et copiez le dossier complet **`lineas_color`** dans le dossier indiqué par **Extensions → Ouvrir le dossier des extensions**. Remplacez le dossier de la version précédente lors d’une mise à jour.
3. Redémarrez IngeTrazo et ouvrez **Extensions → JA LineaStyle…**. L’onglet du panneau s’appelle **LineaStyle** et conserve son icône.
4. Choisissez **Français** dans le sélecteur **Langue** du panneau. Les contrôles, l’aide et les messages changent immédiatement. Le choix est conservé au redémarrage.

Le panneau propose aussi **Español** et **English**. Au premier démarrage, il reprend la langue d’IngeTrazo si elle est prise en charge, sinon l’espagnol. Ce réglage concerne LineaStyle ; les autres outils et menus conservent la langue d’IngeTrazo.

![Panneau de LineaStyle en français](docs/panel_fr.png)

### 3. Contrôles

| Contrôle | Fonction |
|---|---|
| **Langue** | Español, English ou Français ; changement immédiat, choix mémorisé. |
| **Palette** | Rouge, Orange, Jaune, Vert, Bleu, Violet, Noir et Blanc. |
| **Autre couleur…** | Ouvre un sélecteur de couleur traduit dans la langue du panneau. |
| **Couleur actuelle** | Affiche le code de la couleur choisie, par exemple `#E53935`. |
| **Épaisseur à l’écran** | De **1 à 12 px** ; reste constante lors du zoom, sans épaisseur physique. |
| **Style de ligne** | Continue, Pointillée, Tirets, Tirets longs, Trait mixte ou Trait mixte à deux points. |
| **Tracer une ligne de couleur** | Active l’outil de dessin. |
| **Appliquer à la sélection** | Applique la couleur, l’épaisseur et le style actuels aux lignes ou groupes sélectionnés. |
| **Rétablir le style** | Retire les propriétés visuelles de l’extension et conserve la géométrie. |

### 4. Tracer des lignes et des faces

1. Choisissez une couleur, une épaisseur et un style.
2. Cliquez sur **Tracer une ligne de couleur**. Le curseur devient un crayon de la couleur choisie ; sa pointe correspond au point du clic.
3. Cliquez sur le point de départ puis sur le point d’arrivée. Continuez à cliquer pour enchaîner les segments, ou saisissez une longueur.
4. **Échap** termine la chaîne en cours et permet d’en commencer une autre dans le même groupe. **Espace** revient à l’outil de sélection.

Toutes les lignes tracées tant que l’outil reste actif appartiennent à **un seul groupe**, même si vous changez de couleur, de style ou de langue. Chaque arête conserve ses propres propriétés. Revenir au dessin après avoir activé un autre outil crée un nouveau groupe.

Fermer un contour coplanaire crée une face. Une diagonale peut partager cette face en deux. Un contour qui n’est pas plan ne crée pas de surface. Double-cliquez sur un groupe de LineaStyle pour l’ouvrir et poursuivre le dessin dans la même maille, sans sous-groupes.

### 5. Accrochages et directions

Les extrémités, milieux, intersections et points sur les arêtes visibles servent de références. Les six styles prennent en charge ces accrochages, y compris dans les espaces visuels des pointillés, dans les groupes transformés ou imbriqués et sur les segments nouvellement tracés.

Après le premier clic, survolez une arête puis appuyez sur **↓** pour verrouiller une direction parallèle. Appuyez à nouveau pour une perpendiculaire, puis une troisième fois pour libérer la direction. **Maj** maintient une inférence active ; les autres flèches verrouillent les axes natifs. Les éléments masqués n’offrent pas d’accrochage.

### 6. Modifier des lignes existantes

Sélectionnez un groupe ou des arêtes dans un groupe ouvert, choisissez les propriétés puis cliquez sur **Appliquer à la sélection**. Le menu contextuel **JA LineaStyle** change uniquement la couleur et conserve les épaisseurs et les styles de chaque arête.

Les lignes isolées sélectionnées sont réunies dans un groupe. Pour les arêtes d’une face non groupée, groupez d’abord la géométrie avec les outils natifs. Rétablir le style d’un groupe retire ses propriétés visuelles sans effacer ses faces ; sur les arêtes d’un groupe ouvert, cela rétablit le style par défaut du groupe.

Une ligne sélectionnée apparaît avec la surbrillance d’IngeTrazo. Désélectionnez-la pour voir sa couleur.

### 7. Enregistrer, annuler et exporter

La création, l’application et le rétablissement des styles prennent en charge **Annuler / Rétablir**. Déplacer, tourner, copier et supprimer utilisent les outils natifs. Enregistrez au format **`.igz`** pour conserver la géométrie et les propriétés de LineaStyle.

Les couleurs et les styles sont visibles dans la vue 3D et dans les images raster du modèle. Ils ne sont pas conservés lors d’un export vers SKP, DXF, Blender ou un dessin vectoriel. Décomposer un groupe supprime ses propriétés d’extension. Une autre installation d’IngeTrazo doit disposer de LineaStyle pour afficher ces styles.

Les espaces des motifs sont uniquement visuels : les arêtes restent entières pour la création des faces, les accrochages et la sélection. Les faces, les éléments masqués et les plans de coupe sont respectés. Ouvrez `Ejemplo_JA_LineaStyle.igz` dans le dépôt ou dans le paquet complet pour découvrir les six styles et deux faces reliées.

### 8. Résoudre un problème

| Problème | Solution |
|---|---|
| La couleur n’est pas visible | Désélectionnez la ligne pour retirer la surbrillance. |
| La sélection possède déjà ce style | Choisissez une autre couleur, épaisseur ou un autre style. |
| Impossible de modifier les arêtes d’une boîte | Groupez d’abord la géométrie. |
| Le style a disparu | Vérifiez si le groupe a été décomposé ou exporté ; utilisez Annuler ou rechargez le fichier `.igz`. |
| L’extension n’apparaît pas | Vérifiez que le dossier `lineas_color` contient directement `__init__.py`, puis redémarrez IngeTrazo. |

**Auteur : Julio Angulo.** Logiciel libre sous **GPL-3.0-or-later**. Code, versions et signalement des problèmes : [ja-lineastyle-ingetrazo](https://github.com/wrc86/ja-lineastyle-ingetrazo).

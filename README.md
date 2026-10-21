# Hito migrations

Base documental para migraciones de Odoo, preparada para publicación pública.
Los esquemas son **borradores no verificados**, no procedimientos probados ni
pruebas de migraciones exitosas. El menú **Migrando** conserva la documentación general:
[Introducción](docs/index.md), [Procedimiento](docs/procedure.md)
y [Gentle Shell](docs/gentle-shell.md).

**Arquitectura y Plan técnico quedan fuera del menú.** Se conservan sus archivos,
sus URL y sus enlaces de referencia. Las fichas y el calendario de proyectos siguen
como borradores locales y no se incluyen en esta edición pública.

La referencia [Plan técnico](docs/spiral-strategy.md) conserva un único documento completo:
el plan general de migración en espiral, con enlace al Markdown para copiarlo a otro arnés.
La jerarquía del menú no modifica las URL anteriores.

El [manual de uso de Gentle Shell](docs/gentle-shell.md) tiene una sección propia en el menú.
Incluye preparación y acceso desde Windows (PowerShell), Linux y macOS, con un prompt
copiable por sistema para realizar la configuración con ayuda de una IA; después continúa
con comandos comunes en el servidor y mensajes para iniciar, retomar y entregar una migración.
Utiliza ejemplos anónimos. La sección Arquitectura y su diagrama local distinguen
administración en la Mac de Ale, acceso de usuarios y ejecución en PC-ALE; no incluyen
IPs, dominios privados ni credenciales. La edición documental 0.2.3 incorpora esta sección.

Las nueve guías anteriores y Arquitectura conservan sus URL como referencias fuera del menú. `not_in_nav` en `mkdocs.yml` declara esa exclusión;
no elimina páginas ni sus entradas de búsqueda.

## Introducción al diseño de la migración

La [Introducción](docs/index.md) explica el esquema Odoo 17.0 → 19.0: tratamiento de código
oficial, OCA, ADHOC, módulos de Hito y personalizaciones; relación entre repositorio
principal y submódulos; adaptación sobre la estructura existente o preparación de un
repositorio destino con la arquitectura de localización propuesta para Equipavic y Smarttract.
Distingue la actualización de base por Odoo del portado de código, la equivalencia de
reemplazos y la aceptación funcional/histórica. El avance se organiza en espiral.
Las responsabilidades del agente se describen con sus límites: la ayuda a pruebas
funcionales se conserva como capacidad no probada, no como una validación disponible.
No se publican nombres de repositorios internos ni se atribuyen resultados a los proyectos.

## Procedimiento del usuario migrador

El [Procedimiento](docs/procedure.md) se limita a siete pasos: conectarse por SSH,
entrar al caso asignado, abrir `gentle-shell`, iniciar o continuar, aportar repositorio
principal y conexiones SSH de origen/destino si inicia, solicitar en paralelo la
actualización de prueba de la base en [Odoo Upgrade](https://upgrade.odoo.com/), y seguir
al agente guiado por `migration-spiral-strategy-spec.md` del kit del servidor.
Las instrucciones del usuario están integradas en esos pasos: datos y diagnóstico en
el paso 5, solicitud de actualización de base en el 6 y autorizaciones de código,
funcionamiento, datos históricos, ensayo y producción en el 7. Incluye mensajes
copiables, sin contraseñas ni claves privadas, y cómo resolver consultas o bloqueos.
La solicitud de prueba no autoriza producción; el detalle técnico sigue en el plan en espiral.

La antigua URL [Instrucciones del usuario](docs/user-instructions.md) conserva sus
encabezados y enlaces al contenido integrado, sin duplicar los mensajes. Ya no tiene
una entrada separada en el menú. La portada, el manual y Arquitectura apuntan al Procedimiento.

## Plan técnico reutilizable

[Plan técnico](docs/spiral-strategy.md) muestra directamente la estrategia en espiral:
S1 entrada, S2 inventario, S3 código, S4 runtime, S5 aceptación histórica y S6 ensayo de
corte/recuperación. Incluye clasificación de módulos, estados de evidencia y coordinación
por oleadas. No es un catálogo de archivos ni duplica la fuente.

El enlace al Markdown permite copiar el documento completo con Ctrl+A/Ctrl+C o ⌘A/⌘C.
Apunta a la última fuente subida en `docs/spiral-strategy`, no a cambios locales pendientes.
No requiere Gentle Shell. Copiarlo no autoriza operaciones ni acredita resultados de
una migración; se conserva la advertencia de propuesta no verificada.

## Preparación local

Utilice Python 3 y un entorno virtual:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m mkdocs serve
```

Abra la URL local que indica MkDocs. Estos pasos preparan el entorno de trabajo;
para verificar el sitio puede utilizar un entorno desechable fuera del repositorio,
sin instalar dependencias globalmente.

## Compilación y revisión

```sh
python3 -m mkdocs build --strict
SITE_DIR=site python3 -m unittest discover -s tests -v
```

El directorio generado `site/` está excluido de Git. Para una compilación externa,
use `--site-dir /ruta/temporal/site` y el mismo valor en `SITE_DIR`.
Las treinta pruebas comprueban las catorce rutas (tres guías del menú,
Arquitectura, la URL histórica de instrucciones y nueve referencias),
el idioma, las URL canónicas y la navegación limitada a Introducción, Procedimiento y Gentle Shell,
la explicación del código y los datos, las dos estrategias de repositorios y los límites del agente,
el acceso a Plan técnico como único documento en espiral y su enlace Markdown,
el procedimiento de siete pasos con instrucciones integradas, los enlaces de compatibilidad
y los diagramas de referencia técnica y arquitectura,
los ejemplos de instrucciones, los pasos y prompts del manual para Windows/Linux/macOS,
el ejemplo guiado de inicio de once pasos y el de recuperación de seis pasos,
con prompts de asistencia y autorización por paso; también la distinción entre
recuperar un agente vivo y volver a abrir uno cerrado (variante no probada),
los recursos locales y la versión y fecha visibles
(incluida la página 404). Revise también en navegador
la búsqueda, el foco de teclado y la navegación de escritorio y móvil.
Compilar el sitio no verifica una migración; consulte la [lista de validación](docs/validation.md).

### Tema y diseño

MkDocs Material (`>=9.6,<10`) aporta búsqueda superior y navegación izquierda.
La edición 0.2.10 integra el índice de cada guía en esa navegación (`toc.integrate`)
y conserva la ausencia de columna derecha. El conjunto de navegación y contenido
queda centrado con un máximo de 1280 px; el bloque principal tiene un máximo de
936 px, tomando como referencia el límite declarado en el CSS de
[Google Cloud Docs](https://docs.cloud.google.com/docs?hl=es-419), sin reproducir su tema.
En pantallas menores se usa el ancho disponible y se conserva el margen derecho adaptable.
Los gráficos de arquitectura y proceso conservan una composición de 960 px de ancho,
con altura y tipografía reducidas un 30 % respecto de la edición 0.2.7. Las alturas son
1840,3 px y 1498 px, respectivamente; el texto principal es de 14 px y las notas de
12,6 px dentro del SVG, sin transformaciones que deformen las letras. Aprovechan el ancho del
bloque sin ampliarlo: imagen al 100%, altura proporcional y contenedor con bordes y
relleno incluidos en su ancho. Se conservan los enlaces para abrirlos completos.
Los textos copiables conservan la letra pequeña
con `Courier New`, `Courier` o la monoespaciada local.
El contenedor conserva desplazamiento horizontal como protección ante desbordamientos.
La interfaz usa `language: es`, búsqueda `lang: es`
y conserva `mkdocs[i18n]` para las traducciones. `font: false` evita cargar fuentes
externas. `docs/stylesheets/extra.css` aporta un estilo editorial inspirado en la
referencia visual de MIT: fondo blanco, rojo profundo, títulos destacados y bloques
separados por líneas, sin usar su marca ni sugerir afiliación. Se conserva la identidad Hito,
la tipografía del sistema y la navegación de Material; no hay JavaScript personalizado.

`overrides/main.html` y `overrides/404.html` incluyen el bloque compartido
`overrides/partials/doc-edition.html` al inicio del contenido. La versión y fecha
se mantienen en un único lugar, `extra.documentation` de
`mkdocs.yml`: `version` es la versión de la documentación (no de Odoo) y `updated`
es la fecha editorial en formato `AAAA-MM-DD`, mostrada como `DD/MM/AAAA`.
Actualice ambos valores al preparar una edición; compilar no cambia la fecha por sí solo.
Estos datos no acreditan una migración validada. Si cambia la edición, ajuste también
los valores esperados en `tests/test_site.py`.

`docs/assets/migration-process.svg` se conserva como referencia del recorrido técnico
anterior; ya no aparece en el Procedimiento operativo de siete pasos. Es un diagrama
local tipo BPMN simplificado, no ejecutable, que no representa el estado de una
migración real. Tiene descripción accesible y se conserva sin modificar.
El contenedor conserva desplazamiento horizontal y acceso por teclado si algún contenido desborda. No requiere plugins, JavaScript ni servicios de diagramación externos.

Tras actualizar dependencias, revise también la página 404 y los textos de búsqueda.

## Contribución segura

- Lea [AGENTS.md](AGENTS.md) y la [guía de trabajo con IA](docs/ai-guide.md).
- Registre las versiones exactas de origen y destino y el alcance de código y base de datos.
- Marque los borradores como no verificados; aporte evidencias sin datos sensibles antes de afirmar su verificación.
- No incluya datos de clientes, secretos, código propietario ni infraestructura interna. La excepción de identificación de esta edición permite mencionar Equipavic y Smarttract al explicar el diseño; no extienda ese permiso a sus datos o evidencias.

## Publicación y licencia

La documentación está publicada en el [sitio web](https://hito2026.github.io/hito-migrations/).
Las fuentes están en el [repositorio público de Hito](https://github.com/hito2026/hito-migrations).
La portada respondió HTTP 200 durante la comprobación de publicación del 13 de octubre de 2026.
Esa comprobación no acredita la publicación del nuevo diseño; sus cambios requieren
una publicación y una verificación posteriores. Los procedimientos siguen siendo
borradores no verificados: publicar el sitio no valida una migración.

La publicación utiliza la rama `gh-pages` y GitHub Pages, sin un flujo
automático de despliegue. Antes de publicar, revise las fuentes y excluya las notas
operativas privadas, los metadatos locales y los artefactos de entorno y compilación.
La elección de licencia sigue pendiente del propietario; aquí no se concede ninguna licencia.

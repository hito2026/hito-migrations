# Hito migrations

Base documental para migraciones de Odoo, preparada para publicación pública.
Los esquemas son **borradores no verificados**, no procedimientos probados ni
pruebas de migraciones exitosas. La guía tiene seis entradas:
[Introducción](docs/index.md), [Procedimiento](docs/procedure.md),
[Instrucciones del usuario](docs/user-instructions.md), [Gentle Shell](docs/gentle-shell.md)
[Arquitectura](docs/architecture.md) y [Plan técnico](docs/spiral-strategy.md).

El [manual de uso de Gentle Shell](docs/gentle-shell.md) tiene una sección propia en el menú.
Incluye preparación y acceso desde Windows (PowerShell), Linux y macOS, con un prompt
copiable por sistema para realizar la configuración con ayuda de una IA; después continúa
con comandos comunes en el servidor y mensajes para iniciar, retomar y entregar una migración.
Utiliza ejemplos anónimos. La sección Arquitectura y su diagrama local distinguen
administración en la Mac de Ale, acceso de usuarios y ejecución en PC-ALE; no incluyen
IPs, dominios privados ni credenciales. La edición documental 0.2.3 incorpora esta sección.

**Plan técnico** muestra directamente un único documento: la estrategia de migración
en espiral, con sus seis ciclos, clasificación de módulos, estados de evidencia y
coordinación por oleadas. No es un catálogo de archivos. Incluye un enlace al Markdown
original para copiarlo a otro arnés; la fuente se mantiene en `docs/spiral-strategy.md`.
No requiere Gentle Shell ni acredita resultados de una migración real.

Las guías anteriores conservan sus URL. La estrategia en espiral pasa al menú como
Plan técnico; las otras ocho siguen como referencias fuera del menú. `not_in_nav` en
`mkdocs.yml` declara esa exclusión; no elimina páginas ni sus entradas de búsqueda.

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
Las veintiuna pruebas comprueban las catorce rutas (cinco principales y nueve anteriores),
el idioma, las URL canónicas, el menú de seis entradas, el documento único del plan en
espiral y su enlace Markdown, y los diagramas de proceso y arquitectura,
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

El procedimiento usa `docs/assets/migration-process.svg`: un diagrama local tipo BPMN
simplificado, con actores, tareas, decisiones y retornos. No es un modelo BPMN ejecutable
ni representa el estado de una migración real. Tiene descripción accesible y equivalente
en texto; se adapta al ancho del contenido y puede abrirse por separado para ampliarlo.
El contenedor conserva desplazamiento horizontal y acceso por teclado si algún contenido desborda. No requiere plugins, JavaScript ni servicios de diagramación externos.

Tras actualizar dependencias, revise también la página 404 y los textos de búsqueda.

## Contribución segura

- Lea [AGENTS.md](AGENTS.md) y la [guía de trabajo con IA](docs/ai-guide.md).
- Registre las versiones exactas de origen y destino y el alcance de código y base de datos.
- Marque los borradores como no verificados; aporte evidencias sin datos sensibles antes de afirmar su verificación.
- No incluya datos de clientes, secretos, código propietario ni infraestructura interna.

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

# Hito migrations

Base documental para migraciones de Odoo, preparada para publicación pública.
Los esquemas son **borradores no verificados**, no procedimientos probados ni
pruebas de migraciones exitosas. Comience por el [índice de documentación](docs/index.md).

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
Las pruebas comprueban las ocho rutas, el idioma, las URL canónicas, la estructura
de navegación, las tarjetas y los recursos locales. Revise también en navegador
la búsqueda, el foco de teclado y la navegación de escritorio y móvil.
Compilar el sitio no verifica una migración; consulte la [lista de validación](docs/validation.md).

### Tema y diseño

MkDocs Material (`>=9.6,<10`) aporta búsqueda superior, navegación lateral y tabla
de contenidos de las guías. La interfaz usa `language: es`, búsqueda `lang: es`
y conserva `mkdocs[i18n]` para las traducciones. `font: false` evita cargar fuentes
externas; `docs/stylesheets/extra.css` define los acentos de Hito y las tarjetas
con tipografía del sistema. No hay plantillas ni JavaScript personalizados.
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

# Introducción

[**Abrir el manual de Gentle Shell**](gentle-shell.md){ .md-button .md-button--primary }

Comandos para acceder al servidor y empezar a trabajar en una migración.

## La idea del proyecto

Hito propone una forma ordenada de preparar y conducir migraciones de Odoo:
**saber qué hay que conservar, dividir el trabajo y comprobar cada avance antes de continuar**.
Esta guía usa como referencia Odoo 17.0 → 19.0 en Odoo.sh; la ruta de actualización
se confirma para cada edición y servicio.

No se trata solo de adaptar módulos. También hay que conservar los datos históricos,
validar los procesos de negocio y preparar el paso a producción con recuperación posible.

## Cómo trabajamos

- **El usuario aporta el contexto y decide:** alcance, accesos, prioridades y aceptación.
- **Coordinación organiza:** inventario, dependencias, responsables y preguntas pendientes.
- **El equipo técnico implementa y verifica:** cambios pequeños, pruebas y resultados trazables.
- **El proveedor de actualización confirma su cobertura y entrega la base actualizada** por la vía acordada.

El código y los datos avanzan en paralelo, pero se aceptan por separado.
La IA puede ayudar a analizar, adaptar y revisar; no decide permisos ni aprueba una migración.
Si falta información, se formula una pregunta concreta. No se completa con suposiciones.

<div class="draft-notice" role="note" markdown>
**Borrador no verificado.** Se describe una propuesta de trabajo, no una migración exitosa
ni una receta de ejecución probada. Los datos y evidencias del proyecto se mantienen
en un registro privado autorizado; el sitio público permanece anonimizado.
</div>

## Cómo usar esta guía

1. Lea el [Procedimiento](procedure.md) para entender las etapas, actores y decisiones.
2. Complete y entregue las [Instrucciones del usuario](user-instructions.md) para comenzar.
3. Al cerrar cada etapa, revise lo comprobado y autorice solo el siguiente trabajo acotado.

**Un módulo que instala no demuestra que sus datos se hayan migrado bien.** La aceptación
requiere resultados de código, funcionamiento e historia, más una decisión humana.

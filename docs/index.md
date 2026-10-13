# Planifique una migración de Odoo de forma segura

Documentación de Hito para organizar el alcance, las decisiones y las evidencias de una migración.
Elija un tema para comenzar; use la búsqueda para localizar conceptos o plantillas.

<div class="draft-notice" role="note" markdown>
**Borrador no verificado.** Este sitio es una base documental, no un manual listo para ejecutar.
Toda la orientación inicial está **sin verificar**. No se afirma ningún resultado de migración.
</div>

## Explore la documentación

<div class="topic-cards" markdown>

<div class="topic-card" markdown>
### [Manual de migración](migration-manual.md)
Organice las fases, las responsabilidades y las condiciones de un ensayo autorizado.
</div>

<div class="topic-card" markdown>
### [Orientación por versiones](versions.md)
Declare el origen, el destino y las dependencias antes de evaluar la compatibilidad.
</div>

<div class="topic-card" markdown>
### [Recetas técnicas](recipes.md)
Estructure propuestas técnicas acotadas y haga visibles los supuestos pendientes.
</div>

<div class="topic-card" markdown>
### [Lista de validación](validation.md)
Defina criterios de aceptación, parada y recuperación con evidencias observables.
</div>

<div class="topic-card" markdown>
### [Errores conocidos](known-errors.md)
Registre fallos reproducibles, su contexto y las limitaciones de las soluciones propuestas.
</div>

<div class="topic-card" markdown>
### [Guía de trabajo con IA](ai-guide.md)
Acuerde tareas y límites de privacidad sin delegar la autorización de una migración.
</div>

<div class="topic-card" markdown>
### [Plantilla de caso anonimizado](case-template.md)
Resuma un ensayo autorizado sin publicar datos sensibles ni atribuir éxitos sin pruebas.
</div>

</div>

## Etiquetas de evidencia

- **No verificado:** esquema, hipótesis o procedimiento propuesto; no es una instrucción de ejecución.
- **Verificado en un contexto declarado:** evidencias revisadas de un ensayo autorizado,
  con versiones exactas, alcance, fecha y limitaciones registrados.
- **Requiere revalidación:** existen evidencias, pero cambiaron las versiones, las dependencias o el alcance.

La verificación depende del contexto; nunca garantiza que otros entornos funcionen.
Una compilación estricta del sitio comprueba la integridad documental, no la corrección de una migración.

## Límites

Separe el trabajo de compatibilidad de módulos y código de la migración de base de datos,
esquema y datos. Las evidencias de una línea de trabajo no sustituyen las de la otra.
Use solo material apto para publicación; las copias de seguridad, las operaciones sobre
bases de datos y la publicación requieren autorización humana.

# Planifique una migración de Odoo de forma segura

Este sitio es una base documental, no un manual de migración listo para ejecutar.
Toda la orientación inicial está **sin verificar**. No se afirma ningún resultado de migración.

## Elija el siguiente paso

| Necesidad | Punto de partida |
| --- | --- |
| Planificar fases y responsabilidades | [Manual de migración](migration-manual.md) |
| Definir versiones de origen y destino | [Orientación por versiones](versions.md) |
| Proponer un procedimiento técnico acotado | [Índice de recetas](recipes.md) |
| Definir criterios de aceptación y reversión | [Lista de validación](validation.md) |
| Registrar un fallo reproducible | [Errores conocidos](known-errors.md) |
| Trabajar con un asistente de IA | [Guía de trabajo con IA](ai-guide.md) |
| Resumir un ensayo sin datos sensibles | [Plantilla de caso](case-template.md) |

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

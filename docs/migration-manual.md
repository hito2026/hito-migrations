# Esquema del manual de migración

**Estado: esquema no verificado.** Complete los criterios siguientes antes de proponer la ejecución.
Esta página no contiene comandos de migración probados.

## 1. Establecer el acuerdo de trabajo

Registre las versiones de Odoo de origen y destino, la edición, el entorno de ejecución,
la versión de base de datos, el inventario de módulos y las versiones de dependencias.
Identifique los roles autorizados sin publicar datos personales. Acuerde el tiempo de
indisponibilidad, los umbrales de aceptación y el alcance excluido.
Use la [plantilla de orientación por versiones](versions.md).

## 2. Separar las líneas de trabajo

| Línea | Preguntas por resolver |
| --- | --- |
| Código | ¿Qué API, vistas, recursos y dependencias necesitan cambios de compatibilidad? |
| Base de datos | ¿Qué esquemas, registros y metadatos necesitan una transformación aprobada? |
| Integración | ¿Qué interfaces deben aislarse y comprobarse durante el ensayo? |

La compatibilidad del código no demuestra por sí sola la corrección de la base de datos ni la aceptación funcional.

## 3. Diseñar un ensayo autorizado

- Use un entorno aislado aprobado y un registro documental apto para publicación.
- Defina la cobertura de las copias de seguridad, la verificación de restauración y el plazo para decidir la reversión.
- Mantenga los detalles sensibles de ejecución en un sistema privado aprobado, no en este sitio.
- Redacte [recetas](recipes.md) acotadas; identifique las incógnitas y las condiciones de parada.

## 4. Validar y decidir

Aplique la [lista de aceptación](validation.md) a ambas líneas de trabajo.
Registre los fallos con la [plantilla de errores](known-errors.md); no oculte excepciones.
Una persona debe aprobar cualquier paso a producción tras revisar las evidencias del ensayo
y de recuperación. Registre el resultado sin datos sensibles con la [plantilla de caso](case-template.md).

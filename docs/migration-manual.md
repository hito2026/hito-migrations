# Esquema del manual de migración

**Estado: esquema no verificado.** Complete los criterios siguientes antes de proponer la ejecución.
Esta página no contiene comandos de migración probados.

## 1. Establecer el acuerdo de trabajo

Registre las versiones de Odoo de origen y destino, la edición, el entorno de ejecución,
la versión de base de datos, el inventario de módulos y las versiones de dependencias.
Identifique los roles autorizados sin publicar datos personales. Acuerde el tiempo de
indisponibilidad, los umbrales de aceptación y el alcance excluido.
Use la [plantilla de orientación por versiones](versions.md) y la
[ficha de entrada anonimizada](migration-templates.md).

## 2. Separar las líneas de trabajo

| Línea | Preguntas por resolver |
| --- | --- |
| Código | ¿Qué API, vistas, recursos y dependencias necesitan cambios de compatibilidad? |
| Base de datos | ¿Qué esquemas, registros y metadatos necesitan una transformación aprobada? |
| Integración | ¿Qué interfaces deben aislarse y comprobarse durante el ensayo? |

La compatibilidad o publicación del código no demuestra por sí sola la corrección de la
base de datos ni la aceptación funcional o contable.

### Planificar por espirales y módulos

La [estrategia en espiral](spiral-strategy.md) propone S1 entrada, S2 clasificación,
S3 portado, S4 runtime aislado en Odoo.sh Development, S5 aceptación histórica sobre
una copia migrada en Staging y S6 planificación y ensayo de corte/recuperación.
Es una propuesta **no verificada**, no instrucciones de ejecución en producción.
S3/S4 iteran por módulo; S6 se planifica desde el inicio. S5 requiere una base de datos
actualizada y una restauración aprobada por una persona; no se deriva de un S4 exitoso.
Use las [tarjetas de módulo](migration-templates.md) para separar estado, disposición
y evidencias de código, runtime y datos.

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

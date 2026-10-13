# Índice de orientación por versiones

**Estado: plantilla no verificada.** Aún no hay orientación verificada para ningún par de versiones.
No deduzca rutas de migración admitidas a partir de este índice.

## Registrar un par de versiones

| Campo | Información requerida |
| --- | --- |
| Origen | Versión y compilación exactas de Odoo, edición y versiones de dependencias pertinentes |
| Destino | Versión y compilación exactas de Odoo, edición y versiones de dependencias pertinentes |
| Ruta | Propuesta directa o por etapas; documentación pública que la respalda |
| Alcance de código | Cambios de compatibilidad de módulos y módulos excluidos |
| Alcance de base de datos | Transformaciones de esquema y datos y conjuntos de datos excluidos |
| Evidencias | Registro del ensayo sin datos sensibles, fecha y rol de quien revisa |
| Estado | No verificado, verificado en un contexto declarado o requiere revalidación |

## Plantilla de entrada

- **Par:** `<origen>` → `<destino>`; edición `<edición>`.
- **Requisitos previos:** `<supuestos respaldados y referencias a fuentes públicas>`.
- **Cambios de código:** `<trabajo de compatibilidad propuesto; evidencias o incógnitas>`.
- **Cambios de base de datos:** `<transformaciones propuestas; evidencias o incógnitas>`.
- **Recuperación:** `<evidencias de copia de seguridad y restauración y criterio de reversión>`.
- **Aceptación:** `<comprobaciones, umbrales y resultados sin datos sensibles>`.
- **Límites:** `<módulos no admitidos, pasos intermedios y riesgos pendientes>`.

Contraste las afirmaciones de las fuentes con la documentación oficial aplicable antes de usarlas.
Un par de versiones o una edición diferentes requieren una nueva evaluación, no un estado copiado.

Continúe con el [manual](migration-manual.md) y la [validación](validation.md).

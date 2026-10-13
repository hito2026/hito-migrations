# Plantilla de caso anonimizado

**Estado: plantilla no verificada.** No es un informe de una migración completada.
Use solo material aprobado explícitamente para publicación; omita los detalles dudosos.

## Contexto

- **Etiqueta del caso:** `<etiqueta genérica; sin identificadores de clientes ni infraestructura>`.
- **Par de versiones:** `<origen exacto>` → `<destino exacto>`; `<edición>`.
- **Dependencias:** `<contexto del entorno de ejecución y módulos apto para publicación>`.
- **Alcance:** `<trabajo de código>` y `<trabajo de base de datos>`, con exclusiones explícitas.
- **Estado de evidencia:** `<no verificado / verificado en un contexto declarado / requiere revalidación>`.

## Plan y autorización

Describa los objetivos aprobados, los umbrales de aceptación y los roles responsables.
Resuma la cobertura de las copias de seguridad, las evidencias de restauración, los criterios
de reversión y los puntos de decisión sin revelar ubicaciones de almacenamiento,
credenciales ni detalles operativos privados.

## Resultados que completar solo tras observarlos

| Área | Esperado | Observado | Evidencia / limitación |
| --- | --- | --- | --- |
| Compatibilidad de código | `<criterio>` | `<pendiente>` | `<pendiente>` |
| Invariantes de base de datos | `<criterio>` | `<pendiente>` | `<pendiente>` |
| Aceptación funcional | `<criterio>` | `<pendiente>` | `<pendiente>` |
| Ensayo de recuperación | `<criterio>` | `<pendiente>` | `<pendiente>` |

## Revisión y lecciones

Registre fallos sin datos sensibles, comprobaciones omitidas, fecha, rol de quien revisa y decisión humana.
Indique qué no puede generalizarse a otras versiones o entornos.
Confirme el permiso de publicación antes de publicar; el anonimato no equivale a autorización.

Consulte [validación](validation.md) y [errores conocidos](known-errors.md) para los campos de evidencia.

# Índice de recetas técnicas

**Estado: plantilla no verificada.** No hay recetas probadas registradas.
Los temas siguientes son espacios para documentar, no técnicas de migración recomendadas.

## Temas propuestos

| Tema | Línea de trabajo | Evidencias necesarias antes de usarlo |
| --- | --- | --- |
| Compatibilidad de módulos | Código | Par de versiones exactas y pruebas de compatibilidad |
| Transformación de esquema y datos | Base de datos | Ensayo, invariantes y evidencias de restauración |
| Comprobaciones de integración | Ambas | Comprobaciones aisladas y aceptación funcional |

## Plantilla de receta

1. **Objetivo y estado:** `<resultado acotado; etiqueta de evidencia>`.
2. **Contexto:** `<versiones exactas, edición, dependencias y alcance>`.
3. **Requisitos previos:** `<autorización, aislamiento y copia de seguridad validada>`.
4. **Propuesta de procedimiento:** `<pasos con fuentes públicas; sin comandos supuestos>`.
5. **Evidencias esperadas:** `<resultado observable y umbral de aceptación por paso>`.
6. **Condiciones de parada:** `<señales de fallo y rol al que consultar>`.
7. **Recuperación:** `<referencia al procedimiento de restauración y limitaciones comprobadas>`.
8. **Registro de verificación:** `<fecha, resultados sin datos sensibles y rol de quien revisa>`.

## Criterio para declarar la verificación

Mantenga la propuesta como no verificada hasta que un ensayo autorizado aporte evidencias revisadas.
Indique qué comprobaciones de código y base de datos se realizaron y cuáles no.
Nunca publique instrucciones destructivas ejecutables sin aprobación humana explícita.

Use la [lista de validación](validation.md) y la [plantilla de errores](known-errors.md).

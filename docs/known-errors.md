# Plantilla de errores conocidos

**Estado: plantilla no verificada.** Aún no se han catalogado errores de migración confirmados.
No presente un diagnóstico plausible como una solución demostrada.

## Entrada de error

| Campo | Información requerida |
| --- | --- |
| Etiqueta | Título descriptivo genérico, no un identificador de cliente |
| Contexto | Versiones exactas, edición, dependencias y línea de código o base de datos |
| Síntoma | Mensaje mínimo sin datos sensibles y efecto observado |
| Reproducción | Pasos aislados autorizados; resultado esperado frente al real |
| Hipótesis | Causa posible, separada explícitamente de la evidencia confirmada |
| Resolución | Corrección propuesta o verificada, con etiqueta de evidencia y límites |
| Recuperación | Condición de parada, dependencia de copia de seguridad y restauración y decisión humana |
| Evidencias | Resultados sin datos sensibles, fecha y rol de quien revisa |

## Comprobación antes de publicar

- Elimine credenciales, nombres de servidores, datos personales y fragmentos propietarios.
- Resuma los registros; no pegue volcados ni trazas de error con rutas privadas.
- Omita cualquier material cuyo permiso de publicación no esté claro.
- Indique los riesgos pendientes y las comprobaciones omitidas aunque una solución provisional parezca funcionar.

Una corrección verificada necesita un fallo reproducible y una nueva prueba exitosa en el
contexto declarado. En caso contrario, mantenga la etiqueta no verificada y solicite evaluación humana.

Vuelva a las [recetas](recipes.md) o a la [lista de validación](validation.md).

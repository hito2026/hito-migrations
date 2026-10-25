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

## Lecciones cautelares genéricas: no verificadas

Estas hipótesis no son incidentes confirmados ni recetas probadas; requieren evidencias
por versión y autorización antes de proponer cualquier actuación.

### Dependencias y auto-instalación

El grafo transitivo, incluidas reglas de auto-instalación, puede exceder el inventario
aprobado. Calcule y revise el grafo completo antes de proponer una inicialización.
Si introduce módulos fuera de alcance, deténgase y solicite ampliación humana;
no interprete una dependencia implícita como autorización.

### Fallo de obtención de objetos históricos en un clon parcial

Un fallo al obtener objetos históricos de un clon parcial es un incidente de herramientas,
no prueba de corrupción del repositorio ni de los datos. Una posible vía de investigación,
no verificada, es inspeccionar una fuente prístina en un espacio aislado autorizado y
contrastar referencias y disponibilidad de objetos. No repare destructivamente el espacio
original ni atribuya una causa sin evidencia; esta página no aporta comandos de reparación.

### Posible sustitución de módulos de pago ADHOC

La relación `account_payment_group` → `account_payment_pro` (+ `l10n_ar_payment_bundle`
para pagos agrupados) se observó en un caso 17 → 19 de ADHOC: `account_payment_pro` hace
que cada pago sea el recibo; el grupo desaparece y sus menús dan 404. **La conversión de
datos de los grupos no está verificada**: ADHOC no incluye script para ella en 19.0.
Ver [lecciones de base migrada](upgraded-db-lessons.md). Confirme versiones, cobertura
funcional, historia y numeración en su contexto.

### Reglas fiscales y controles de seguridad

Un fallback fiscal fijo puede ocultar una configuración incompleta; una validación solo
mediante `onchange` puede no cubrir otras vías de escritura. Son riesgos genéricos por
investigar con pruebas autorizadas de comportamiento y controles del servidor, no
vulnerabilidades confirmadas ni correcciones verificadas. No publique valores reales.

Problemas observados sobre una base migrada: [lecciones de base migrada](upgraded-db-lessons.md).
Registre las decisiones en las [tarjetas de módulo](migration-templates.md).
Vuelva a las [recetas](recipes.md) o a la [lista de validación](validation.md).

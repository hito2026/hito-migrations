# Estrategia de migración en espiral

**Plan técnico general de migración.** Este es el documento completo del plan en espiral.
Para llevarlo a otro arnés, [abra el Markdown original](https://raw.githubusercontent.com/hito2026/hito-migrations/refs/heads/docs/spiral-strategy/docs/spiral-strategy.md),
seleccione todo y copie con **Ctrl+A → Ctrl+C** o **⌘A → ⌘C** en Mac.
El enlace muestra la última fuente subida a la rama documental; no requiere Gentle Shell.

**Estado: propuesta no verificada.** Organice decisiones y evidencias en ciclos pequeños,
no como una receta ejecutable ni como una migración exitosa. La compatibilidad o
publicación del código no acredita la migración de datos ni la aceptación funcional o contable.

## Ruta de planificación

1. Complete la [ficha de entrada](migration-templates.md) y acuerde alcance y permisos.
2. Clasifique el inventario y sus dependencias antes de proponer oleadas de módulos.
3. Itere código y runtime; mantenga separadas las evidencias sobre datos históricos.
4. Solicite decisiones humanas en cada límite; planifique la recuperación desde el inicio.

## Espirales y condiciones de avance

Las espirales no son una secuencia rígida: S3 y S4 se repiten por módulo; un hallazgo
puede devolver el trabajo a S1 o S2. S6 comienza a planificarse temprano.

| Espiral | Objetivo propuesto | Evidencia o condición de avance |
| --- | --- | --- |
| S1 — Entrada y restricciones | Acordar versiones, edición, runtime, permisos, alcance y exclusiones | Ficha de entrada revisada; decisiones pendientes visibles |
| S2 — Inventario y clasificación | Distinguir disposiciones y calcular dependencias completas | Grafo revisado, responsables y oleadas propuestas dentro del alcance |
| S3 — Portado de código | Adaptar cada módulo y sus pruebas al destino | Evidencia local de compatibilidad; no implica runtime ni datos aceptados |
| S4 — Runtime aislado | Evaluar carga y comportamiento en Odoo.sh Development aislado | Resultados de pruebas de runtime, integraciones aisladas y fallos registrados |
| S5 — Aceptación histórica | Evaluar una copia migrada en Staging | Base de datos actualizada y restauración aprobada por una persona; conciliación y aceptación humana |
| S6 — Plan y ensayo de corte/recuperación | Acordar criterios, responsabilidades y ensayo autorizado | Evidencias del ensayo y decisión humana; no habilita ejecutar en producción |

S4 no sustituye S5: un runtime limpio no demuestra conservación de historia, numeración,
saldos ni flujos de negocio. S5 está bloqueada sin una base de datos ya actualizada
por una vía autorizada y sin aprobación humana de su restauración. Esta propuesta no
incluye instrucciones para actualizarla, restaurarla ni operar en producción.
Los detalles privados del ensayo y de recuperación quedan fuera del sitio público.

## Clasificar antes de portar

La clasificación expresa una decisión propuesta, no un estado de avance. Que exista un
addon homónimo en destino no demuestra equivalencia de comportamiento, datos o seguridad.

| Disposición | Pregunta que debe resolverse |
| --- | --- |
| Portar (`port`) | ¿Qué adaptación requiere y con qué pruebas? |
| Rama destino presente (`target branch present`) | ¿La rama cubre las funciones e historia requeridas? |
| Destino más parche (`target plus patch`) | ¿Qué brecha concreta justifica un parche acotado? |
| Disponible upstream (`upstream available`) | ¿La versión, licencia y cobertura upstream son adecuadas? |
| Reemplazo (`replacement`) | ¿Hay equivalencia demostrada y una ruta de datos aprobada? |
| Decisión pendiente (`decision needed`) | ¿Qué evidencia o autorización falta? |
| Candidato a retirar (`drop candidate`) | ¿Quién acepta el impacto funcional y sobre datos históricos? |

Revise dependencias directas, transitivas y reglas de auto-instalación antes de cualquier
inicialización propuesta. Si el grafo excede el alcance aprobado, deténgase y solicite
ampliación; no incorpore módulos implícitamente. Véanse las [lecciones cautelares](known-errors.md).

## Estados del tablero y evidencia

Estos nombres son un vocabulario propuesto, no certificaciones. No avance por inferencia
ni copie el estado de otro entorno. Registre contexto, fecha, esperado, observado y límites.

| Estado | Significado mínimo propuesto |
| --- | --- |
| `identified` | Módulo inventariado; alcance aún por evaluar |
| `classified` | Disposición y dependencias revisadas |
| `porting` | Adaptación en curso con responsable exclusivo |
| `ported_local` | Compatibilidad local respaldada por comprobaciones registradas |
| `ported` | Código integrado/revisado en el destino autorizado; publicación, si existe, registrada aparte |
| `runtime_passed` | Pruebas acordadas de runtime aislado superadas en contexto declarado |
| `data_validated` | Invariantes y conciliación histórica comprobadas sobre la copia migrada autorizada |
| `accepted` | Aceptación humana explícita funcional y contable, cuando corresponda, con riesgos residuales |
| `blocked` | Impedimento explícito, responsable de decisión y condición de desbloqueo |

Conserve el último estado respaldado y el historial de bloqueos. `ported` no implica
`runtime_passed`; `runtime_passed` no implica `data_validated`; ninguno equivale a
`accepted`. Publicar código no es aceptar una migración. La aceptación requiere revisar
las evidencias separadas de código, runtime y datos y las comprobaciones omitidas.

## Coordinación por oleadas

Proponga primero dependencias base y después consumidores; documente ciclos y bloqueos
antes de asignar trabajo. Solo proponga paralelismo con worktrees y ramas aislados,
propiedad exclusiva de un conjunto estrecho de archivos y contratos de dependencia claros.
Crear esos espacios o integrar cambios también requiere los permisos humanos aplicables.

El coordinador mantiene tablero, oleadas e integración y es responsable de Git dentro
de lo autorizado; los trabajadores entregan cambios y evidencias, no amplían el alcance
ni publican por su cuenta. Detenga una colisión de archivos o un cambio de contrato antes
de continuar. Amplíe estas reglas con la [guía de IA](ai-guide.md).

## Siguiente decisión

Use las [plantillas reutilizables](migration-templates.md) para registrar lo pendiente y
la [lista de validación](validation.md) para acordar la aceptación. Vuelva al
[manual](migration-manual.md) si cambian permisos, alcance o condiciones de recuperación.

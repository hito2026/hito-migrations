# Lista de validación y aceptación

**Estado: lista no verificada.** Marcar casillas requiere evidencias, no suposiciones.
Defina umbrales específicos del proyecto antes de un ensayo autorizado.

## Antes de la ejecución

- [ ] Se registraron las versiones exactas de origen y destino, la edición y las dependencias.
- [ ] Se acordaron el alcance de código y base de datos, las exclusiones y los roles responsables.
- [ ] Una persona autoriza el entorno, las operaciones y el tratamiento de datos.
- [ ] La cobertura, la retención y el acceso a las copias de seguridad están aprobados en un registro privado.
- [ ] Se ensayó la restauración; se registraron el tiempo de recuperación y las limitaciones.
- [ ] Son explícitos los criterios de reversión, la autoridad para decidir y los límites del paso a producción.

## Evidencias de aceptación

| Área | Evidencias que registrar sin datos sensibles |
| --- | --- |
| Código | Comprobaciones de compatibilidad, carga de módulos y resultados de pruebas pertinentes |
| Base de datos | Invariantes acordadas de esquema y datos y resultados de conciliación |
| Negocio | Flujos críticos acordados y decisión humana de aceptación |
| Operaciones | Tiempos, comprobaciones de integración aisladas y resultados de recuperación |

- [ ] Cada resultado indica el valor esperado, el observado y si la comprobación pasó o falló.
- [ ] Los fallos, las comprobaciones omitidas y las diferencias sin explicar siguen visibles.
- [ ] Las evidencias identifican el contexto y la fecha sin exponer datos sensibles.
- [ ] Una persona acepta los riesgos residuales o bloquea el paso a producción; la decisión queda registrada.

## Detenerse y recuperar

Deténgase ante invariantes incumplidas, copias de seguridad ausentes, efectos inesperados
o retirada de la aprobación. Consulte a la persona autorizada; no improvise reparaciones
ni comandos de reversión. La recuperación debe contemplar las escrituras posteriores al
paso a producción y los efectos externos, no solo los archivos.

Registre excepciones en [errores conocidos](known-errors.md) y resultados en [casos](case-template.md).

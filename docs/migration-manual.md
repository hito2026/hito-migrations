# Guía técnica de migración

Esta guía propone un recorrido para el equipo técnico que prepara una migración de
**Odoo 17.0 a 19.0 en Odoo.sh**: por dónde empezar, qué hacer y qué consultar antes
de avanzar. Reúne criterios y aprendizajes anonimizados, no el relato de un cliente.

**Borrador no verificado.** No es una receta de comandos probados ni acredita una
migración exitosa. Confirme la ruta de actualización según la edición y el servicio.

## Por dónde empezar

Antes de modificar código, reúna tres cosas:

1. **Una ficha de entrada:** versiones, alcance, accesos autorizados y responsables.
2. **Un inventario real:** módulos instalados y utilizados, sus fuentes y dependencias.
3. **Una lista de decisiones:** qué falta saber, quién responde y qué impide continuar.

Use la [ficha de entrada y las tarjetas de módulo](migration-templates.md) en un
registro privado autorizado. No publique datos, referencias reales, credenciales ni
evidencias de clientes. Si algo no aplica, registre `N/A` y el motivo; si no se sabe,
registre una pregunta, no una suposición.

## 1. Acordar el punto de partida

**Qué y por qué.** Defina qué se migra y con qué permisos. Sin una línea base clara,
es fácil adaptar código que no coincide con lo que está funcionando.

**Cómo hacerlo:**

- Registre versiones y compilaciones exactas, edición, dependencias y referencias desplegadas.
- Identifique quién coordina, quién adapta, quién verifica y quién acepta cada proceso.
- Acuerde procesos críticos, exclusiones, entornos y operaciones autorizadas.

**Qué consultar:** al responsable técnico, cuál es la línea base y cómo detectar
cambios posteriores; al propietario y los referentes funcionales, qué debe conservarse,
qué queda fuera y cuánta indisponibilidad es tolerable.

**Para avanzar:** ficha revisada y responsables definidos. Un acceso disponible no
es permiso para modificar código, restaurar bases ni operar en producción.

## 2. Inventariar lo que realmente se usa

**Qué y por qué.** Compare código disponible, módulos instalados y uso efectivo.
No son lo mismo: una personalización puede estar en Studio o depender de otro repositorio.

**Cómo hacerlo:**

- Liste módulos nativos, Enterprise, de terceros, propios y personalizaciones de Studio.
- Ubique fuentes autorizadas, submódulos, licencias y destino propuesto de cada repositorio.
- Revise dependencias directas, transitivas, auto-instalables y ciclos entre módulos.
- Incluya informes, permisos, integraciones y procesos críticos confirmados por sus usuarios.

**Qué consultar:** al responsable técnico, dónde está cada fuente y qué está desplegado;
al referente funcional, qué se usa realmente y con qué escenario se comprobará.

**Para avanzar:** inventario trazable y dependencias dentro del alcance aprobado.
Si faltan fuentes o aparecen módulos no autorizados, registre el bloqueo antes de asignarlos.

## 3. Elegir qué hacer con cada módulo

**Qué y por qué.** No porte todo por defecto. Puede existir una alternativa en 19.0,
pero compartir nombre no garantiza conservar funciones, permisos ni datos.

**Cómo hacerlo:**

- Abra una [tarjeta por módulo](migration-templates.md#tarjeta-reutilizable-de-modulo).
- Proponga adaptar, usar una versión disponible, aplicar un parche, reemplazar,
  investigar o retirar, con su justificación y licencia.
- Compare funciones y datos que deben conservarse. Registre brechas y pruebas esperadas.
- Ordene el trabajo por dependencias: primero bases compartidas, luego consumidores e informes.

**Qué consultar:** al dueño funcional, si acepta el reemplazo o la retirada; al
responsable de datos, qué sucede con la historia; al titular de derechos, si el uso está permitido.

**Para avanzar:** una decisión respaldada por módulo. Si hay pérdida funcional,
impacto histórico o licencia sin resolver, no lo marque como listo para adaptar.

## 4. Resolver la actualización de datos en paralelo

**Qué y por qué.** Adaptar código y actualizar la base son trabajos distintos.
Puede avanzar con el código autorizado mientras se confirma la cobertura del proveedor;
no puede aceptar la historia sin probar una copia migrada.

**Cómo hacerlo:** solicite al proveedor la ruta admitida, cobertura estándar y de
personalizaciones, exclusiones y condiciones de entrega. El responsable de datos
registra la respuesta, las transformaciones propuestas y quién autorizará la restauración.
Una solicitud enviada no demuestra que los datos se hayan convertido.

### Preguntas que conviene anticipar

**Qué consultar:** use estas preguntas según los dominios aplicables al proyecto.
El técnico reúne las respuestas;
las decisiones funcionales, fiscales y de seguridad corresponden a sus responsables.

| Tema | Qué preguntar y a quién |
| --- | --- |
| Pagos y cheques | Al referente contable: ¿cómo se conservarán agrupaciones, estados, pendientes, vínculos y numeración? Contraste la cobertura con el proveedor. |
| Retenciones, IVA y ajuste por inflación | Al referente fiscal/contable: ¿qué historia, documentos pendientes, liquidaciones y resultados deben conciliarse? |
| Comprobantes y remitos | Al referente funcional/contable: ¿qué tipos, relaciones y numeración legal deben continuar? |
| Stock y fabricación | A operaciones: ¿se mantienen los flujos o se propone un rediseño MRP? ¿Con qué escenarios se aceptará? |
| Campos, informes y permisos | A los dueños funcionales y seguridad: ¿se conserva el significado de los datos? ¿Quién podrá ver costos, pestañas de producto y editar información? |
| Informes con SQL arbitrario | A seguridad: ¿se permite esa capacidad, con qué restricciones y pruebas de acceso negativo, o debe retirarse? |
| Contingencia fiscal | Al responsable fiscal y al propietario: ¿qué política está permitida ante indisponibilidad o falta de cobertura y cuándo debe detenerse la operación? |

**Para avanzar hacia la validación histórica:** cobertura y pendientes documentados,
base actualizada entregada y restauración aislada autorizada. Una respuesta desconocida
queda con rol decisor, fecha objetivo y condición de desbloqueo; no se inventa una equivalencia.

## 5. Adaptar y probar en ciclos pequeños

**Qué y por qué.** Trabaje por grupos de dependencias y compruebe cada entrega antes
de acumular cambios. Cambiar el manifest o lograr un build no demuestra que el módulo funcione.

**Cómo hacerlo:**

1. Acuerde el alcance del grupo, archivos, contratos entre módulos y pruebas esperadas.
2. Revise API, vistas, seguridad, recursos y dependencias para 19.0; adapte el código y sus pruebas.
3. En **Development aislado y autorizado**, compruebe instalación, permisos y escenarios acordados.
   Controle correo, bancos, servicios fiscales y otras integraciones para evitar efectos externos.
4. Registre esperado, observado, contexto y fallos. Corrija y repita el ciclo cuando corresponda.

Con varios desarrolladores o agentes, asigne archivos exclusivos y ramas o worktrees
aislados. Coordinación mantiene el tablero y organiza la integración dentro de los permisos
concedidos; una colisión o un cambio de contrato exige revisar la asignación.

**Qué consultar:** al responsable técnico, dependencias y aislamiento; a los referentes
funcionales, resultados esperados; a coordinación, cualquier ampliación de alcance.

**Para avanzar:** pruebas acordadas superadas y evidencia registrada. Distinga
`ported_local`, `ported` y `runtime_passed`: código local, código integrado y runtime
comprobado no son el mismo resultado. Consulte los [estados y ciclos S1–S6](spiral-strategy.md).

## 6. Validar la historia con los referentes

**Qué y por qué.** Pruebe sobre una copia migrada en **Staging**, con restauración
autorizada y servicios externos aislados. Una base nueva sirve para probar runtime,
no para demostrar que se conservaron saldos, documentos o procesos.

**Cómo hacerlo:**

- Antes de probar, acuerde escenarios, roles, valores esperados y tolerancias de conciliación.
- Compruebe saldos, pagos, impuestos, stock, numeraciones y relaciones entre documentos,
  según el alcance. Use muestras anonimizadas solo bajo autorización.
- Pida una verificación independiente y registre diferencias, fallos y comprobaciones omitidas.
- Solicite aceptación funcional y contable; no cierre diferencias sin explicación aceptada.

**Qué consultar:** al responsable de datos, entrega y cobertura efectiva; a los
referentes funcionales y contables, criterios y diferencias; a seguridad, permisos y accesos.

**Para avanzar:** evidencia histórica y aceptación humana de cada ámbito aplicable.
Use la [lista de validación](validation.md); `runtime_passed` no equivale a `data_validated`
ni a `accepted`.

## 7. Ensayar el corte y presentar la decisión

**Qué y por qué.** Planifique el corte desde el inicio y ensáyelo antes de proponer
producción. Que el sistema funcione en Staging no prueba que pueda recuperarse ante un fallo.

**Cómo hacerlo:**

- Acuerde ventana, congelamiento de cambios y escrituras, responsables y condiciones de parada.
- Con plataforma, documente copias, retención, restauración, reversión y efectos de escrituras posteriores.
- Solicite autorización para el ensayo; registre tiempos, resultados y límites de recuperación.
- Presente evidencias de código, runtime y datos, pendientes y riesgos residuales al propietario.
- Defina seguimiento posterior: alertas, conciliaciones, responsables de incidentes y escalamiento.

**Qué consultar:** a plataforma, si la restauración y recuperación quedaron comprobadas;
a los referentes, si aceptan su ámbito; al propietario, si autoriza el corte o decide posponerlo.

**Para avanzar:** ensayo respaldado y autorización específica de producción.
Ante fallos, copias ausentes o aprobación retirada, deténgase y consulte; no improvise
reparaciones ni reversión. Esta guía no concede permisos de ejecución.

## Cómo dejar el trabajo claro para el siguiente técnico

Mantenga la ficha y las tarjetas en el registro privado, sin duplicar tableros.
Cada entrega debe responder cuatro preguntas:

- **¿Qué se hizo?** Módulo, alcance y último estado respaldado.
- **¿Cómo se comprobó?** Esperado, observado y resultado: aprobado, fallido o no comprobado.
- **¿Qué falta?** Bloqueo, pregunta concreta y rol que debe decidir.
- **¿Qué sigue?** Próxima acción, permiso necesario y condición para avanzar.

Registre los hallazgos con la [plantilla de errores conocidos](known-errors.md).
Si necesita más detalle de organización, consulte la [estrategia en espiral](spiral-strategy.md).
**Primera acción: complete la ficha de entrada y resuelva la primera pregunta pendiente.**

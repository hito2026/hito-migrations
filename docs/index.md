# Introducción

## La idea del proyecto

Migrar Odoo significa **llevar a una nueva versión tanto el sistema que ejecuta el negocio
como la información que ese negocio necesita conservar**. No alcanza con cambiar la
versión de Odoo, apuntar a otra rama de código o conseguir que un módulo se instale.
También deben mantenerse las funciones necesarias, las relaciones entre documentos,
los datos históricos y los controles de acceso.

El esquema de trabajo de Hito toma como referencia **Odoo 17.0 → 19.0 en Odoo.sh**.
La edición, la ruta de actualización y la cobertura del servicio se confirman para cada caso.
La migración se organiza en tres frentes relacionados, pero con resultados distintos:

| Frente | Trabajo que se realiza | Qué debe comprobarse |
| --- | --- | --- |
| Código | Seleccionar versiones compatibles, adaptar módulos propios y resolver reemplazos. | Que el conjunto de módulos instale y funcione en la versión destino. |
| Base de datos | Solicitar a Odoo la actualización de una copia de la base y revisar su cobertura. | Que los datos y sus relaciones se conserven en el entorno actualizado. |
| Negocio y aceptación | Ejecutar escenarios reales acordados con los referentes. | Que los procesos críticos funcionen y las diferencias sean aceptadas por sus responsables. |

**El código y la base pueden avanzar en paralelo; ninguno acredita por sí solo una
migración aceptada.** El encuentro entre ambos se comprueba en un entorno de pruebas,
antes de considerar el paso a producción.

## Qué cambia entre origen y destino

Un proyecto no contiene únicamente el código oficial de Odoo. El **repositorio principal**
reúne la configuración y las referencias a otros repositorios, frecuentemente mediante
**submódulos**. Cada origen de código requiere una decisión propia:

| Origen en 17.0 | Tratamiento previsto para 19.0 |
| --- | --- |
| Odoo y sus componentes oficiales | Utilizar la versión destino admitida por la plataforma y el servicio contratado. |
| OCA | Revisar si existe una rama 19.0 compatible y qué módulos incluye; actualizar las referencias solo después de comprobar dependencias y cobertura. |
| ADHOC y sus forks | Contrastar la versión destino con las personalizaciones del fork e identificar módulos cambiados, reorganizados o reemplazados. |
| Módulos de Hito | Adaptar el código propio, sus dependencias y sus pruebas en las ramas de destino correspondientes. |
| Personalizaciones `custom-cliente` | Revisar las necesidades específicas del cliente y migrar las que continúan dentro del alcance. |
| Repositorio principal | Preparar una rama de migración que integre las referencias compatibles y la configuración del destino. |

**Cambiar de rama no demuestra equivalencia** funcional ni conservación de datos. Un módulo
puede no existir en destino, estar en otro repositorio, haber cambiado de diseño o haber
sido sustituido. Además, deben conservarse o trasladarse las modificaciones propias del fork.

Por eso, primero se identifica lo instalado y utilizado, y luego se decide qué reutilizar,
qué adaptar, qué reemplazar y qué requiere investigación. No se migra todo por defecto.

## Cómo trabajamos

El esquema contempla dos formas de organizar el código destino. La elección depende del
proyecto; no modifica la necesidad de actualizar la base y validar el resultado completo.

### Adaptar el repositorio actual

Se prepara una rama de trabajo sobre la estructura existente y se lleva cada componente
a una referencia compatible con 19.0. Los módulos propios se adaptan y los de terceros
se toman de una versión adecuada cuando existe, preservando las diferencias necesarias.

Odoo.sh puede gestionar la actualización de prueba de la base y el cambio de versión de
su entorno. **Ese servicio no adapta automáticamente el código de OCA, ADHOC, Hito ni las
personalizaciones del cliente.** Si esas referencias siguen en 17.0 o no son compatibles,
la aplicación todavía no está preparada para funcionar en 19.0.

Después se integran código y base actualizada en pruebas, se observan los errores y se
corrigen sus causas. Los cambios de módulos de terceros son un foco de revisión, no una
predicción de que todo fallará ni de que un cambio de rama resolverá todas las diferencias.

### Preparar el repositorio de destino

**Para Equipavic y Smarttract, el enfoque indicado en el esquema es preparar un repositorio
de destino para 19.0 con la arquitectura actual de la localización de Hito**, en lugar de
reproducir sin revisión la organización histórica de repositorios y submódulos.
Esto describe el diseño propuesto, no afirma que su implementación ya esté terminada.

La organización diferencia la localización argentina, los módulos genéricos compartidos,
los repositorios o forks de terceros y las personalizaciones del cliente. Los nombres y
las referencias reales se mantienen en el registro privado de cada proyecto.

El recorrido previsto es:

1. **Preparar el repositorio y la rama de destino.** Definir la estructura, las fuentes
   permitidas y las referencias que integrará el proyecto para 19.0.
2. **Relacionar el inventario de origen con el destino.** Identificar para cada módulo
   si conserva su implementación, se adapta o pasa a una alternativa. Revisar sus
   dependencias y ubicarlo en el repositorio que corresponde a la nueva arquitectura.
3. **Actualizar el código y solicitar la actualización de la base en paralelo.**
   La adaptación técnica y la solicitud al servicio de Odoo son trabajos separados;
   no hace falta esperar a terminar todos los módulos para iniciar la solicitud autorizada.
4. **Integrar la copia actualizada con el código destino.** Restaurar o incorporar la
   entrega únicamente en el entorno aislado autorizado, con las condiciones de copia
   y recuperación acordadas. No se reemplaza la base de producción en este paso.
5. **Resolver diferencias y verificar.** Registrar errores, corregir código o preparar
   transformaciones de datos cuando sean necesarias y estén aprobadas; repetir las pruebas
   hasta reunir evidencia suficiente para la aceptación.

No es un traslado mecánico de carpetas: el destino debe conservar las capacidades y la
historia que el usuario necesita, aunque cambie la organización del código.

### Qué implica reemplazar un módulo

El esquema utiliza como ejemplo un módulo de pagos `payment_group` procedente de un fork
de ADHOC y un posible destino en el repositorio `account-payment-pro`. El ejemplo ilustra
una **decisión de correspondencia que debe investigarse**, no una equivalencia ya probada
ni una afirmación de que esos sean los módulos efectivos de todos los proyectos.

Antes de adoptar una alternativa hay que comprobar las funciones que cubre, sus dependencias,
las personalizaciones y el tratamiento de los registros existentes. Cambiar un submódulo de
Git no convierte los datos: si cambian modelos, campos o relaciones, debe definirse y probarse
su transición. Una brecha funcional, contable o histórica requiere una decisión explícita.

## La actualización de la base de datos

El servicio oficial [Odoo Upgrade](https://upgrade.odoo.com/) recibe la solicitud de
actualización de una base de origen y entrega, cuando el proceso resulta satisfactorio,
una base para la versión destino. La cobertura de datos estándar y de personalizaciones
se confirma para el caso; no se presume por haber recibido una entrega.

En Odoo.sh se utiliza el flujo de actualización de prueba sobre una rama **Staging**;
el formulario del servicio también distingue solicitudes de prueba y de producción.
El [Procedimiento](procedure.md#6-en-paralelo-solicitar-la-actualizacion-de-la-base)
explica dónde iniciar la solicitud. El envío de datos, la restauración y las pruebas
requieren sus permisos correspondientes.

**Una base actualizada no acredita aceptación de los datos ni compatibilidad del código
personalizado.** Debe integrarse con los módulos de destino y comprobarse con escenarios,
valores esperados y criterios acordados. El origen se preserva: una restauración de prueba
no es una autorización para modificarlo ni para ejecutar un corte a producción.

## Validar y avanzar en espiral

El trabajo se realiza en **espiral**: inventariar y decidir, adaptar un conjunto acotado,
probar, analizar diferencias y volver a corregir cuando sea necesario. Las dependencias
orientan el orden: primero los componentes base y después los módulos que los utilizan.
Un hallazgo puede obligar a revisar una decisión anterior; no se fuerza el avance por haber
terminado una lista de tareas.

La verificación separa tres niveles:

- **Técnico:** instalación, carga, dependencias, permisos y resultados de pruebas de código.
- **Funcional:** operaciones del negocio, informes e integraciones con resultados esperados.
- **Histórico:** saldos, documentos, numeraciones, estados y relaciones de la copia migrada,
  según los dominios incluidos en el alcance.

Una base nueva puede servir para probar código, pero no demuestra la conservación de la
historia. A su vez, una base convertida no demuestra que sus procesos funcionen correctamente.
Las diferencias y las comprobaciones omitidas se registran, no se ocultan con un estado de éxito.

Solo después se presenta la aceptación a los referentes y se prepara o completa el ensayo
de corte y recuperación. **La producción exige autorización específica**, evidencias revisadas,
responsables, condiciones de parada y un plan de recuperación acordado.

## Qué aporta el agente

El agente ejecutado desde Gentle Shell ayuda a organizar y desarrollar el trabajo dentro
de los permisos del caso. El esquema le asigna estas funciones:

| Función | Aporte esperado |
| --- | --- |
| Analizar la estrategia | Identificar qué módulos deben migrarse realmente, cuáles ya tienen una versión compatible y cuáles necesitan análisis por reemplazo. |
| Adaptar técnicamente | Trabajar sobre Python, XML, vistas, manifiestos y dependencias de los módulos autorizados. |
| Registrar el avance | Mantener trazabilidad de módulos migrados, pendientes y que requieren revisión, con bloqueos y dependencias visibles. |
| Preparar pruebas técnicas | Proponer y, con medios y permisos disponibles, ejecutar comprobaciones de instalación y comportamiento técnico; registrar resultados reales. |
| Apoyar pruebas funcionales | Ayudar a definir escenarios y resultados esperados para que los responsables comprueben los procesos. |

**El apoyo a pruebas funcionales figura como capacidad no probada en el esquema recibido.**
No debe presentarse como una función ya validada ni como una aceptación automática.
Preparar una prueba tampoco equivale a haberla ejecutado o superado.

El agente debe seguir `migration-spiral-strategy-spec.md`, informar lo que no sabe y
pedir decisiones cuando falte una fuente, un permiso o una definición. **No sustituye la aceptación humana**
ni puede concederse acceso, ampliar el alcance o autorizar producción por su cuenta.
Los conteos de módulos se respaldan con el inventario y las comprobaciones: no se inventan
cantidades ni se deduce progreso de la mera ausencia de errores informados.

## Responsabilidades y decisiones

| Responsable | Decisiones y entregas |
| --- | --- |
| Usuario migrador y coordinación | Aportar contexto y fuentes autorizadas, organizar dependencias, mantener el registro y resolver o elevar bloqueos. |
| Equipo técnico y agente | Proponer e implementar cambios acotados, preparar pruebas y entregar resultados, fallos y límites de lo comprobado. |
| Servicio de actualización de Odoo | Procesar la solicitud y entregar la base actualizada dentro de la cobertura confirmada. |
| Referentes funcionales y contables | Definir criterios, revisar escenarios y diferencias y aceptar o rechazar los resultados de su ámbito. |
| Propietario y responsables del entorno | Autorizar acciones sensibles, restauraciones, ensayos y el eventual corte a producción. |

<div class="draft-notice" role="note" markdown>
**Borrador no verificado.** Esta explicación formaliza el diseño de trabajo aportado;
no acredita resultados de Equipavic, Smarttract ni de otra migración. Los inventarios,
repositorios internos, accesos y evidencias se conservan en registros privados autorizados.
</div>

## Cómo usar esta guía

1. Use esta Introducción para comprender qué se migra y cómo se relacionan código, datos y aceptación.
2. Siga el [Procedimiento](procedure.md) para entrar al proyecto, aportar los datos y utilizar
   los mensajes de inicio o autorización en el paso correspondiente.
3. Consulte [Gentle Shell](gentle-shell.md) para preparar el acceso o recuperar una sesión.

**Un módulo que instala no demuestra que sus datos se hayan migrado bien.** El cierre
requiere evidencia de código, funcionamiento e historia, más una decisión humana.

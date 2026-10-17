# Instrucciones del usuario

Empiece pidiendo un diagnóstico, no una ejecución completa. Copie los mensajes siguientes
y reemplace los campos entre `<…>` **en su registro privado autorizado**, nunca en este sitio.
No incluya credenciales. Una instrucción habilita solo la etapa y las acciones que indique.

## Usar el entorno de trabajo

Si trabaja en el servidor del equipo, consulte el [manual de uso de Gentle Shell](gentle-shell.md):
ejecute los comandos de acceso, abra el caso y copie el mensaje para empezar la migración.
Después utilice las instrucciones de esta página para autorizar cada etapa.

## Para comenzar

Reúna versiones y edición, fuentes autorizadas, procesos críticos y una persona que pueda
decidir por cada área. Si no conoce un dato, escriba «por confirmar».

```text
Prepare el diagnóstico y el plan de migración, sin ejecutar cambios.
Origen y destino: <versiones y compilaciones exactas; edición>.
Entorno previsto: <plataforma; Development y Staging disponibles>.
Fuentes permitidas: <repositorios, documentación e inventario autorizados>.
Procesos que debemos conservar: <procesos, informes e integraciones críticos>.
Fuera de alcance: <exclusiones>.
Responsables: <coordinación; técnico; datos; funcional/contable; propietario>.
Restricciones: <accesos, acciones permitidas e indisponibilidad tolerable>.
Entregue inventario, dependencias, propuesta por módulo, dudas y plan por etapas.
No modifique archivos, no haga commits ni publique. No restaure bases ni opere en producción.
```

**Qué recibirá:** una propuesta revisable, no una migración iniciada.
Se le consultará por accesos, fuentes faltantes, uso real, prioridades, licencias,
reemplazos, datos históricos y criterios de aceptación.

## Para adaptar código

Revise el plan antes de autorizar un grupo de módulos. Confirme el destino de cada módulo
y quién acepta los cambios funcionales. Crear ramas o integrar también necesita permiso explícito.

```text
Apruebo el plan <referencia privada> solo para adaptar <grupo de módulos>.
Puede modificar <archivos autorizados> en <espacio de trabajo autorizado>.
Use <dependencias y decisiones aprobadas>; conserve <funciones y datos requeridos>.
Compruebe <pruebas locales y resultados esperados> y entregue el diff y sus resultados.
No amplíe el alcance, no publique, no opere sobre bases ni haga cambios en producción.
Si falta una decisión o aparece otra dependencia, informe el bloqueo antes de continuar.
```

## Para probar el funcionamiento

Confirme el grafo completo de dependencias y cómo se aislarán las integraciones.
Autorice las acciones concretas sobre el entorno de prueba, no cualquier operación en él.

```text
Autorizo <acciones de instalación/prueba> de <grupo y dependencias aprobados>
en <Development aislado>, durante <vigencia>.
El aislamiento aprobado es <controles de correo, bancos, fiscal y otras integraciones>.
Pruebe <escenarios, roles, resultados esperados>.
Registre lo esperado, lo observado, fallos y comprobaciones omitidas.
No use datos productivos ni contacte servicios externos; no pase a Staging o producción.
```

**Qué recibirá:** evidencia del funcionamiento del código. Todavía no acredita la historia.

## Para validar los datos

Solicite primero al proveedor la cobertura y las exclusiones: estándar, personalizaciones,
reemplazos y datos sin conversión confirmada. Acordará con sus referentes pagos, cheques,
retenciones, IVA, numeración, stock y demás dominios aplicables; no deje que el técnico
invente el criterio contable o fiscal.

```text
La entrega actualizada es <referencia privada y cobertura confirmada>.
El responsable de datos autoriza <restauración y pruebas concretas> en <Staging aislado>,
bajo <condiciones de copia, recuperación, acceso y vigencia aprobadas>.
Valide <escenarios históricos, valores esperados y tolerancias acordadas>.
Los referentes <roles> revisarán las diferencias y registrarán aceptación o rechazo.
No modifique el origen ni opere en producción. Deténgase ante diferencias fuera de criterio.
```

Si falta la entrega, el permiso o el criterio, mantenga esta etapa pendiente.

## Para ensayar el corte

La recuperación debe tener responsable y condiciones verificables. Un ensayo no autoriza producción.

```text
Autorizo el ensayo del plan de corte <referencia> en <entorno aislado>.
Alcance: <acciones aprobadas, responsables, ventana y congelamiento de escrituras>.
Compruebe <copias, restauración, tiempos, reversión y efectos externos>.
Deténgase si <condiciones acordadas> y escale a <rol decisor>.
Entregue resultados, límites de recuperación y pendientes. No ejecute el corte real.
```

## Para decidir producción

Revise el informe final con los referentes funcionales y contables. Elija **autorizar o
posponer**; no deje ambas opciones en el mensaje y no autorice con pruebas críticas pendientes.

```text
Decisión del propietario: <autorizar el corte / posponerlo> según el plan <referencia>.
Aceptaciones revisadas: <funcional, contable y seguridad, según alcance>.
Evidencias revisadas: <código, funcionamiento, historia y ensayo de recuperación>.
Riesgos residuales aceptados: <lista; sin ocultar fallos ni omisiones>.
Si se autoriza: únicamente <equipo y acciones> en <ventana y entorno aprobados>,
con parada/reversión según <plan> y seguimiento a cargo de <roles>.
Si se pospone: no ejecute; resuelva <pendientes> y solicite una nueva decisión.
```

## Cómo responder una consulta o un bloqueo

Pida siempre **qué falta, qué opciones hay, qué cambia con cada una y quién decide**.
Responda con la opción elegida, su alcance y sus condiciones. Si no tiene la evidencia
o autoridad necesaria, mantenga la tarea bloqueada; no dé una aprobación genérica.

El equipo debe poder continuar desde esa respuesta sin adivinar. Consulte el
[Procedimiento](procedure.md) para ubicar cada decisión en su etapa.

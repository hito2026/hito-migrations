# Procedimiento

Siete pasos para que el usuario migrador entre al proyecto y trabaje con el agente.
Se parte de un caso **ya creado y asignado**, con acceso al servidor y Gentle Shell instalado.

## 1. Conectarse al servidor

Desde la terminal de su computadora:

```sh
ssh servidor-migraciones
```

## 2. Entrar al proyecto

En el servidor:

```sh
cd "/srv/migraciones/cases/MIG-Nombre del proyecto"
```

Reemplace `MIG-Nombre del proyecto` por la carpeta real del caso.
Las comillas permiten espacios en la ruta. Si no existe, consulte al responsable;
no cree otro caso para continuar.

## 3. Abrir Gentle Shell

Desde la carpeta del proyecto:

```sh
gentle-shell
```

Espere a que aparezca la interfaz. Si ya hay una sesión activa del mismo caso,
**no abra otro coordinador**: [retome la sesión existente](gentle-shell.md#7-retomar-el-trabajo).
Si lo coordina otra persona, acuerde el relevo.

## 4. Iniciar o continuar

En el chat de Gentle Shell:

- **Si inicia**, entregue los datos y el mensaje del paso 5.
- **Si continúa**, use este mensaje y siga con los pasos 6 y 7 según lo pendiente:

```text
Continúe la migración del proyecto actual desde el último registro de trabajo.
Revise lo realizado, las comprobaciones, los bloqueos y las decisiones pendientes.
Proponga el próximo paso sin repetir tareas ya verificadas y espere su autorización.
```

## 5. Si inicia: informar repositorio y accesos

Reúna los datos del caso y complete este mensaje en el **canal privado del caso**,
no en el sitio público. Si no conoce un dato, escriba «por confirmar».
Empiece con un diagnóstico: este mensaje no autoriza la ejecución completa.

```text
Inicie el diagnóstico de la migración del proyecto actual.
Repositorio principal: <URL del repositorio y ramas de origen y destino>.
SSH de origen: <alias o usuario@servidor y puerto, si corresponde>.
SSH de destino: <alias o usuario@servidor y puerto, si corresponde>.

Origen y destino: <versiones y compilaciones exactas; edición>.
Entorno previsto: <plataforma; Development y Staging disponibles>.
Fuentes permitidas: <repositorios, documentación e inventario autorizados>.
Procesos que debemos conservar: <procesos, informes e integraciones críticos>.
Fuera de alcance: <exclusiones>.
Responsables: <coordinación; técnico; datos; funcional/contable; propietario>.
Restricciones: <accesos, acciones permitidas e indisponibilidad tolerable>.

Siga migration-spiral-strategy-spec.md.
Entregue inventario, dependencias, propuesta por módulo, dudas y plan por etapas.
No modifique archivos, no haga commits ni publique. No restaure bases ni opere en producción.
Si falta información o autorización, pregunte antes de avanzar.
```

**No pegue contraseñas**, claves privadas ni tokens en el chat. Configure la autenticación
por el canal seguro acordado. Informar una conexión no autoriza su uso ni cambios en datos.

**Qué recibirá:** una propuesta revisable. El agente consultará por accesos, fuentes
faltantes, uso real, prioridades, licencias, reemplazos, datos históricos y aceptación.

## 6. En paralelo: solicitar la actualización de la base

Mientras avanza el trabajo de código, el usuario migrador solicita la actualización
**de prueba** de la base mediante [Odoo Upgrade](https://upgrade.odoo.com/).

Para Odoo.sh, use la rama **Staging**, pestaña **UPGRADE**, versión destino acordada y
**Test Upgrade**. Si utiliza el formulario del servicio, seleccione **Testing**.
Realice la solicitud solo con autorización para tratar la base y usar el entorno elegido.

**No seleccione Production** ni inicie el corte a producción en este paso.
Informe al agente la solicitud, su estado y los errores. Si ya hay una solicitud en curso,
revise esa solicitud antes de crear otra. Recibir una base actualizada
**no acredita aceptación de los datos**: todavía deben verificarse según el plan.

## 7. Seguir al agente y el plan en espiral

**Siga las indicaciones del agente**, que guía la migración utilizando
`migration-spiral-strategy-spec.md`, disponible en el kit del servidor.
El manual identifica su ubicación como
`/srv/migraciones/kit/docs/migration-spiral-strategy-spec.md`.
Si el agente no puede leerlo, debe informar el bloqueo en lugar de improvisar el plan.

Responda sus consultas, revise las comprobaciones y autorice las acciones que correspondan.
El acceso **no autoriza operaciones sobre bases ni producción**: se requieren los
**permisos correspondientes** para cada acción.

Use los mensajes siguientes **solo cuando llegue a esa etapa**. Reemplace los campos
entre `<…>` en el registro privado autorizado. Cada mensaje habilita únicamente las
acciones y el alcance que indique; no es una aprobación general de la migración.

### Para adaptar código

Revise el plan y confirme el destino de cada módulo y quién acepta los cambios funcionales.
Crear ramas o integrar también requiere permiso explícito.

```text
Apruebo el plan <referencia privada> solo para adaptar <grupo de módulos>.
Puede modificar <archivos autorizados> en <espacio de trabajo autorizado>.
Use <dependencias y decisiones aprobadas>; conserve <funciones y datos requeridos>.
Compruebe <pruebas locales y resultados esperados> y entregue el diff y sus resultados.
No amplíe el alcance, no publique, no opere sobre bases ni haga cambios en producción.
Si falta una decisión o aparece otra dependencia, informe el bloqueo antes de continuar.
```

### Para probar el funcionamiento

Confirme las dependencias y el aislamiento de las integraciones. Autorice acciones
concretas en el entorno de prueba, no cualquier operación en él.

```text
Autorizo <acciones de instalación/prueba> de <grupo y dependencias aprobados>
en <Development aislado>, durante <vigencia>.
El aislamiento aprobado es <controles de correo, bancos, fiscal y otras integraciones>.
Pruebe <escenarios, roles, resultados esperados>.
Registre lo esperado, lo observado, fallos y comprobaciones omitidas.
No use datos productivos ni contacte servicios externos; no pase a Staging o producción.
```

**Qué recibirá:** evidencia del funcionamiento del código, no de la historia.

### Para validar los datos

Espere la entrega actualizada del paso 6 y confirme con el proveedor la cobertura y las
exclusiones: estándar, personalizaciones, reemplazos y datos sin conversión confirmada.
Acuerde con los referentes los pagos, cheques, retenciones, IVA, numeración, stock y
otros dominios aplicables; el agente no debe inventar criterios contables o fiscales.

```text
La entrega actualizada es <referencia privada y cobertura confirmada>.
El responsable de datos autoriza <restauración y pruebas concretas> en <Staging aislado>,
bajo <condiciones de copia, recuperación, acceso y vigencia aprobadas>.
Valide <escenarios históricos, valores esperados y tolerancias acordadas>.
Los referentes <roles> revisarán las diferencias y registrarán aceptación o rechazo.
No modifique el origen ni opere en producción. Deténgase ante diferencias fuera de criterio.
```

Sin entrega, permiso o criterio, mantenga esta etapa pendiente.

### Para ensayar el corte

Defina responsables y condiciones verificables de recuperación. Un ensayo no autoriza producción.

```text
Autorizo el ensayo del plan de corte <referencia> en <entorno aislado>.
Alcance: <acciones aprobadas, responsables, ventana y congelamiento de escrituras>.
Compruebe <copias, restauración, tiempos, reversión y efectos externos>.
Deténgase si <condiciones acordadas> y escale a <rol decisor>.
Entregue resultados, límites de recuperación y pendientes. No ejecute el corte real.
```

### Para decidir producción

Revise el informe con los referentes funcionales y contables. Elija **autorizar o posponer**;
no deje ambas opciones en el mensaje ni autorice con pruebas críticas pendientes.

```text
Decisión del propietario: <autorizar el corte / posponerlo> según el plan <referencia>.
Aceptaciones revisadas: <funcional, contable y seguridad, según alcance>.
Evidencias revisadas: <código, funcionamiento, historia y ensayo de recuperación>.
Riesgos residuales aceptados: <lista; sin ocultar fallos ni omisiones>.
Si se autoriza: únicamente <equipo y acciones> en <ventana y entorno aprobados>,
con parada/reversión según <plan> y seguimiento a cargo de <roles>.
Si se pospone: no ejecute; resuelva <pendientes> y solicite una nueva decisión.
```

### Cómo responder una consulta o un bloqueo

Pida **qué falta, qué opciones hay, qué cambia con cada una y quién decide**.
Responda con la opción elegida, su alcance y sus condiciones. Sin evidencia o autoridad,
mantenga la tarea bloqueada; no dé una aprobación genérica.

Como referencia pública, consulte el [Plan técnico en espiral](spiral-strategy.md).
Para preparación o problemas de acceso, use el [manual de Gentle Shell](gentle-shell.md).

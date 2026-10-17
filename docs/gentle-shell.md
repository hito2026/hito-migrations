# Usar Gentle Shell para una migración

Siga los pasos en orden. Reemplace `ssh.example.com`, `devN` y `MIG-CLIENTE-001`
por el servidor, usuario y caso asignados por el administrador.

## 1. Preparar el acceso — una sola vez

**En su computadora:** tenga instalados OpenSSH y `cloudflared`. En Mac con Homebrew:

```sh
brew install cloudflared
```

Si no tiene una clave SSH, créela. No sobrescriba una existente:

```sh
ssh-keygen -t ed25519
```

Muestre la clave pública y envíesela al administrador:

```sh
cat ~/.ssh/id_ed25519.pub
```

Pídale que habilite su usuario, esa clave pública y su email en Cloudflare Access.
**No copie claves privadas** ni tokens al chat.

Abra `~/.ssh/config`:

```sh
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/config
```

Agregue este bloque, reemplazando servidor y usuario. En nano, guarde con
**Ctrl+O**, **Enter** y cierre con **Ctrl+X**:

```sshconfig
Host servidor-migraciones
  HostName ssh.example.com
  User devN
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
  ProxyCommand cloudflared access ssh --hostname %h
  ServerAliveInterval 30
```

```sh
chmod 600 ~/.ssh/config
```

## 2. Entrar al servidor

**En su computadora:**

```sh
cloudflared access login https://ssh.example.com
```

Complete el login en el navegador. Luego:

```sh
ssh servidor-migraciones
```

La primera vez, confirme la huella SSH con el administrador antes de aceptarla.
**Ya en el servidor**, compruebe que aparece su usuario:

```sh
whoami
```

## 3. Abrir su sesión de trabajo

**En el servidor:**

```sh
tmux new-session -A -s trabajo
```

Si recupera una sesión con Gentle Shell ya abierto, continúe allí: no abra otro
coordinador del mismo caso. Si aparece una terminal vacía, siga al paso 4.

## 4. Abrir el caso

**En la terminal del servidor**, elija un identificador con cliente en mayúsculas
alfanuméricas y tres dígitos. Reemplace el ejemplo:

```sh
CASO=MIG-CLIENTE-001
mig-case list
```

**Solo si es un caso nuevo autorizado:**

```sh
mig-case new "$CASO"
```

**Para un caso nuevo o existente:**

```sh
mig-case status "$CASO"
mig-case claim "$CASO"
```

Si lo coordina otra persona, deténgase y acuerde el relevo. No borre su lock.
**Solo si el reclamo terminó correctamente**, continúe:

```sh
cd "/srv/migraciones/cases/$CASO"
gentle-shell
```

Espere a que termine la preparación inicial y aparezca la interfaz.

## 5. Conectar el modelo — primera vez

**Dentro de Gentle Shell**, escriba:

```text
/login
```

Elija cuenta o clave API, seleccione su proveedor y complete la autenticación.
Introduzca códigos y claves solo en ese flujo, no en el chat del agente.
Si ya tiene un proveedor y modelo disponibles, omita este paso.

## 6. Empezar la migración

**En el chat de Gentle Shell**, pegue el mensaje siguiente. Complete los campos
entre `<…>` con los datos del caso; use «por confirmar» si falta alguno:

```text
Prepare el diagnóstico y el plan de esta migración.

Origen: <versión exacta de Odoo y edición>.
Destino: <versión exacta de Odoo y edición>.
Repositorios autorizados: <URLs y ramas de origen y destino>.
Entornos autorizados: <proyecto Odoo.sh; Development y Staging disponibles>.
Procesos que deben conservarse: <flujos, informes e integraciones críticos>.
Responsables: <técnico; funcional/contable; datos; persona que autoriza>.
Fuera de alcance: <exclusiones>.

Lea runbook.md, case-intake.yml, module-board.yml y
/srv/migraciones/kit/docs/migration-spiral-strategy-spec.md.
Use únicamente las fuentes autorizadas, en modo lectura.
Complete los datos confirmados en case-intake.yml y registre el diagnóstico,
las preguntas y el próximo paso en runbook.md.
Entregue inventario, dependencias, propuesta por módulo y plan por etapas.
No modifique repositorios ni bases, no haga commits ni push y no opere en producción.
Si falta acceso o una decisión, indique exactamente qué necesito resolver.
```

Responda las preguntas del agente y revise el plan. Para autorizar la siguiente
etapa, copie el mensaje correspondiente de [Instrucciones del usuario](user-instructions.md).
Siga el orden del [Procedimiento](procedure.md); no autorice toda la migración de una vez.

## 7. Retomar el trabajo

Para salir sin cerrar la sesión: **Ctrl+b**, suelte y presione **d**.

Para volver, **desde su computadora**:

```sh
ssh servidor-migraciones
```

**En el servidor:**

```sh
tmux attach -t trabajo
```

Si Gentle Shell sigue abierto, pegue:

```text
Lea runbook.md y module-board.yml. Resuma dónde quedamos, los bloqueos y el
próximo paso autorizado. No ejecute acciones nuevas hasta confirmar el alcance.
```

## 8. Entregar el caso

**En Gentle Shell**, antes de salir:

```text
Actualice runbook.md y module-board.yml con lo realizado, las pruebas,
los fallos, los pendientes y el próximo paso. No marque como terminado
lo que no se comprobó. Indique si quedan trabajadores o procesos activos.
```

Resuelva los procesos activos antes de entregar la coordinación. Abra otra ventana
con **Ctrl+b**, suelte y presione **c**. **En esa terminal del servidor:**

```sh
mig-case release MIG-CLIENTE-001
mig-case status MIG-CLIENTE-001
```

Reemplace el caso; el estado debe quedar `free`. Acuerde quién continúa.

## Si no puede avanzar

| Mensaje o problema | Acción |
| --- | --- |
| Vence la conexión antes de entrar | En su computadora, ejecute `cloudflared access login https://ssh.example.com` y complete el navegador |
| `Permission denied (publickey)` | Pida al administrador verificar su usuario y el alta de su `.pub` |
| Cambió la huella SSH | Deténgase y confirme la nueva huella con el administrador |
| `No models available` | En Gentle Shell, ejecute `/login` |
| Otro usuario coordina el caso | Acuerde el relevo antes de reclamarlo |
| Falta acceso a GitHub u Odoo.sh | Solicite acceso para su propia cuenta; no use credenciales ajenas |
| Falta `mig-case`, falla el editor o aparece una actualización | Consulte al administrador; no instale ni actualice herramientas compartidas |

# Usar Gentle Shell para una migración

Siga los pasos en orden. Reemplace `ssh.example.com`, `devN` y `MIG-CLIENTE-001`
por el servidor, usuario y caso asignados por el administrador.

## 1. Preparar el acceso — una sola vez

**En su computadora**, siga únicamente su sistema: [Windows](#windows),
[Linux](#linux) o [macOS](#macos). Pida al administrador su usuario, servidor,
huella SSH esperada y alta de su email en Cloudflare Access.

### Windows

Abra **PowerShell**, no CMD ni WSL. Compruebe el cliente SSH:

```powershell
ssh -V
```

Solo si `ssh` no existe, abra PowerShell **como administrador**, ejecute lo siguiente
y después vuelva a una ventana normal. No instale OpenSSH Server:

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

En PowerShell **normal**, instale `cloudflared` para su usuario
(Windows de 64 bits, x86-64):

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\cloudflared", "$HOME\.ssh" | Out-Null
Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile "$HOME\cloudflared\cloudflared.exe" -ErrorAction Stop
& "$HOME\cloudflared\cloudflared.exe" --version
```

Si usa otro tipo de Windows, solicite al administrador el cliente compatible de
[descargas oficiales](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/downloads/#windows).

Cree una clave solo si no tiene la indicada; muestre la parte pública:

```powershell
if (-not (Test-Path "$HOME\.ssh\id_ed25519")) {
    ssh-keygen -t ed25519 -f "$HOME\.ssh\id_ed25519"
}
Get-Content "$HOME\.ssh\id_ed25519.pub"
```

Envíe **solo esa clave pública** al administrador y espere el alta. Abra la configuración:

```powershell
if (-not (Test-Path "$HOME\.ssh\config")) {
    New-Item -ItemType File -Path "$HOME\.ssh\config" | Out-Null
}
notepad "$HOME\.ssh\config"
```

Agregue el bloque de [Configurar SSH](#configurar-ssh). Guarde con **Ctrl+S** y cierre.
El archivo debe llamarse `config`, **no `config.txt`**.

### Linux

Abra una **terminal**. Instale las herramientas de su distribución; elija un solo bloque.

**Ubuntu / Debian:**

```sh
sudo apt-get update
sudo apt-get install openssh-client curl nano
```

**Fedora:**

```sh
sudo dnf install openssh-clients curl nano
```

En otras distribuciones, instale esos clientes con su gestor de paquetes.
Para instalar `cloudflared` en su usuario, consulte la arquitectura:

```sh
uname -m
mkdir -p ~/.local/bin
```

**Si muestra `x86_64`:**

```sh
curl -fL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o ~/.local/bin/cloudflared
```

**Si muestra `aarch64` o `arm64`:**

```sh
curl -fL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -o ~/.local/bin/cloudflared
```

Para otra arquitectura, use la [descarga oficial correspondiente](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/downloads/#linux).
**Solo si la descarga terminó correctamente**, continúe:

```sh
chmod 755 ~/.local/bin/cloudflared
~/.local/bin/cloudflared --version
mkdir -p ~/.ssh
chmod 700 ~/.ssh
if [ ! -f ~/.ssh/id_ed25519 ]; then
    ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519
fi
cat ~/.ssh/id_ed25519.pub
```

Envíe **solo esa clave pública** al administrador y espere el alta. Abra la configuración:

```sh
nano ~/.ssh/config
```

Agregue el bloque de [Configurar SSH](#configurar-ssh). Guarde con **Ctrl+O**, **Enter**
y cierre con **Ctrl+X**. Luego:

```sh
chmod 600 ~/.ssh/config
```

### macOS

Abra **Terminal**. Si no tiene Homebrew, instálelo desde [brew.sh](https://brew.sh/).
Después ejecute:

```sh
brew install cloudflared
ssh -V
cloudflared --version
mkdir -p ~/.ssh
chmod 700 ~/.ssh
if [ ! -f ~/.ssh/id_ed25519 ]; then
    ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519
fi
cat ~/.ssh/id_ed25519.pub
```

Envíe **solo esa clave pública** al administrador y espere el alta. Abra la configuración:

```sh
nano ~/.ssh/config
```

Agregue el bloque de [Configurar SSH](#configurar-ssh). Guarde con **Ctrl+O**, **Enter**
y cierre con **Ctrl+X**. Luego:

```sh
chmod 600 ~/.ssh/config
```

### Configurar SSH

Agregue este bloque a la configuración abierta. Reemplace servidor y usuario Linux
por los asignados. Cambie también `/RUTA/CLOUDFLARED` según la tabla:

```sshconfig
Host servidor-migraciones
  HostName ssh.example.com
  User devN
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
  ProxyCommand "/RUTA/CLOUDFLARED" access ssh --hostname %h
  ServerAliveInterval 30
```

| Sistema | Qué poner entre las comillas de `ProxyCommand` |
| --- | --- |
| Windows | `C:/Users/SU_USUARIO/cloudflared/cloudflared.exe`; reemplace `SU_USUARIO` por su usuario local de Windows, no por `devN` |
| Linux | La ruta completa de su ejecutable; ejecute `realpath ~/.local/bin/cloudflared` y copie el resultado |
| macOS | Ejecute `command -v cloudflared` y copie el resultado, por ejemplo `/opt/homebrew/bin/cloudflared` |

Conserve las comillas si la ruta contiene espacios. **No copie claves privadas** ni tokens al chat.

## 2. Entrar al servidor

**En su computadora**, reemplace el hostname y ejecute el bloque de su sistema.

**Windows — PowerShell:**

```powershell
& "$HOME\cloudflared\cloudflared.exe" access login https://ssh.example.com
```

**Linux — terminal:**

```sh
~/.local/bin/cloudflared access login https://ssh.example.com
```

**macOS — Terminal:**

```sh
cloudflared access login https://ssh.example.com
```

Complete el login en el navegador. Luego, en **cualquiera de los tres sistemas**:

```sh
ssh servidor-migraciones
```

La primera vez, confirme la huella SSH con el administrador antes de aceptarla.
**A partir de aquí, todos ejecutan los mismos comandos de Linux en el servidor**,
aunque su computadora use Windows o macOS. Compruebe que aparece su usuario:

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
| Vence la conexión antes de entrar | Repita el login de su sistema en el paso 2 y complete el navegador |
| `Permission denied (publickey)` | Pida al administrador verificar su usuario y el alta de su `.pub` |
| Cambió la huella SSH | Deténgase y confirme la nueva huella con el administrador |
| `No models available` | En Gentle Shell, ejecute `/login` |
| Otro usuario coordina el caso | Acuerde el relevo antes de reclamarlo |
| Falta acceso a GitHub u Odoo.sh | Solicite acceso para su propia cuenta; no use credenciales ajenas |
| Falta `mig-case`, falla el editor o aparece una actualización | Consulte al administrador; no instale ni actualice herramientas compartidas |

# Usar Gentle Shell para una migración

Siga los pasos en orden. Reemplace `ssh.example.com`, `devN` y `MIG-CLIENTE-001`
por el servidor, usuario y caso asignados por el administrador.

Para seguir un caso completo, con verificaciones y un prompt de asistencia en cada
paso, vaya al [ejemplo guiado de inicio](#ejemplo-guiado-de-inicio).
Para continuar un caso existente sin duplicar agentes, use el
[ejemplo guiado para retomar un caso](#ejemplo-guiado-para-retomar-un-caso).

## 1. Preparar el acceso — una sola vez

**En su computadora**, siga únicamente su sistema: [Windows](#windows),
[Linux](#linux) o [macOS](#macos). Pida al administrador su usuario, servidor,
huella SSH esperada y alta de su email en Cloudflare Access.

### Windows

Para hacerlo con una IA, despliegue y copie el siguiente prompt. Para hacerlo manualmente,
continúe con los comandos debajo.

<details markdown>
<summary>Prompt para configurar el acceso con una IA — Windows</summary>

```text
Ayúdeme a configurar el acceso a PC-ALE desde Windows usando PowerShell y OpenSSH nativo, sin WSL.

Antes de empezar, pídame el hostname, mi usuario Linux asignado y la huella SSH
esperada; confirme que el administrador habilitó mi cuenta y mi email en Access.
Trabaje solo en mi computadora. Pida autorización para las rutas concretas y
antes de instalar herramientas o editar configuración; conserve una copia del
archivo SSH de configuración existente y agregue el alias sin sobrescribir otros accesos.
Compruebe mi versión y arquitectura de Windows, OpenSSH Client y cloudflared.
Si falta SSH, instale solo OpenSSH Client, no OpenSSH Server ni reglas de firewall.
Use descargas oficiales de cloudflared compatibles con mi equipo.
Reutilice mi clave pública autorizada o guíeme para crear una sin sobrescribir
claves existentes. No lea ni copie el contenido de ninguna clave privada.
Solo la clave pública .pub se entrega al administrador; espere que confirme su alta.
Configure servidor-migraciones en mi archivo .ssh/config, sin crear config.txt,
con mi usuario, mi clave y la ruta absoluta entre comillas de cloudflared.exe.
Guíeme para completar Cloudflare Access en el navegador fuera del chat.
No capture ni reproduzca tokens, códigos ni claves API; no me pida pegarlos aquí.
Compruebe ssh servidor-migraciones, whoami y gentle-shell --version con mi cuenta.
No modifique el servidor, no use sudo remoto, no toque bases ni inicie una migración.
Si algo falla, muestre el error sin secretos y el próximo paso; no desactive Access
ni la comprobación de la huella. Termine con los comandos para entrar y retomar tmux.
```

</details>

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

Para hacerlo con una IA, despliegue y copie el siguiente prompt. Para hacerlo manualmente,
continúe con los comandos debajo.

<details markdown>
<summary>Prompt para configurar el acceso con una IA — Linux</summary>

```text
Ayúdeme a configurar el acceso a PC-ALE desde Linux usando mi terminal local.

Antes de empezar, pídame el hostname, mi usuario Linux asignado y la huella SSH
esperada; confirme que el administrador habilitó mi cuenta y mi email en Access.
Trabaje solo en mi computadora. Pida autorización para las rutas concretas y
antes de instalar herramientas o editar configuración; conserve una copia del
archivo SSH de configuración existente y agregue el alias sin sobrescribir otros accesos.
Detecte mi distribución y arquitectura antes de proponer comandos.
Compruebe OpenSSH Client y curl. Instale solo lo que falte con el gestor apropiado
y cloudflared desde fuentes oficiales, con binario compatible x86-64 o ARM64.
Prefiera cloudflared en ~/.local/bin; no suponga que esa ruta está en mi PATH.
Reutilice mi clave pública autorizada o guíeme para crear una sin sobrescribir
claves existentes. No lea ni copie el contenido de ninguna clave privada.
Solo la clave pública .pub se entrega al administrador; espere que confirme su alta.
Configure servidor-migraciones en ~/.ssh/config con mi usuario, mi clave y la ruta
absoluta de cloudflared. Aplique 700 a ~/.ssh y 600 a su archivo config.
Guíeme para completar Cloudflare Access en el navegador fuera del chat.
No capture ni reproduzca tokens, códigos ni claves API; no me pida pegarlos aquí.
Compruebe ssh servidor-migraciones, whoami y gentle-shell --version con mi cuenta.
No modifique el servidor, no use sudo remoto, no toque bases ni inicie una migración.
Si algo falla, muestre el error sin secretos y el próximo paso; no desactive Access
ni la comprobación de la huella. Termine con los comandos para entrar y retomar tmux.
```

</details>

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

Para hacerlo con una IA, despliegue y copie el siguiente prompt. Para hacerlo manualmente,
continúe con los comandos debajo.

<details markdown>
<summary>Prompt para configurar el acceso con una IA — macOS</summary>

```text
Ayúdeme a configurar el acceso a PC-ALE desde macOS usando Terminal.

Antes de empezar, pídame el hostname, mi usuario Linux asignado y la huella SSH
esperada; confirme que el administrador habilitó mi cuenta y mi email en Access.
Trabaje solo en mi computadora. Pida autorización para las rutas concretas y
antes de instalar herramientas o editar configuración; conserve una copia del
archivo SSH de configuración existente y agregue el alias sin sobrescribir otros accesos.
Detecte si mi Mac es Intel o Apple Silicon. Compruebe OpenSSH y Homebrew.
Use Homebrew para instalar cloudflared solo si falta; si falta Homebrew, guíeme
con su sitio oficial y espere mi autorización antes de instalarlo.
Obtenga la ruta real con command -v cloudflared; no suponga /usr/local/bin
ni /opt/homebrew/bin para todos los equipos.
Reutilice mi clave pública autorizada o guíeme para crear una sin sobrescribir
claves existentes. No lea ni copie el contenido de ninguna clave privada.
Solo la clave pública .pub se entrega al administrador; espere que confirme su alta.
Configure servidor-migraciones en ~/.ssh/config con mi usuario, mi clave y la ruta
absoluta de cloudflared. Aplique 700 a ~/.ssh y 600 a su archivo config.
Guíeme para completar Cloudflare Access en el navegador fuera del chat.
No capture ni reproduzca tokens, códigos ni claves API; no me pida pegarlos aquí.
Compruebe ssh servidor-migraciones, whoami y gentle-shell --version con mi cuenta.
No modifique el servidor, no use sudo remoto, no toque bases ni inicie una migración.
Si algo falla, muestre el error sin secretos y el próximo paso; no desactive Access
ni la comprobación de la huella. Termine con los comandos para entrar y retomar tmux.
```

</details>

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
etapa, copie la [autorización correspondiente del Procedimiento](procedure.md#7-seguir-al-agente-y-el-plan-en-espiral).
Para las etapas técnicas, siga el [Plan técnico en espiral](spiral-strategy.md);
no autorice toda la migración de una vez. El [Procedimiento](procedure.md) resume el acceso
y la puesta en marcha del trabajo con el agente.

## 7. Retomar el trabajo

Para salir sin cerrar la sesión: **Ctrl+b**, suelte y presione **d**.

Para volver, **desde su computadora**:

```sh
ssh servidor-migraciones
```

**En el servidor**, localice primero la instancia y compruebe la coordinación;
reemplace el caso de ejemplo:

```sh
tmux list-sessions
tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index} | #{pane_current_command} | #{pane_current_path}'
mig-case status MIG-CLIENTE-001
```

Si lo coordina otra persona, acuerde el relevo. El nombre de proceso `node` por sí
solo no identifica el caso: contraste la ruta y después la pantalla.
Si encuentra el agente en `trabajo`, ventana `0`, recupérelo así; cambie ambos
valores por los que realmente encontró:

```sh
tmux attach-session -t trabajo:0
```

No vuelva a ejecutar `gentle-shell` ni reclame otra vez un caso que sigue coordinado
por su usuario. Si Gentle Shell sigue abierto en el caso correcto, pegue:

```text
Lea únicamente runbook.md, module-board.yml y case-intake.yml del caso actual.
Resuma dónde quedamos, los bloqueos y el próximo paso propuesto.
Distinga valores de plantilla de datos confirmados. No modifique archivos,
consulte servicios ni ejecute acciones nuevas: espere una nueva autorización.
```

Vea el [recorrido de reconexión y recuperación](#ejemplo-guiado-para-retomar-un-caso)
para distinguir una instancia viva de un agente que ya se cerró.

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

## Ejemplo guiado de inicio

Este recorrido muestra cómo pasar de una terminal local a un caso listo para
completar su ficha. **No ejecuta una migración de código ni de base de datos.**
Use el caso ficticio `MIG-DEMO1719-001`, la cuenta personal de ejemplo `dev1`,
el alias SSH `servidor-migraciones` y la sesión `main`. Reemplácelos por los datos
asignados; no comparta cuentas ni credenciales. `1719` es parte del nombre, no una
confirmación de versiones. El acceso debe estar preparado según el paso 1 del manual.

Puede hacer cada paso manualmente o desplegar su **prompt de asistencia**.
Si usa una IA con control de terminales, indique la terminal exacta; si no tiene
ese control, pídale los comandos para ejecutarlos usted. Antes de actuar, la IA debe
explicar qué hará, pedir autorización, mostrar el resultado y detenerse antes del
siguiente paso. Un permiso para conectarse no autoriza crear casos, dar confianza a
carpetas ni modificar una migración. Herdr no es un requisito de este recorrido.

### Paso 1 — Identificar la terminal

**En la terminal que pretende usar**, compruebe dónde está y con qué usuario.
No confunda una pestaña rotulada «Linux» con una conexión SSH activa: después de un
corte puede haber vuelto a su computadora.

**macOS o Linux:**

```sh
whoami
hostname
uname -s
pwd
command -v ssh
command -v cloudflared
```

`Darwin` indica macOS; `Linux` no basta para probar que está en PC-ALE: contraste
usuario y equipo con los datos del administrador. **Windows — PowerShell:**

```powershell
whoami
hostname
Get-Location
Get-Command ssh, cloudflared -ErrorAction SilentlyContinue
```

**Resultado esperado:** distinguir computadora local y servidor, y saber si existen
SSH y cloudflared. Si falta una herramienta, vuelva a la preparación de su sistema;
no instale nada como parte de este diagnóstico.

<details markdown>
<summary>Prompt de asistencia — paso 1: identificar la terminal</summary>

```text
Asístame en el paso 1. Identifique conmigo la terminal concreta que voy a usar.
Explique el paso y pida mi autorización antes de ejecutarlo.
Compruebe usuario, equipo, sistema, carpeta y disponibilidad de SSH y cloudflared
con comandos de lectura adecuados a mi sistema. No suponga que ya estoy en Linux
remoto por el nombre de la pestaña. No instale herramientas ni lea claves privadas.
Si no puede controlar la terminal, muéstreme qué ejecutar manualmente.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

### Paso 2 — Conectarse con la cuenta personal

**En su computadora**, usando el alias ya configurado:

```sh
ssh -l dev1 servidor-migraciones
```

Use su propio usuario asignado. Complete Cloudflare Access en el navegador si lo
solicita; no copie códigos al chat. Ante una huella nueva o distinta, deténgase y
confírmela con el administrador, sin desactivar su comprobación.

**Resultado esperado:** un prompt como `dev1@pc-ale:~$`. No continúe si sigue en la
computadora local o si entró con una cuenta que no le corresponde.

<details markdown>
<summary>Prompt de asistencia — paso 2: conectarse por SSH</summary>

```text
Asístame en el paso 2. Confirme mi usuario personal y el alias SSH configurado.
Explique el paso y pida mi autorización antes de ejecutarlo.
Con los datos confirmados, use ssh -l dev1 servidor-migraciones, reemplazando los
valores de ejemplo por los míos. Deje que complete Access en el navegador.
Si cambia la huella, deténgase y pida confirmación al administrador.
Compruebe el prompt remoto. No instale nada ni desactive controles de acceso.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

### Paso 3 — Abrir una sesión persistente

**En el servidor:**

```sh
tmux new-session -A -s main
```

Crea `main` si no existe o la recupera si ya existe. **Resultado esperado:** la barra
de tmux muestra `[main]`. Si recupera trabajo anterior, revise qué está abierto
antes de escribir: no envíe comandos de shell dentro del chat de un agente.
La sesión puede sobrevivir a un corte de SSH, pero no a un reinicio del servidor.

<details markdown>
<summary>Prompt de asistencia — paso 3: preparar tmux</summary>

```text
Asístame en el paso 3. Verifique que estoy en un prompt del servidor con mi cuenta.
Explique el paso y pida mi autorización antes de ejecutarlo.
Ejecute únicamente tmux new-session -A -s main y compruebe la barra de sesión.
Si se recupera una aplicación o un agente, identifíquelo antes de enviar texto.
No cierre sesiones existentes ni inicie una migración.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

### Paso 4 — Abrir Gentle Shell para comprobar el entorno

**En un prompt libre dentro de tmux:**

```sh
gentle-shell
```

**Resultado esperado:** Gentle Shell muestra el modelo seleccionado y espera
instrucciones. Abrirlo puede preparar configuración personal en su cuenta, pero no
confirma que el proveedor responda. Si aparecen actualizaciones, no las ejecute:
las herramientas compartidas las administra el responsable del servidor.

Esta primera apertura desde `~` solo comprueba el entorno. Todavía no es la sesión
de trabajo de un caso y no debe recibir instrucciones de migración.

<details markdown>
<summary>Prompt de asistencia — paso 4: abrir el entorno de prueba</summary>

```text
Asístame en el paso 4. Confirme que hay un prompt libre dentro de tmux.
Explique el paso y pida mi autorización antes de ejecutarlo.
Abra únicamente gentle-shell desde mi home. Observe el modelo y si espera entrada.
No envíe consultas todavía ni instale actualizaciones, cree casos o abra repositorios.
Si falta autenticación, guíeme con /login sin capturar mis credenciales.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

### Paso 5 — Probar la respuesta del modelo

**En el chat de Gentle Shell**, con permiso para consumir uso del proveedor:

```text
Responda únicamente: CONEXIÓN OK.
No use herramientas, no ejecute comandos ni lea o modifique archivos.
```

**Resultado esperado:** una respuesta con `CONEXIÓN OK` y regreso al estado de espera,
sin llamadas a herramientas. Puede consumir uso del modelo aunque el mensaje sea
breve. Si falla, resuelva autenticación o disponibilidad antes de seguir; no cambie
a otro proveedor sin permiso. Use sus propias credenciales: esta prueba no verifica
su titularidad ni demuestra que GitHub u Odoo.sh sean accesibles.

<details markdown>
<summary>Prompt de asistencia — paso 5: comprobar el proveedor</summary>

```text
Asístame en el paso 5. Muestre el modelo actualmente seleccionado, sin cambiarlo.
Explique el paso y pida mi autorización antes de ejecutarlo.
Avise que la consulta consume uso del proveedor. Envíe una sola vez:
«Responda únicamente: CONEXIÓN OK. No use herramientas, no ejecute comandos ni
lea o modifique archivos». Observe la respuesta o el error sin reintentos automáticos.
No use este resultado como prueba de acceso a repositorios o bases.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

### Paso 6 — Abrir una consola auxiliar y consultar los casos

**Dentro de tmux**, presione **Ctrl+b**, suelte y luego **c**. Se abre otra ventana
con un prompt de shell; la anterior conserva Gentle Shell. Allí ejecute:

```sh
mig-case list
```

**Resultado esperado:** una lista de casos y su coordinación. Una salida vacía sin
errores indica que no se listaron casos; un mensaje de error no equivale a una lista
vacía. Esto no crea ni reclama nada. Para cambiar de ventana, use **Ctrl+b** y luego
**0** o **1**, comprobando los números en la barra de tmux.

<details markdown>
<summary>Prompt de asistencia — paso 6: consultar casos existentes</summary>

```text
Asístame en el paso 6. Conserve Gentle Shell abierto sin enviarle comandos de shell.
Explique el paso y pida mi autorización antes de ejecutarlo.
Abra una consola auxiliar en el mismo tmux con Ctrl+b y luego c. Compruebe que
hay un prompt y ejecute solo mig-case list. Distinga lista vacía de error.
No cree casos, reclame coordinación ni cierre la ventana anterior.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

### Paso 7 — Elegir el identificador y crear el caso

El kit exige `MIG-<NOMBRE>-<NNN>`: nombre alfanumérico en mayúsculas y **exactamente
tres dígitos finales**. `MIG-DEMO-1719` no es válido. Para conservar `1719` como parte
del nombre se puede proponer `MIG-DEMO1719-001`; el usuario debe aceptarlo, no la IA.

**En la consola auxiliar**, solo para un caso nuevo autorizado:

```sh
mig-case new MIG-DEMO1719-001
```

**Resultado esperado:** `created /srv/migraciones/cases/MIG-DEMO1719-001`.
Crea la ficha, el tablero, el runbook y la configuración de proyecto. No toma la
coordinación, clona repositorios ni modifica bases. Si el caso ya existe, no lo
sobrescriba: revise si corresponde retomarlo.

<details markdown>
<summary>Prompt de asistencia — paso 7: crear el caso</summary>

```text
Asístame en el paso 7. Pídame el identificador y valide MIG-<NOMBRE>-<NNN>.
Si propongo MIG-DEMO-1719, explique el rechazo y proponga MIG-DEMO1719-001,
sin cambiarlo ni crearlo hasta que yo acepte el nombre.
Explique el paso y pida mi autorización antes de ejecutarlo.
Para ese ejemplo aceptado, ejecute solo mig-case new MIG-DEMO1719-001 y observe
el resultado. No sobrescriba casos existentes ni tome aún la coordinación.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

### Paso 8 — Tomar la coordinación y entrar al caso

**En la consola auxiliar del servidor:**

```sh
mig-case claim MIG-DEMO1719-001 &&
cd /srv/migraciones/cases/MIG-DEMO1719-001
```

`&&` evita entrar si falla el reclamo. **Resultado esperado:** el caso queda
reclamado por su usuario y el prompt muestra su carpeta. Si otra persona lo coordina,
**no borre su lock**: acuerde el relevo. El lock es un acuerdo operativo, no una
barrera de seguridad. Haberlo tomado no autoriza operaciones sobre repositorios o bases.

<details markdown>
<summary>Prompt de asistencia — paso 8: tomar la coordinación</summary>

```text
Asístame en el paso 8. Caso: MIG-DEMO1719-001; use el identificador real que acepté.
Explique el paso y pida mi autorización antes de ejecutarlo.
Ejecute mig-case claim MIG-DEMO1719-001 && cd /srv/migraciones/cases/MIG-DEMO1719-001.
Compruebe el resultado y la carpeta del prompt. Si otro usuario coordina el caso,
deténgase: no borre ni fuerce el lock. No clone ni acceda a bases.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

### Paso 9 — Abrir Gentle Shell dentro del caso y resolver la confianza

**Desde la carpeta del caso:**

```sh
gentle-shell
```

Ahora el entorno puede cargar la configuración de esa migración; el modelo puede
ser distinto del usado en `~`. Compruébelo antes de enviar instrucciones. No use la
ventana de prueba del home como coordinador de este caso ni abra coordinadores
competidores del mismo caso.

Si aparece **`Trust project folder?`**, deténgase: autorizar el inicio no equivale
a aceptar esa confianza. El permiso permite cargar recursos y configuración `.pi`,
instalar paquetes de proyecto faltantes y ejecutar extensiones. Revise quién preparó
la carpeta. Si confía en ella, puede elegir **`Trust (this session only)`**, limitado
a este caso y esta sesión. No confíe en la carpeta padre de todos los casos por
comodidad. La elección la hace el usuario; si la IA maneja la terminal, necesita
una autorización separada para seleccionar la opción concreta.

**Resultado esperado:** el usuario resuelve el diálogo y Gentle Shell espera entrada
en el caso correcto. Una alerta de herramientas o skills ausentes no demuestra que
el servidor esté completamente preparado: consúltela con el administrador.

<details markdown>
<summary>Prompt de asistencia — paso 9: abrir el entorno del caso</summary>

```text
Asístame en el paso 9. Compruebe que el prompt está en la carpeta del caso reclamado.
Explique el paso y pida mi autorización antes de ejecutarlo.
Abra gentle-shell. Si aparece Trust project folder?, muestre la ruta y explique
que confiar permite cargar .pi, instalar paquetes y ejecutar extensiones.
Deténgase y pida una decisión separada sobre la opción exacta; no acepte confianza
ni amplíe el permiso a la carpeta padre automáticamente. Si yo resuelvo el diálogo,
observe el resultado sin asumir qué opción elegí. Compruebe el caso, modelo y estado
de espera. No envíe instrucciones de migración ni instale actualizaciones.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

### Paso 10 — Pedir una revisión inicial solo de lectura

**En Gentle Shell del caso**, autorice únicamente la lectura inicial. Pida al
administrador la ruta de la guía de lecciones del kit y reemplace
`<RUTA_DE_GUIA_DE_LECCIONES>` antes de enviar el prompt. No publique nombres de casos
reales en ejemplos compartidos. El prompt sirve tanto para pedir asistencia como
para dárselo directamente al agente:

<details markdown>
<summary>Prompt de asistencia — paso 10: revisar el estado inicial</summary>

```text
Asístame en el paso 10. Caso: MIG-DEMO1719-001; use el identificador real aceptado.
Explique el paso y pida mi autorización antes de ejecutarlo.
Tras mi aprobación, lea únicamente case-intake.yml, module-board.yml y runbook.md
ubicados en la carpeta del caso, y estas dos guías:
- /srv/migraciones/kit/docs/migration-spiral-strategy-spec.md
- <RUTA_DE_GUIA_DE_LECCIONES>
Informe qué está registrado, qué datos faltan y qué próximo paso propone,
con la autorización que necesitaría. No infiera versiones por el nombre del caso
ni trate valores de plantilla como datos confirmados del proyecto.
No modifique archivos, no instale paquetes, no clone repositorios,
no consulte servicios externos ni acceda a bases de datos.
No use Engram ni memoria persistente mientras su aislamiento no esté validado.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

**Resultado esperado:** un diagnóstico basado en esos archivos, sin cambios.
En un caso recién creado puede encontrar una ficha sin completar, un tablero con
`modules: []` y un runbook con la entrada pendiente. Eso describe la plantilla,
no una migración inspeccionada ni aprobada. Si falta un archivo, debe informarlo y
esperar; no crearlo ni sustituir la fuente sin permiso.

### Paso 11 — Reunir y confirmar los datos antes de escribir la ficha

**Fuera de cualquier comando de ejecución**, complete esta lista con el responsable
de la migración. Si falta un dato, escriba «sin confirmar»:

```text
Versión de Odoo de origen:
Versión de Odoo de destino:
URL del repositorio de origen:
Rama de origen:
Proyecto Odoo.sh de origen:
Proyecto Odoo.sh de destino, si ya existe:
```

El `19.0` de una plantilla no confirma el destino del caso. Tampoco el nombre
`DEMO1719` confirma una migración 17 → 19. Distinga lo que declara el responsable
de lo que luego se verificará mediante evidencia autorizada.

**Resultado esperado:** datos confirmados y preguntas pendientes, más una propuesta
de qué registrar en `case-intake.yml`. Pida autorización antes de escribirlo.
Consultar repositorios o bases, registrar claves, pedir una actualización de base,
hacer commits o push requiere su propio alcance y permiso: no se desprende de haber
completado esta lista. La coordinación ya tomada no necesita un nuevo reclamo.

<details markdown>
<summary>Prompt de asistencia — paso 11: preparar la ficha inicial</summary>

```text
Asístame en el paso 11. Pídame versiones exactas de origen y destino,
URL y rama del repositorio de origen, y proyectos Odoo.sh de origen y destino.
Explique el paso y pida mi autorización antes de ejecutarlo.
Si falta un dato, conserve «sin confirmar». Separe mi declaración de la evidencia
verificada. No tome 19.0 de la plantilla ni el nombre del caso como confirmación.
Devuélvame una propuesta de ficha y pida un permiso separado antes de escribirla.
No consulte repositorios o servicios, acceda a bases, registre claves ni solicite
actualizaciones de base. No haga commits ni push. No vuelva a reclamar el caso
si ya está coordinado por mi usuario.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

Para continuar después de aprobar la ficha y delimitar las fuentes, use
[Empezar la migración](#6-empezar-la-migracion) y las autorizaciones por etapa de
[Procedimiento](procedure.md#7-seguir-al-agente-y-el-plan-en-espiral). Para desconectarse o entregar,
siga [Retomar el trabajo](#7-retomar-el-trabajo) o [Entregar el caso](#8-entregar-el-caso).

## Ejemplo guiado para retomar un caso

Este recorrido recupera una instancia de Gentle Shell que **sigue ejecutándose en
PC-ALE aunque el usuario cierre SSH**. Luego contrasta el estado con los archivos
del caso, antes de autorizar trabajo nuevo. No abre una instancia de Odoo ni valida
una migración: recupera el entorno del agente.

Use el ejemplo ficticio `MIG-DEMO1719-001`, cuenta personal `dev1`, alias
`servidor-migraciones` y sesión `main`, ventana `1`. Reemplace esos valores por los
asignados y por los encontrados en las consultas; no suponga que todos los casos
usan la misma ventana. Cada prompt de asistencia pide autorización antes de actuar
y se detiene antes del siguiente paso. Si la IA no controla terminales, le debe
indicar los comandos para ejecutarlos usted.

### Paso 1 — Identificar qué quedó abierto

**En la terminal del usuario**, observe la pantalla antes de escribir. Distinga un
prompt local, un prompt remoto y el chat de Gentle Shell. Si continúa dentro de
tmux, su barra puede mostrar `[main]` y la ventana activa. Si el agente indica
`waiting for input`, está esperando: no significa que la migración esté terminada.

**Resultado esperado:** identificar equipo, cuenta, sesión, ventana y caso visibles.
Si el agente está trabajando, no lo interrumpa ni presuponga que se puede desconectar
sin evaluar la operación. Si ya está desconectado, vaya al paso 3, no ejecute `exit`
en su computadora por copiar el paso 2.

<details markdown>
<summary>Prompt de asistencia — retomar, paso 1: inspeccionar la terminal</summary>

```text
Para retomar, asístame en el paso 1. Identifique conmigo la terminal exacta.
Explique el paso y pida mi autorización antes de ejecutarlo.
Inspeccione solo la pantalla para distinguir equipo local, SSH, tmux y agente.
Informe sesión, ventana, caso y si el agente espera o trabaja; no envíe texto
ni comandos todavía. Si no puede ver la terminal, pídame esos datos sin secretos.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

### Paso 2 — Desconectarse sin cerrar el agente

Este paso prepara la prueba de salida y regreso. **Dentro de tmux**, presione
**Ctrl+b**, suelte y presione **d**. Espere el mensaje de separación y el **prompt remoto**. Solo después, para cerrar SSH:

```sh
exit
```

**Resultado esperado:** vuelve al prompt de su computadora. Esto **no libera** la
coordinación ni cierra intencionalmente Gentle Shell. No use `Ctrl+c`, `kill-session`
ni el comando de salida del agente para simular esta desconexión. Todavía hay que
reconectar y verificar que el proceso se conservó. tmux no protege de un reinicio
del servidor ni de que otro usuario termine el proceso.

<details markdown>
<summary>Prompt de asistencia — retomar, paso 2: separar tmux y cerrar SSH</summary>

```text
Para retomar, asístame en el paso 2. Confirme que el agente no está trabajando.
Explique el paso y pida mi autorización antes de ejecutarlo.
Separe el cliente de tmux con Ctrl+b y luego d. Observe el mensaje de separación
y el prompt remoto. Solo entonces ejecute exit para cerrar únicamente SSH.
Si no aparece ese prompt, deténgase. Compruebe retorno a la computadora local.
No cierre el agente, mate procesos, libere coordinación ni altere otras sesiones.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

### Paso 3 — Conectarse de nuevo con la misma cuenta

**En su computadora:**

```sh
ssh -l dev1 servidor-migraciones
```

**Resultado esperado:** vuelve al prompt remoto de su cuenta personal. Complete
Cloudflare Access en el navegador si lo solicita. Si cambia de cuenta, no verá las
sesiones personales de la anterior: no use credenciales ajenas para recuperarlas.
No ejecute todavía `gentle-shell` ni cree un nuevo caso.

<details markdown>
<summary>Prompt de asistencia — retomar, paso 3: volver a PC-ALE</summary>

```text
Para retomar, asístame en el paso 3. Confirme el alias y mi cuenta personal asignada.
Explique el paso y pida mi autorización antes de ejecutarlo.
Con los datos confirmados, conecte usando ssh -l dev1 servidor-migraciones,
reemplazando el ejemplo por mi cuenta y alias. Deje que complete Access fuera del chat.
Confirme el prompt remoto; no acepte una huella nueva sin verificarla con el administrador.
No abra agentes ni cree sesiones o casos todavía.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

### Paso 4 — Localizar la instancia y comprobar la coordinación

**En el prompt del servidor**, no en el chat de un agente:

```sh
tmux list-sessions
tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index} | #{pane_current_command} | #{pane_current_path}'
mig-case status MIG-DEMO1719-001
```

**Resultado esperado:** una fila como esta, con los valores reales de su sesión:

```text
main:1.0 | node | /srv/migraciones/cases/MIG-DEMO1719-001
```

La fila orienta hacia `main`, ventana `1`, panel `0`. `node` no prueba por sí solo
que sea el agente correcto: hay que contrastar ruta y pantalla. Verifique además
que el caso sigue coordinado por su usuario. Si otra persona lo coordina, deténgase
y acuerde el relevo; no borre el lock. No se vuelva a reclamar un caso ya coordinado
por su usuario solo por reconectar.

Si aparecen varias sesiones o una marcada `attached`, no las cierre, separe ni
reutilice automáticamente. Identifique el caso antes de seleccionar un destino.
Si falta la sesión o el proceso del caso, vaya a la variante posterior; no cree otro
coordinador para ocultar el problema.

<details markdown>
<summary>Prompt de asistencia — retomar, paso 4: localizar sin modificar</summary>

```text
Para retomar, asístame en el paso 4. Caso: MIG-DEMO1719-001; use mi caso real confirmado.
Explique el paso y pida mi autorización antes de ejecutarlo.
Ejecute solo tmux list-sessions, tmux list-panes -a -F
'#{session_name}:#{window_index}.#{pane_index} | #{pane_current_command} | #{pane_current_path}'
y mig-case status MIG-DEMO1719-001, sustituyendo el caso confirmado.
Informe qué sesión/ventana/panel tiene la ruta del caso y quién lo coordina.
No dé por correcto un proceso solo porque se llama node. No toque otras sesiones,
cree agentes, fuerce locks ni adjunte todavía. Si algo falta, informe el bloqueo.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

### Paso 5 — Recuperar la ventana existente

**En el prompt remoto**, si la consulta localizó su caso en `main`, ventana `1`:

```sh
tmux attach-session -t main:1
```

Reemplace sesión y ventana según lo observado. **Resultado esperado:** reaparecen
Gentle Shell y la conversación anterior del caso, en la ventana elegida.
No ejecute de nuevo `gentle-shell`: si el agente sigue vivo, el directorio de trabajo
ya está conservado. Tampoco necesita `cd` para recuperar ese proceso.

Si aparece otro caso, una aplicación inesperada o un prompt vacío, deténgase:
recuperar tmux no prueba que el agente buscado siga abierto. No escriba comandos de
shell en el chat ni envíe una instrucción de migración solo para probar la pantalla.

<details markdown>
<summary>Prompt de asistencia — retomar, paso 5: recuperar sin duplicar agentes</summary>

```text
Para retomar, asístame en el paso 5. Use la sesión y ventana identificadas antes.
Explique el paso y pida mi autorización antes de ejecutarlo.
Si mi caso está en main:1, ejecute solo tmux attach-session -t main:1;
si está en otro destino, muéstreme primero el comando exacto corregido y espere permiso.
Compruebe que vuelve la conversación del caso y el agente espera instrucciones.
No abra otro gentle-shell, cambie coordinación ni envíe mensajes de migración.
Si vuelve una pantalla inesperada, deténgase y describa lo observado.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

### Paso 6 — Reconstruir el estado antes de continuar

**En la instancia recuperada**, pida una revisión de lectura. La conversación puede
estar conservada, pero el estado del trabajo debe contrastarse con el runbook, el
tablero y la ficha. Esta consulta consume uso del modelo; no autoriza escrituras.

<details markdown>
<summary>Prompt de asistencia — retomar, paso 6: resumir estado sin ejecutar trabajo</summary>

```text
Para retomar, asístame en el paso 6. Caso: MIG-DEMO1719-001; use el caso confirmado.
Explique el paso y pida mi autorización antes de ejecutarlo.
Tras mi aprobación, lea únicamente runbook.md, module-board.yml y case-intake.yml
de la carpeta actual del caso. Informe:
1. Qué está registrado y qué sigue sin confirmar.
2. En qué etapa está el caso y qué bloqueos tiene.
3. Cuál es el próximo paso propuesto y qué autorización necesita.
Distinga valores de plantilla de datos confirmados; no infiera versiones por el nombre.
Si mi usuario ya coordina el caso, no vuelva a reclamarlo.
No modifique archivos, no ejecute comandos de migración, no consulte repositorios,
servicios externos ni bases de datos. No use Engram ni memoria persistente mientras
su aislamiento no esté validado. No retome acciones anteriores automáticamente.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

**Resultado esperado:** un resumen verificable y una propuesta que espera permiso.
En un caso recién creado, el resumen puede indicar que la ficha sigue sin completar
y el tablero está vacío. Recuperar la sesión no convierte eso en avance de migración
ni confirma la versión `19.0` que viene en la plantilla. Para trabajo nuevo, otorgue
solo la autorización de la etapa correspondiente del
[Procedimiento](procedure.md#7-seguir-al-agente-y-el-plan-en-espiral).

### Si el agente ya no está abierto

**Esta variante no se probó en el recorrido de reconexión anterior.** No confunda
un proceso que sigue vivo con volver a abrir uno cerrado. Si no existe la sesión o
solo queda un prompt, compruebe primero cuenta, ruta, coordinación y si hay otro
agente del caso activo. Si la coordinación está libre, acuerde quién continúa y
autorice el reclamo según [Abrir el caso](#4-abrir-el-caso); si la tiene otra persona,
espere el relevo.

Solo después de resolver eso, con permiso para abrir un nuevo entorno:

```sh
cd /srv/migraciones/cases/MIG-DEMO1719-001 && pwd
```

Si la ruta existe y es la correcta, abra el entorno en una sesión tmux:

```sh
gentle-shell
```

Esto carga la configuración del directorio, pero **no recupera automáticamente la conversación**
anterior. Si aparece un diálogo de confianza, necesita su propia decisión. Reconstruya
el estado con los tres archivos del caso; recuperar un historial guardado requiere
confirmar el procedimiento disponible en la versión instalada, no inventar opciones
ni identificadores. No documentamos esta variante como una recuperación comprobada.

<details markdown>
<summary>Prompt de asistencia — si falta el agente o su sesión</summary>

```text
Si falta el agente, ayúdeme a diagnosticarlo sin abrir otro automáticamente.
Explique el paso y pida mi autorización antes de ejecutarlo.
Confirme mi cuenta, la ruta del caso, su coordinación y si existe otro agente activo.
No fuerce locks ni cree sesiones para ocultar el problema. Muestre un plan acotado
para entrar al directorio correcto y abrir el entorno solo si corresponde, sin
prometer que eso recupera la conversación anterior. Pida permiso para cada acción;
la confianza de carpeta requiere una decisión separada. No invente flags de reanudación.
No pida ni muestre secretos.
No avance al siguiente paso sin una nueva autorización.
```

</details>

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

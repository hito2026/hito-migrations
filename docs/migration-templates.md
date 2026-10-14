# Plantillas de entrada y seguimiento de módulos

**Estado: plantillas no verificadas.** Copie la estructura, no supuestos de éxito.
Use marcadores genéricos y material autorizado para publicación. No incluya identificadores
reales, direcciones, IP, hashes, datos personales, código de clientes ni registros privados.
El anonimato no otorga permiso de publicación; conserve referencias sensibles en el sistema
privado aprobado, nunca en esta página.

## Ficha de entrada anonimizada

Complete esta ficha antes de asignar módulos. Un campo pendiente debe producir una
pregunta concreta, no una autorización implícita.

| Campo | Marcador que completar |
| --- | --- |
| Contexto | `<etiqueta genérica sin identidad del cliente>` |
| Versiones | `<versiones y compilaciones exactas de origen y destino; dependencias>` |
| Edición | `<edición de origen y destino; restricciones aplicables>` |
| Runtime | `<entornos previstos; aislamiento e integraciones por evaluar>` |
| Alcance | `<código>` / `<base de datos>` / `<integraciones autorizadas>` |
| Permisos | `<acciones y archivos autorizados; rol que aprueba; límites y vigencia>` |
| No objetivos | `<operaciones, módulos y datos expresamente excluidos>` |
| Inventario | `<módulos, familias de repositorios y fuentes autorizadas; grafo pendiente o revisado>` |
| Aceptación | `<criterios separados de código, runtime, datos y negocio; rol que acepta>` |
| Responsabilidad de datos | `<rol responsable del acceso, copias, restauración, conciliación y aprobación>` |
| Recuperación | `<criterios de parada; responsabilidades y evidencias de ensayo pendientes>` |
| Decisiones abiertas | `<pregunta; opciones; rol decisor; condición para continuar>` |

No complete los permisos con comandos ni ubicaciones privadas. Esta ficha planifica;
no autoriza operaciones sobre bases de datos ni ejecución en producción.

## Tarjeta reutilizable de módulo

Mantenga una tarjeta por unidad de trabajo; separe disposición, estado y evidencia.
Las referencias siguientes son marcadores, no ramas, repositorios ni revisiones reales.

| Campo | Marcador que completar |
| --- | --- |
| Módulo | `<nombre genérico autorizado>` |
| Referencia origen | `<referencia_origen_autorizada>` |
| Referencia destino | `<referencia_destino_propuesta>` |
| Familia de repositorio destino | `<upstream / comunitario / extensiones propias autorizadas / por decidir>` |
| Dependencias | `<directas, transitivas, auto-instalables; consumidores y ciclos>` |
| Disposición | `<clasificación de S2 y justificación; decisión pendiente si falta evidencia>` |
| Estado | `<estado respaldado del tablero; contexto y fecha>` |
| Responsable | `<rol con propiedad exclusiva de archivos acotados>` |
| Superficie de edición | `<archivos autorizados; exclusiones y contratos compartidos>` |
| Evidencia de código | `<prueba; esperado; observado; contexto; limitaciones o pendiente>` |
| Evidencia de runtime | `<prueba aislada; esperado; observado; contexto; limitaciones o pendiente>` |
| Evidencia de datos | `<copia migrada autorizada; invariantes y conciliación; resultados o pendiente>` |
| Aceptación | `<decisión humana funcional/contable; riesgos aceptados o pendiente>` |
| Bloqueos | `<impedimento; rol decisor; condición de desbloqueo>` |
| Riesgos | `<historia, numeración, seguridad, equivalencia u otras incógnitas>` |
| Próxima acción | `<acción acotada; permiso requerido; evidencia esperada>` |

Use el [catálogo de disposiciones y estados](spiral-strategy.md) sin saltar controles.
Una referencia destino existente o código publicado no prueba equivalencia ni aceptación.
Si cambia el contexto, indique qué evidencias requieren revalidación.

## Orden de oleadas opcional

| Oleada propuesta | Dependencias previas | Propiedad exclusiva | Condición de integración |
| --- | --- | --- | --- |
| `<base>` | `<grafo revisado dentro del alcance>` | `<rol y archivos autorizados>` | `<pruebas y contratos acordados>` |
| `<consumidores>` | `<base validada para el contrato requerido>` | `<rol y archivos sin solapamiento>` | `<evidencias y bloqueos revisados>` |

El orden es una propuesta, no un permiso para crear ramas o integrar. Solo use trabajadores
paralelos con worktrees y ramas aislados y asignaciones sin solapamiento. El coordinador
mantiene el tablero y revisa dependencias e integración bajo autorización humana.

## Revisión de la ficha

- [ ] Versiones, alcance, permisos y no objetivos son explícitos.
- [ ] El grafo completo no incorpora trabajo fuera del alcance aprobado.
- [ ] Código, runtime y datos tienen evidencias separadas; lo pendiente permanece visible.
- [ ] La aceptación pertenece a una persona autorizada, no a una publicación de código.
- [ ] El contenido tiene permiso de publicación y no revela información sensible.

Continúe con la [estrategia en espiral](spiral-strategy.md), la [guía de IA](ai-guide.md)
y la [lista de validación](validation.md). Para resumir un ensayo observado y autorizado,
use la [plantilla de caso](case-template.md), no estas fichas como prueba de éxito.

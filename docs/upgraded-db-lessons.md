# Lecciones: base migrada por el servicio oficial (17 → 19)

**Estado: verificado en un contexto declarado.** Observado en un caso real
anonimizado; no es una receta universal. Repita cada comprobación en su
propio contexto antes de aplicar nada.

## Contexto declarado

- **Par de versiones:** Odoo 17.0 Enterprise → 19.0 Enterprise (servicio de
  upgrade oficial, con paso intermedio por 18.0), localización argentina.
- **Entorno:** Odoo.sh; base importada en una rama de Staging de prueba.
- **Dependencias:** stack ADHOC 19.0 (`account_payment_pro`, `l10n_ar_tax`,
  `l10n_ar_account_reports`, `l10n_latam_check_ux`) y módulos propios migrados.
- **Dump de origen:** sin filestore y neutralizado; ver la lección de *assets*.
- **Línea:** base de datos (S5). La migración de código se hizo antes (S3/S4).

## Qué deja el upgrade oficial

- Los módulos de terceros **sin código en el destino** quedan como
  "para actualizar" con sus **tablas y datos intactos**, pero sus modelos no
  se cargan.
- Sus **vistas, menús y restricciones de grupo siguen activos** en la base.
- El informe del upgrade lista impuestos con fórmula Python inválida, vistas
  desactivadas y módulos renombrados por conflicto de nombre. Léalo completo.

## Problemas observados y tratamiento aplicado

Todos los ajustes fueron reversibles, registrados en `ir_config_parameter`,
aplicados con autorización humana y **sin tocar registros de negocio**.

| # | Síntoma al instalar o usar el stack destino | Causa observada | Tratamiento aplicado |
|---|---|---|---|
| A | Falla la carga: una vista hereda una vista estándar y usa un campo inexistente | Vistas activas de módulos sin código en el destino | Desactivar las vistas activas de esos módulos |
| B | Falla al actualizar un módulo que sí tiene código destino | Vistas propias de la versión vieja que ya no existen en el código nuevo; Odoo valida las nuevas antes de borrar las viejas | Desactivar las vistas cuyo `xmlid` ya no está en el código destino |
| C | Falla la limpieza final al borrar una vista obsoleta | Vistas hijas (incluida Studio) que la heredan | Desenganchar y desactivar las hijas |
| D | "Ya existe un índice para el período…" | Datos absorbidos por otro módulo con el mismo `xmlid` | Pasar la propiedad del `xmlid` al módulo nuevo tras comparar valores |
| E | Falla al borrar etiquetas contables obsoletas | Etiquetas usadas por impuestos y líneas contables | Conservarlas moviendo su `xmlid` fuera de la limpieza |
| G | Un menú abre con `404 … KeyError: '<modelo>'` | Menús de módulos sin código en el destino | Desactivar esos menús |
| H | Desaparecen los menús estándar de pagos | El módulo viejo los ocultaba con un grupo propio | Quitar de los menús estándar los grupos de módulos sin código |
| F | La interfaz se ve sin estilos tras el login | Dump sin filestore + disco del build lleno; un archivo de 0 bytes con el sha del paquete bloquea su regeneración | Liberar disco, borrar adjuntos de *assets* sin archivo, apartar el archivo vacío |

Orden que funcionó: A, B, C, D, E y G, H antes de instalar o actualizar el
stack destino. F solo si aparece el síntoma.

## Impuestos con fórmula Python

En el contexto declarado, los impuestos IIBB que fallaban eran **impuestos
nativos** del plan de cuentas a los que un módulo propio les había cambiado el
tipo a Python. Antes de rediseñarlos, verifique si la lógica se usaba: aquí la
tabla de alícuotas por cliente y el padrón estaban vacíos. La propuesta
(pendiente de validación contable) es devolverles el tipo nativo.

## Pagos agrupados

Sin conversión, los grupos de pago de 17 quedan en su tabla. En el caso
observado, los pagos ya tenían talonario y estaban conciliados, y la mayoría
de los grupos tenía un solo pago. La propuesta de conversión no está
verificada; ver [errores conocidos](known-errors.md).

## Comprobaciones que hicimos

- Conteos de asientos, pagos, cheques y remitos antes y después: iguales.
- Debe = haber de los asientos publicados.
- Apertura de vistas y lectura de registros de modelos clave.
- Reportes contables principales y PDF de factura, recibo y remito.

## Límites

- No hay base de Producción probada todavía.
- La conversión de datos de pagos, cheques y remitos está pendiente.
- Repetir sobre un dump **con filestore** puede cambiar los resultados de F.

Vea el [procedimiento](procedure.md), los [errores conocidos](known-errors.md)
y la [lista de validación](validation.md).

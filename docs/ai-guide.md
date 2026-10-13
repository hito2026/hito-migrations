# Guía de trabajo con IA

Use la IA para estructurar evidencias y proponer trabajo acotado, no para autorizar migraciones.
Consulte el [índice](index.md) para las etiquetas de evidencia y el [manual](migration-manual.md)
para los criterios de planificación. Estos esquemas no demuestran ningún procedimiento de migración.

## Antes de trabajar

1. Confirme la tarea aprobada por una persona, los archivos permitidos y el público destinatario.
2. Registre las versiones exactas de origen y destino y el alcance de código y base de datos.
3. Identifique las fuentes públicas autorizadas y los supuestos pendientes de resolver.
4. Acuerde las evidencias de aceptación, las condiciones de parada y las responsabilidades de recuperación.

## Privacidad y autoridad

- No acceda a material de clientes en directorios vecinos ni a otras fuentes no aprobadas.
- Nunca copie secretos, datos personales, código propietario ni identificadores de infraestructura.
- Anonimizar un material no otorga permiso para publicarlo.
- No ejecute operaciones sobre bases de datos, migraciones ni comandos destructivos sin aprobación.
- No cree commits ni configure repositorios remotos, no suba cambios, no despliegue ni publique sin aprobación explícita.
- Deje las decisiones de licencia y titularidad en manos del propietario.

## Resultados basados en evidencias

Marque las propuestas como no verificadas. Separe las afirmaciones de fuentes públicas,
las observaciones y las hipótesis. Registre resultados reales de comandos; no invente pruebas,
registros ni éxitos. Compilar la documentación solo valida el sitio, no una migración de código
o base de datos. Deténgase y consulte a la persona responsable si hay dudas sobre el alcance,
la autoridad, la privacidad o la recuperación.

## Entrega del trabajo

Informe los archivos modificados, las comprobaciones realizadas, los riesgos pendientes
y la siguiente decisión humana. Use la [lista de validación](validation.md) para la aceptación
y la [plantilla de caso](case-template.md) para un resumen autorizado y sin datos sensibles.

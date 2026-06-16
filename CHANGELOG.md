# Histórico de cambios

Este repositorio actúa como **repositorio base** (documentación, gobernanza, enlaces y distribuciones) de las extensiones personalizadas de [datos.gob.es](https://datos.gob.es/)

>[!NOTE]
> El histórico previo (2017–2022) corresponde a publicaciones donde el repositorio agrupaba código (CKAN/Drupal) y documentación.

## 

## [2.2.0] - 2026-06
### Added Drupal
- Módulo custom dge_custom_scheduler para la gestión programada de contenidos.
- Librería js para la generación de gráficos dinámicos.
- Vista 'Temas de actualidad' en la home y en la landing de sectores.
- Lógica de acciones sobre comentarios por js.

### Changed Drupal
- Estilos en diferentes secciones y vistas del portal.
- Gestión y visualización de comentarios para usuarios con permisos.
- Comportamiento del mosaico de sectores.
- Vista de aplicaciones con plataformas añadidas.
- Comportamiento de nombre público en comentarios.  
- Icono favicon.
- Visualización usuario logado.
- Control de errores en formalario de registro.
- Adaptación de numeración en elementos "li" al tamaño del header.
- Comportamiento del formulario de 2FA.
- Traducción de literales.

### Added Ckan
- Logo AENOR el de "Compromiso de la IA Responsable".
- Iconos.
- Cookies
- Formulario de datos de DCAT-AP-ES conjunto de datos.
- Formulario de datos de DCAT-AP-ES servicio de datos.
- Proceso de enlaces rotos, paralelizado por organismos.

### Changed Ckan
- Estilos en diferentes secciones y vistas del portal.
- Gestión y lógica de integración de logos en el footer.
- Información de interés en el footer.
- Comportamiento de nombre público en comentarios.
- Visualización usuario logado.
- Traducción de literales.
- Adaptación a la versión 2.9.14 de ckan.
- Correcciones y actualizaciónes en el proceso de federación.
- Ordenación de organismos alfabéticamente en vista de catálogo.
- Ficheros SHACL.
- Eliminación de funcionalidad 'Y/O' en el Catálogo de datos.
- Vista de formulario de federación.

## [2.1.0] - 2026-03
### Added Drupal
- Módulo custom dge_audit_log_prune para eliminación automática de registros a partir de una fecha dada.
- Módulo custom dge_custom_ckeditor_defaults para el manejo de opciones de tabla en CKEditor.
- Módulos custom para la gestión y tratamiento de los diferentes tipos políticas de cookies.  
- Gestión de caducidad del proceso de doble factor de autenticación y nuevos mensajes al usuario.
- Vista para un nodo de iniciativas.

### Changed Drupal
- Estilos en diferentes secciones y vistas del portal.
- Página de mantenimiento.
- Añadir opciones de bloqueo de comentarios en varios tipos de contenido.
- Información enviada al Datalayer en distintos idiomas.
- Traducción de literales.
- Notificaciones de correos.

### Added Ckan
- Icono de Spotify.
- Texto en buscador Ckan.
- Metatags.

### Changed Ckan
- Correcciones de ficheros de descarga.
- Estilos en diferentes secciones y vistas del portal.
- Logos.
- Ficheros SHACL conforme al repositorio DCAT-AP-ES.
- Traducción de literales.
- Mensajes de reporte de federaciones.
- Correcciones en la visualización de comentarios.
- Modificaciones en eventos GA.
- Permisos para comentarios.

## [2.0.0] - 2026-01
### Added
- Nueva estructura de repositorio base (documentación + enlaces a componentes).
- Documentación en `docs/`.
- Información de distribuciones en `distributions/`.
- Catálogo de repositorios por componente en `repositories/` (CKAN / Drupal).

### Changed
- Publicación del proyecto en **modelo descentralizado**: el código vive en repositorios independientes (extensiones CKAN y repos Drupal de módulos/temas).

## [1.0.0] - 2022-06
### Changed
- Actualización del código de datos.gob.es (última publicación de 2022 / cierre del ciclo v1).

## [0.2.0] - 2019-02
### Added
- Incorporación de ficheros (carga inicial de contenidos adicionales respecto a la publicación original).

## [0.1.0] - 2017-12
### Added
- Publicación inicial del código creado y/o modificado para su uso en datos.gob.es.
- Inclusión de extensiones CKAN y módulos/features/tema Drupal utilizados en el portal.

[2.1.0]: https://github.com/datosgobes/datos.gob.es/releases/tag/v2.1.0
[2.0.0]: https://github.com/datosgobes/datos.gob.es/releases/tag/v2
[1.0.0]: https://github.com/datosgobes/datos.gob.es/releases/tag/v1

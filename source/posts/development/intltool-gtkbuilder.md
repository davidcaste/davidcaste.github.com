Title: Extraer cadenas de un fichero .ui de gtk-builder con intltool
Category: desarrollo
Tags: gtk, autotools, intltool
Lang: es

Tenemos entre manos un proyecto en el que utilizamos Glade para la creación de
la interfaz de usuario; es muy cómodo porque crea una serie de ficheros XML que
describen la UI del programa, en lugar de crearla programáticamente. Hasta ahora
usábamos `libglade` para cargar estos ficheros, pero como esta librería [está
deprecada desde el año 2009][1], estamos trabajando en reemplazarla con
`gtk-builder` del proyecto GTK.

Es un proceso aburrido y tedioso más que difícil, pero nos hemos encontrado con
un pequeño problema. Estamos usando Autotools en el proyecto, e `intltool` no
es capaz de extraer cadenas de los ficheros con extensión `.ui` de
`gtk-builder`.

La solución para este problema es sencilla y la encontramos en un documento
llamado [GNOME Goal: Use GtkBuilder instead of libglade][2]. Consiste en
indicar a `intltool` que estos ficheros son de tipo `gettext/glade`. Basta con
editar el fichero `POTFILES.in` y añadir un prefijo a cada una de las líneas
donde aparezca un fichero `.ui` de la siguiente manera:

~~~
[type: gettext/glade]data/preferences.ui
~~~

[1]: http://mail.gnome.org/archives/devel-announce-list/2009-May/msg00003.html
[2]: http://live.gnome.org/GnomeGoals/RemoveLibGladeUseGtkBuilder

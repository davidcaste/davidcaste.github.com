Title: Solucionar cuelgue de Eclipse en Ubuntu 13.04 al mostrar una sugerencia de autocompletado
Date: 2013-05-21
Category: desarrollo
Tags: eclipse, linux, ubuntu, wtf
Lang: es

Para lo bueno y para lo malo Eclipse no deja de sorprenderme, y la última
sorpresa no ha sido agradable. En Ubuntu 13.04 de 64 bits, Eclipse 4.2 se
cuelga justo después de mostrar cualquier sugerencia de autocompletado de
código.

El error está reportado en Eclipse ([#406763][1]) y en Ubuntu
([#988646][2]), pero en ninguno de estos sitios se describe un *workarond*.
Afortunadamente encontré una solución (para variar) en un artículo de
Stackoverflow titulado [Why does my Eclipse Indigo crashes on Ubuntu 13.04 with
Oracle JDK 64bit?][3].

Este *workaround* consiste simplemente en añadir al final del fichero
`eclipse.ini` la siguiente línea:

    ::text
    -Dorg.eclipse.swt.browser.DefaultType=mozilla

[1]: https://bugs.eclipse.org/bugs/show_bug.cgi?id=406736
[2]: https://bugs.launchpad.net/ubuntu/+source/eclipse/+bug/988646
[3]: http://stackoverflow.com/questions/16383992/why-does-my-eclipse-indigo-crashes-on-ubuntu-13-04-with-oracle-jdk-64bit


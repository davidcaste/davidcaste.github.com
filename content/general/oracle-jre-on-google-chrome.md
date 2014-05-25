Title: Oracle JDK y Google Chrome en Ubuntu 12.04 LTS 
Date: 2012-04-30
Category: general
Tags: java, ubuntu, alternatives

A menudo utilizo *Juniper Network Connect* para conectar a la intranet
corporativa del trabajo. Es un applet de Java que, al menos en mi caso, no
funciona bien con [OpenJDK][1] y sólo funciona con [Oracle JVM][2] (la
anteriormente conocida como Sun JVM). En agosto del 2011, [Canonical dejó de
tener permiso para distribuir la JVM de Sun][3]. Aunque existen algunos PPAs
mantenidos por miembros de la comunidad de Ubuntu que ofrecen paquetes DEB del
Oracle JVM, suelen ser versiones demasiado antiguas y con problemas de
seguridad.

Aunque hay disponible un instalador oficial en la [sección de descargas de
Oracle para Java][4], suele ser mejor opción utilizar el script `make-jpkg`
para crear un paquete Debian. Este script está empaquetado para Debian en el
paquete [java-package][5], y recientemente ha sido actualizado a la versión
0.50 que tiene como novedad el soporte para Java 7.

Sólo he encontrado un problema con estos paquetes, y es que no instalan el
plugin de Java en el navegador Google Chrome, sin embargo si lo hace para
Iceweasel y Chromium. Es problema es muy sencillo de resolver, sólo es
necesario crear un enlace simbólico al fichero `libnpjp2.so` que se encuentra
en el JRE. Utilizando el [sistema de alternatives de Debian][6] se haría de la
siguiente manera:

    ::text
    $ sudo update-alternatives --install \
    > /usr/lib/mozilla/plugins/libjavaplugin.so \
    > mozilla-javaplugin.so \
    > /usr/lib/jvm/j2sdk1.6-oracle/jre/lib/i386/libnpjp2.so 100

[1]: http://openjdk.java.net
[2]: http://www.java.com
[3]: https://lists.ubuntu.com/archives/ubuntu-security-announce/2011-December/001528.html
[4]: http://www.oracle.com/technetwork/java/javase/downloads/index.html
[5]: http://packages.debian.org/java-package
[6]: http://www.debian-administration.org/articles/91

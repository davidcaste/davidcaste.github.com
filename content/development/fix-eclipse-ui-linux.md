Title: Solucionar problemas gráficos en Eclipse bajo GNU/Linux
Date: 2012-08-1
Category: desarrollo
Tags: eclipse, linux, windowbuilder, android

Aunque [Eclipse][1] es una plataforma de desarrollo multiplataforma, no es un
secreto que MS Windows ha sido hasta ahora la plataforma mejor soportada.
La versión de Eclipse para Mac OS X ha ido mejorando versión a versión, sobre
todo desde la publicación de [Eclipse 4.2 (Juno)][2].

Aunque completamente funcional, el soporte de Eclipse para GNU/Linux no está a
la altura quei en el resto de plataformas. Un ejemplo es el bug [#368543][4],
en el que se describen problemas gráficos con [WindowBuilder][3] bajo
GNU/Linux. Estes mismos problemas los tiene el [plugin ADT][5] de Google (que
al fin y al cabo utiliza el mismo editor gráfico que WindowBuilder).

[Lars Vogel][5] propone un [workaround][6] a este problema, que consiste en
forzar a SWT a no utilizar [Cairo][7]. En mi caso, utilizo un script que
además desactiva las [overlay scrollbars][8] de Ubuntu, que tampoco parecen
terminar de funcionar bien en Eclipse:

    :::bash
    #!/usr/bin/env bash

    export GDK_NATIVE_WINDOWS=1
    export LIBOVERLAY_SCROLLBAR=0

    ECLIPSE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    $ECLIPSE_DIR/eclipse -Dorg.eclipse.swt.internal.gtk.cairoGraphics=false \
        -Dorg.eclipse.swt.internal.gtk.useCairo=false

[1]: http://www.eclipse.org
[2]: http://www.eclipse.org/juno
[3]: http://www.eclipse.org/windowbuilder/
[4]: https://bugs.eclipse.org/bugs/show_bug.cgi?id=368543
[5]: http://developer.android.com/tools/sdk/eclipse-adt.html
[5]: https://twitter.com/vogella/
[6]: https://bugs.eclipse.org/bugs/show_bug.cgi?id=368543#c17
[7]: http://cairographics.org/
[8]: https://launchpad.net/ayatana-scrollbar/


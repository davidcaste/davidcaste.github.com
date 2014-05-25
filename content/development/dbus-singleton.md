Title: Control de concurrencia usando D-Bus
Date: 2012-05-04
Category: desarrollo
Tags: python, dbus, concurrencia

Un problema frecuente es cómo impedir que un programa se ejecute dos o más
veces de forma concurrente. Uno de los mecanismos más utilizados para afrontar
este problema es el conocido como [file locking][1]. En un proyecto hemos
utilizado [D-Bus][2] para implementar un mecanismo similar.

D-Bus es un sistema de bus de mensajes, una forma sencilla para que las
aplicaciones se comuniquen entre sí. De forma muy resumida (más información en
la web del [proyecto D-Bus][3]), cuando un usuario inicia una sesión gráfica en
el sistema tiene a su disposición un bus del sistema y un bus del usuario
ligado a su sesión. Un programa en ejecución se puede registrar en uno de estos
buses para ofrecer uno o más servicios, identificados unívocamente con un
identificador asignado por D-Bus (p.e. `:34-907`) y un nombre *conocido*
elegido por el programa (p.e. `es.foo.Bar`).

Puesto que sólo puede haber un único servicio en un bus con el mismo nombre, es
sencillo idear un mecanismo de control de concurrencia. Consistiría básicamente
en consultar si existe un servicio en el bus de sesión con un determinado
nombre. Un ejemplo sencillo implementado en Python es el siguiente:

    ::python
    #!/usr/bin/env python
    # dbus-singleton-example.py

    import sys
    import gobject
    import dbus
    import dbus.mainloop.glib
    import dbus.service

    BUS_NAME = 'es.foo.Bar'

    class DBusSingleton(dbus.service.Object):
        def __init__(self):
            bus = dbus.SessionBus()
            if not bus.name_has_owner(BUS_NAME):
                bus.request_name(BUS_NAME)
                dbus.service.Object.__init__(self, bus, '/es/foo/bar')
                print 'Adquired D-Bus name: "%s"' % BUS_NAME
            else:
                print 'Failed to request D-Bus name: "%s"' % BUS_NAME
                sys.exit()

    if __name__ == '__main__':
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        singleton = DBusSingleton()

        loop = gobject.MainLoop()
        loop.run()

Al ejecutarlo de forma concurrente *n* veces se obtiene la salida:

    ::bash
    $ for i in {1..5}; do python dbus-concurrenty-example.py & done
    Adquired D-Bus name: "es.foo.Bar"
    Failed to request D-Bus name: "es.foo.Bar"
    Failed to request D-Bus name: "es.foo.Bar"
    Failed to request D-Bus name: "es.foo.Bar"
    Failed to request D-Bus name: "es.foo.Bar"


[1]: http://en.wikipedia.org/wiki/File_locking
[2]: http://en.wikipedia.org/wiki/DBus
[3]: http://www.freedesktop.org/wiki/Software/dbus

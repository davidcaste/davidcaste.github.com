Title: Monitorizar una red privada desde un Nagios público con NRPE
Date: 2014-06-27
Modified: 2015-05-13
Category: sysadmin
Tags: nagios, firewall, ubuntu

Hace apenas un par de semanas he cambiado de trabajo, y uno de los primeros problemas que he tenido que resolver estaba relacionado con [Nagios](http://www.nagios.org/). Ocurre que tenemos unas máquinas en una red privada, y un servidor Nagios corporativo que no puede acceder a ellas.

Nagios es una herramienta de monitorización de redes y sistemas de código abierto. Es extremadamente popular, y desde su origen en 1999 se usa en multitud de sistemas. Por lo general se compone de un servidor que realiza tests y recopila sus resultados, [agentes](http://exchange.nagios.org/directory/Addons/Monitoring-Agents) que tienen la capacidad de realizar tests, y de *plugins*. Estos plugins son pequeños programas que se pueden utilizar para ejecutar pruebas locales, pruebas remotas, o para realizar tareas auxiliares que asistan a los dos usos anteriores.

La principal característica de Nagios es la cantidad de recursos y plugins existenes. Algunos ejemplos de repositorios de plugins son [Nagios Exchange](http://exchange.nagios.org), [Nagios Plugins](http://nagios-plugins.org/), [The Monitoring Plugins Project](https://www.monitoring-plugins.org/), etc. El blog de [El Despistado](http://www.eldespistado.com/) trata casi en exclusiva sobre Nagios y tiene publicados multitud de artículos de interés.

En esta entrada voy a repasar la solución que hemos adoptado. El sistema operativo de los equipos que he utilizado es Ubuntu 12.04, aunque posiblemente la configuración del entorno sea exactamente la misma (o al menos muy parecida) en Ubuntu 14.04.


### Problemática

El servidor Nagios (en adelante Nagios a secas) no es capaz de llegar a un conjunto de hosts que se encuentran en una red privada. Después de investigar, encontramos dos posibles soluciones:

* Realizar chequeos pasivos utilizando [NSCA](http://exchange.nagios.org/directory/Addons/Passive-Checks/NSCA--2D-Nagios-Service-Check-Acceptor/details) (*Nagios Service Check Acceptor*). La iniciativa de la comunicación la toman los hosts, y estos si que pueden llegar al Nagios porque salen a través de un NAT. Esta aproximación requiere la instalación de un servidor NSCA en el Nagios, y de un cliente NSCA en cada uno de los hosts.
* Utilizar [NRPE](http://exchange.nagios.org/directory/Addons/Monitoring-Agents/NRPE--2D-Nagios-Remote-Plugin-Executor/details) (*Nagios Remote Plugin Executor*) para montar un escenario muy parecido al descrito en [Multiple Indirected Service Checks](http://nagios.sourceforge.net/docs/3_0/indirectchecks.html). NRPE es un agente de Nagios que permite la monitorización mediante plugins que se encuentran instalados en los sistemas remotos. Se compone de un plugin NRPE que se debe instalar en el Nagios, y de un servidor NRPE en cada uno de los hosts.

Como resulta que el Nagios es corporativo, y que ya tenían el plugin NRPE instalado, se eligió esta última opción.

### Descripción del escenario

Nuestro escenario consiste básicamente en que hay un host que está detrás del firewall y que tiene acceso al resto de elementos que queremos monitorizar. El servidor Nagios se conecta a él, y éste a su vez se conectará al resto de elementos de la red:

<div class="figure">
    <img alt="{filename}/images/indirectsvccheck2.png" src="{filename}/images/indirectsvccheck2.png" />
</div>

Tendremos por tanto los siguientes elementos:

1. Un *servidor* en el que estará instalado Nagios, y el plugin de NRPE.
2. Una *máquina de salto* en la que estarán instalados el servidor NRPE, el plugin NRPE, y posiblemente otros plugins de Nagios.
3. Un conjunto de *hosts* a monitorizar, en los que se instalarán un servidor NRPE en cada uno de ellos, y un cojunto de plugins de Nagios.

#### Configuración de los hosts

En los hosts es necesario instalar el servidor NRPE:

    ::text
    sudo apt-get install nagios-nrpe-server nagios-plugins

Los comandos que van a ser invocados por el servidor NRPE se configuran en el archivo `/etc/nagios/nrpe.cfg`, como por ejemplo:

    ::text
    command[check_users]=/usr/lib/nagios/plugins/check_users -w 5 -c 10
    command[check_load]=/usr/lib/nagios/plugins/check_load -w 15,10,5 -c 30,25,20

Como medida de seguridad, se puede añadir la IP de la máquina de salto en la variable `allowed_hosts` del archivo `/etc/nagios/nrpe.cfg`:

    ::text
    allowed_hosts=192.168.60.10

La documentación de NRPE informa que esta opción se ignora si NPRE se ejecuta bajo `inetd` o `xinetd`, y que en los casos que se aplica las comprobaciones que realiza son bastante rudimentarias. Por estas razones es bastante común combinar esta variable con comprobaciones adicionales en los archivos `/etc/hosts.allow` y `/etc/hosts.deny`. 

No hay que olvidar reiniciar el servicio `nagios-nrpe-server` después de modificar la configuración:

    ::text
    sudo service nagios-nrpe-server restart


#### Configuración de la máquina de salto

En la máquina de salto se deben instalar el servidor NRPE y el plugin NRPE de Nagios:

    ::text
    sudo apt-get install nagios-nrpe-server nagios-plugins

Hay que prestar atención a la hora de instalar el paquete `nagios-nrpe-plugin` porque "recomienda" el paquete `nagios3`, y en Ubuntu los paquetes recomendados se instalan automáticamente. Como no necesitamos instalar Nagios en la máquina de salto, le debemos pasar el flag `--no-install-recommends` a `apt-get`:

    ::text
    sudo apt-get install --no-install-recommends nagios-nrpe-plugin

El paquete `nagios-nrpe-plugin` proporciona el binario `check_nrpe` en la ruta `/usr/lib/nagios/plugins`. Este binario es en realidad un cliente que utilizaremos para ordenar la ejecución de tests en un host remoto que tenga instalado un servidor NRPE.

Es recomendable ejecutar primero el binario `check_nrpe` para depurar la configuración, y comprobar que la comunicación entre los hosts es correcta:

    ::text
    /usr/lib/nagios/plugins/check_nrpe -H 192.168.60.11 -c check_users
    USERS OK - 1 users currently logged in |users=1;5;10;0

Una vez se ha comprobado que la comunicación entre la máquina de salto y los hosts es correcta, se añadirá un nuevo test *dummy* llamado `check_remote_check` en el servidor NRPE de la máquina de salto. La misión de este test es ordenar la ejecución de un test en un host remoto y recoger el resultado. Este nuevo test se definirá al igual que antes en el archivo  `/etc/nagios/nrpe.cfg`:

    ::text
    command[check_remote_check]=/usr/lib/nagios/plugins/check_nrpe -H $ARG1$ -c $ARG2$

Este test toma dos parámetros:

* `$ARG1$` es el host remoto.
* `$ARG2$` es el test que se desea ejecutar.

En Ubuntu, el servidor NRPE no permite por defecto el paso de parámetros a los tests porque es un riesgo de seguridad. Para habilitar esta funcionalidad se debe modificar el fichero `/etc/nagios/nrpe.cfg` y habilitar la opción `dont_blame_nrpe`:

    ::text
    dont_blame_nrpe=1

Una alternativa a habilitar los parámetros sería que en lugar de crear un comando genérico como `check_remote_check`, añadir comandos específicos para cada host como:

    ::text
    command[check_remote_users_host1]=/usr/lib/nagios/plugins/check_nrpe -H 192.168.60.11 -c check_users

Aunque posiblemente más segura, esta aproximación tiene la desventaja de que habría que crear un comando para cada uno de los tests de cada uno de los hosts que se quisieran monitorizar.

Al igual que en el caso anterior, es aconsejable configurar la variable `allowed_hosts` para que sólo figure la IP del servidor Nagios. 

No hay que olvidar reiniciar el servicio `nagios-nrpe-server` después de modificar la configuración:

    ::text
    sudo service nagios-nrpe-server restart


#### Configuración servidor Nagios

Además de Nagios, en el servidor se debe instalar el plugin NRPE:

    ::text
    sudo apt-get install nagios-nrpe-plugin

Si la configuración de la máquina de salto y de los hosts es correcta, el binario `check_nrpe` debería poder ejecutar el test `check_remote_check` en la máquina de salto:

    ::text
    /usr/lib/nagios/plugins/check_nrpe -H 192.168.50.5 -c check_remote_check -a 192.168.60.11 check_users
    USERS OK - 1 users currently logged in |users=1;5;10;0

Por ejemplo, se pueden definir un conjunto de test que usen `check_remote_check` de la máquina de salto de la siguiente manera:

    ::text
    define host {
        use                 generic-host
        host_name           jumpbox
        alias               JumpBox
        address             192.168.50.5
    }

    define host {
        use                 generic-host
        host_name           host1
        alias               Host1
        address             192.168.50.5  
    }

    define service {
        use                 generic-service
        host_name           jumpbox
        service_description JumpBox_PING
        check_command       check_ping!100.0,20%!500.0,60%
    }

    define service {
        use                 generic-service
        host_name           host1
        service_description host1_System_Load_With_Params
        check_command       check_nrpe_3args!check_remote_check!192.168.60.11!check_load
    }

    define service {
        use                 generic-service
        host_name           host1
        service_description host1_System_Load_Without_Params
        check_command       check_nrpe_1arg!check_remote_load_host1
    }

Hay que prestar atención a los siguientes detalles:

* Cuando se definan los hosts que no están directamente accesibles en Internet, el campo `address` debe tener la dirección IP de la máquina de salto. De esta forma, cuando Nagios vaya a ejecutar los tests de `host1` realmente se ejecutarán en la máquina `jumpbox`.
* El test *host1_System_Load_With_Params* utiliza el comando `check_remote_check` que hemos definido anteriormente en la máquina de salto.
* El test *host1_System_Load_Without_Params* utiliza el comando `check_remote_load_host1` para ejecutar un test sin que haya un paso de parámetros del Nagios a la máquina de salto.
* Se utilizan los comandos `check_nrpe_1arg` y `check_nrpe_3args` que respectivan invocan a `check_nrpe` tomando uno y tres argumentos.

A diferencia de la distribución estándar de Nagios, Ubuntu (o mas bien Debian) fragmenta la definición de los comandos en múltiples ficheros que se encuentran en `/etc/nagios-plugins/config/`. En el caso de NRPE, utiliza el archivo `check_nrpe.cfg`. En mi caso tuve que añadir la definición del comando `check_nrpe_3args` para invocar a `check_nrpe` con 3 argumentos:

    ::text
    # this command runs a program $ARG1$ with arguments $ARG2$
    define command {
        command_name    check_nrpe
        command_line    /usr/lib/nagios/plugins/check_nrpe -H $HOSTADDRESS$ -c $ARG1$ -a $ARG2$
    }

    # this command runs a program $ARG1$ with no arguments
    define command {
        command_name    check_nrpe_1arg
        command_line    /usr/lib/nagios/plugins/check_nrpe -H $HOSTADDRESS$ -c $ARG1$
    }

    # this command runs a program $ARG1$ with arguments $ARG2$ and $ARG3$
    define command {
        command_name    check_nrpe_3args
        command_line    /usr/lib/nagios/plugins/check_nrpe -H $HOSTADDRESS$ -c $ARG1$ -a $ARG2$ $ARG3$
    }

No hay que olvidar reiniciar el servicio `nagios3` después de modificar la configuración:

    ::text
    sudo service nagios3 restart


#### Problemas

Más que problemas, esta aproximación introduce las siguientes *molestias*:

1. Nagios realiza *pings* periódicos a todos los hosts definidos en su configuración. Según el resultado de este test explícito, Nagios determina si un host está *UP* o *DOWN*. Como en la definición de las máquinas que están en la red interna se ha utilizado la dirección IP de la máquina de salto, el resultado de este test será falso porque quien en realidad estará contestando los pings es la máquina de salto.
2. La monitorización de gran parte de la infraestructura depende exclusivamente de la máquina de salto. Como esta máquina se desconecte o se caiga nos llegarán miles de alertas, aún cuando el resto de la infraestructura esté operativa.

### Conclusiones

Se ha presentado una posible solución para el problema de monitorizar una red privada desde un servidor Nagios que no tiene acceso directo a los elementos de red. Es posible que la solución óptima en estos casos sea que las propias máquinas envíen sus resultados al servidor Nagios, pero cuando esto no sea posible la propuesta presentada puede ser de utilidad.

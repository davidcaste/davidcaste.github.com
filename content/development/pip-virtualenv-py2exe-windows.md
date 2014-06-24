Title: Instalar py2exe en un virtualenv con Python 2.7
Date: 2014-06-02
Category: desarrollo
Tags: python, pip, virtualenv, py2exe

Para distribuir un programa Python en Windows la opción más sencilla suele ser empaquetar la aplicación en un único fichero binario, y que los usuarios ejecuten el fichero `.exe` resultante. Existen varias alternativas para construir estos ficheros binarios, como p.e. [py2exe][3] y [cx_freeze][4]. Como parece que [cx_freeze no se integra bien con virtualenv][5], terminé eligiendo `py2exe`.

La forma más sencilla de instalar Python, `pip` y `virtualenv` en Windows es seguir las instrucciones de la sección [Installing Python on Windows][6] y [Virtual Environments][7] de [Python Guide][8].

Sin embargo, si usamos Python 2.7 no podemos instalar `py2exe` con `pip` debido a que la última versión (a día de hoy `0.9.2.0`) de `py2exe` sólo funciona con Python 3.3 o posterior. La versión `0.6.9` es la última que funciona con Python 2.7, pero no podemos instalarla con `pip` porque el enlace en [PyPI][10] es erróneo.

La [única solución][9] es descargar el instalador `py2exe-0.6.9.win32-py2.7.exe` que podemos encontrar en el [área de descargas][11] del proyecto en SourceForge, y usar `easy_install` para instalarlo dentro del `virtualenv`:

    :::console
    (env) c:\Users\dcastellanos\Documents\workspace\FooExample>easy_install C:\Users\dcastellanos\Downloads\py2exe-0.6.9.win32-py2.7.exe
    Processing py2exe-0.6.9.win32-py2.7.exe
    zipextimporter: module references __file__
    py2exe.boot_service: module references __file__
    py2exe.build_exe: module references __file__
    py2exe.build_exe: module references __path__
    py2exe.mf: module references __file__
    py2exe.mf: module references __path__
    py2exe.samples.pywin32.isapi.setup: module references __path__
    creating 'c:\users\dcaste~1\appdata\local\temp\easy_install-qlkqlz\py2exe-0.6.9-py2.7-win32.egg' and adding 'c:\users\dcaste~1\appdata\local\temp\easy_install-qlkqlz\py2exe-0.6.9-py2.7-win32.egg.tmp' to it
    creating c:\users\dcastellanos\documents\workspace\fooexample\env\lib\site-packages\py2exe-0.6.9-py2.7-win32.egg
    Extracting py2exe-0.6.9-py2.7-win32.egg to c:\users\dcastellanos\documents\workspace\fooexample\env\lib\site-packages
    Adding py2exe 0.6.9 to easy-install.pth file
    Installing py2exe_postinstall.py script to c:\Users\dcastellanos\Documents\workspace\FooExample\env\Scripts
    Installing py2exe_postinstall.pyc script to c:\Users\dcastellanos\Documents\workspace\FooExample\env\Scripts

    Installed c:\users\dcastellanos\documents\workspace\fooexample\env\lib\site-packages\py2exe-0.6.9-py2.7-win32.egg
    Processing dependencies for py2exe==0.6.9
    Finished processing dependencies for py2exe==0.6.9

    (env) c:\Users\dcastellanos\Documents\workspace\FooExample>

Una vez completada la instalación podemos seguir los pasos del [tutorial de py2exe][12], u otro de los otros muchos (como [1][13] y [2][14]) que podemos encontrar en Internet.

[1]: https://pypi.python.org/pypi/virtualenv
[2]: https://pypi.python.org/pypi/pip
[3]: http://www.py2exe.org/
[4]: http://cx-freeze.sourceforge.net/
[5]: https://www.google.es/#q=cx_freeze+virtualenv
[6]: http://docs.python-guide.org/en/latest/starting/install/win/
[7]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
[8]: http://docs.python-guide.org
[9]: https://pypi.python.org/pypi/py2exe/0.6.9
[10]: http://stackoverflow.com/questions/11288923/cannot-install-py2exe-with-python-2-7
[11]: http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/
[12]: http://www.py2exe.org/index.cgi/Tutorial
[13]: http://www.pythoncentral.io/py2exe-python-to-exe-introduction/
[14]: http://yasoob.github.io/beta/using-py2exe-the-right-way

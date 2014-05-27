Title: Blog lowcost con GitHub y Pelican
Date: 2014-05-27
Category: general
Tags: github, python, pelican
<!--
Status: draft
-->

Gracias a [GitHub Pages][1] y un generador estático de contenido como [Pelican][2] es muy fácil montar un blog *lowcost*. Un humilde ejemplo es este blog, pero hasta hace poco no había conseguido una configuración que mereciera la pena compartir.

### GitHub Pages

En general, el comportamiento de GitHub Pages es muy sencillo. Prácticamente consiste en crear un repositorio `git`, realizar un commit con documentos HTML, y unos minutos después este contenido será accesible en una URL.

GitHub Pages ofrece dos modalidades de servicio: páginas para desarrolladores u organizaciones, y páginas para proyectos. Dependiendo de la modalidad que estemos usando varía la forma en la que se monta el sitio:

-   En la modalidad para desarrolladores u organizaciones, se debe crear un repositorio llamado *usuario*.github.io, donde *usuario* es el nombre del usuario o de la organización en GitHub. La página (o páginas) HTML que se deseen servir se deben añadir directamente en la rama `master`, y no importa lo que haya en el resto de ramas. Este contenido es accesible desde la URL **http://_usuario_.github.io**.
-   En la modalidad para proyectos, no es necesario crear nuevos repositorios. En el repositorio del proyecto se debe crear una rama llamada `gh-pages`, y añadir ahí el contenido HTML. Este contenido será accesible desde la URL **http://_usuario_.github.io/_repository_**.

Aunque puede parecer un lío la gestión de estas ramas, afortunadamente existe una herramienta llamada [ghp-import][3] que facilita en gran manera estas operaciones.

### Pelican

Pelican es un generador estático de contenido, al estilo de [Jekyll][4]. Por si fuera necesario, en [Static Site Generators][5] hay una recopilación de proyectos similares.

Además de la [documentación][6] del proyecto, hay multitud de páginas con instrucciones para configurar Pelican (por ejemplo [aquí][7] y [aquí][8]). Además el comando `pelican-quickstart` es de ayuda para crear rápidamente una configuración básica de un blog.

### Usar Pelican en GitHub Pages para desarrolladores

En mi caso, elegí utilizar GitHub Pages en su modalidad para desarrolladores. Para ello, hice lo siguiente:

1. Crear un repositorio llamado [davidcaste.github.io][9], y clonarlo en mi ordenador:

    ```
    git clone https://github.com/davidcaste/davidcaste.github.io
    ```

2. En el repositorio local, crear una rama llamada `source`, y cambiar a ella:

    ```
    git checkout -b source
    ```

3. Crear una configuración básica con `pelican-quickstart` y seguir las instrucciones.
 
Llegados a este punto, contamos con una configuración Pelican funcional. La [documentación de Pelican][10] nos explica (entre otras muchas cosas) cómo crear contenidos y generar el contenido estático a partir de ellos.

Según la configuración por defecto, las páginas generadas se almacenarán en el directorio `output`. Este directorio **no** es necesario añadirlo al repositorio, y lo ideal es añadir las siguientes líneas al fichero `.gitignore`:

    output
    pelican.pid
    srv.pid

Como se comentó anteriormente, GitHub Pages para desarrolladores va a servir el contenido HTML que se encuentre en la rama `master` del repositorio. Podríamos copiar el contenido del directorio `ouput` a algún sitio, cambiar a la rama `master` y añadir el contenido anteriores. Es factible, pero sin duda que es un procedimiento muy tedioso.

El script `ghp-import` nos permite evitar los pasos anteriores. Con ejecutar ```ghp-import -b master output``` él sólo va a realizar un commit en `master` con los contenidos del directorio `output`. Sólo nos quedaría subir los cambios de vuelta a GitHub con el comando ```git push origin master```.

El proceso se puede automatizar aún más modificando el fichero `Makefile` que genera `pelican-quickstart`; en lugar de que el objetivo `github` invoque a `ghp-import` sobre la rama `gh-pages`, nos interesa que se invoque sobre la rama `master`:

```
github: publish
    ghp-import -b master $(OUTPUTDIR)
    git push origin master
```

### Conclusiones

La tupla GitHub Pages y un generador estático de contenido como Pelican permiten crear fácilmente páginas y blogs que requieren un esfuerzo de mantenimiento cercano a cero. Pelican en particular ofrece una serie de scripts y facilidades que automatizan las operaciones más tediosas.

En definitiva, la posibilidad de poder usar las mismas herramientas que las usadas durante el desarrollo de software, hacen de GitHub Pages junto con Pelican ofrece una alternativa muy a tener en cuenta con respecto a otras plataformas de blogs tradicionales como [WordPress][11] o [Blogger][12].

[1]: https://pages.github.com/
[2]: http://blog.getpelican.com/
[3]: https://github.com/davisp/ghp-import/
[4]: http://jekyllrb.com/
[5]: http://staticsitegenerators.net/
[6]: http://docs.getpelican.com
[7]: http://www.circuidipity.com/github-pages.html
[8]: http://mathamy.com/migrating-to-github-pages-using-pelican.html
[9]: https://github.com/davidcaste/davidcaste.github.io
[10]: http://docs.getpelican.com/en/3.3.0/getting_started.html#basic-usage
[11]: http://es.wordpress.com/
[12]: https://www.blogger.com
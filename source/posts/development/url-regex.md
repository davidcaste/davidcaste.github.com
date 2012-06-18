Title: (Otra) expresión regular para extraer URLs
Date: 2012-06-18
Category: desarrollo
Tags: regex, web, python
Lang: es

Escribir una expresión regular que extraiga URLs de un texto arbitrario no es
una tarea sencilla, la prueba es que existen en Internet literalmente cientos
de aproximaciones que abordan el problema con más o menos éxito.

Hay que tener en cuenta que [no es posible detectar _cualquier_
URL en un texto arbitrario][5], puesto que el espacio es un carácter admitido en
las URLs. Después de dedicar bastante tiempo a buscar en Internet, la
aproximación que más me gustó es la realizada por [John Gruber][1], creador de
[Markdown][2], en el artículo [An Improved Liberal, Accurate Regex Pattern for
Matching URLs][3]. Propone  una expresión regular muy interesante porque aborda
el problema de URLs con parejas de paréntesis, común en ciertos sitios como la
Wikipedia.  Aunque su expresión regular reconoce correctamente la inmensa
mayoría de URLs,
requiere que después del dominio superior (_Top Level Domain_, o TLD) de la URL
tenga una barra invertida después del dominio. Por ejemplo
[t.co/](http://t.co/) se reconoce correctamente, pero [t.co](http://t.co) no.

Afortunadamente Jesús González (Chuso), un compañero de Escritorio Movistar
para la plataforma Windows, había tenido el mismo problema y había escrito una
expresión regular que no tiene este problema:

    :::text
    # Capture entire matched URL
    (
        # Optional: only allow some network protocols
        # URL protocol and a colon followed by 2 slashes
        (?:
            (?:
                http|https|ftp
            ):\\/\\/
        )?

        # Check if it is the beginning of a word
        (?<=\\b)

        # The URL must not start with the character '@'
        (?<!\\@)

        # The domain name must begin with a valid character
        (?:[\w\d]

            # Other characters allowed in the domain
            (?:[\w\dñÑ()+,-.:=;$_!*'%?#])*
        )

        # A recognized domain is required
        \\.
        (?:
            aero|arpa|asia|biz|cat|com|coop|edu|gov|inet|info|int|jobs|mil|
            mobi|museum|name|net|org|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|
            al|am|an|ao|aq|ar|as|at|au|aw|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|
            bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|
            cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|
            fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|
            hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|
            km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|
            mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|
            ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|
            py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|
            st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|
            ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|za|zm|zw
        )

        # Optional: Port number
        (?::[0-9]+)?

        # Characters allowed in a URL according to RF1738
        (?:
            \\/[\w\d()+,-.:=@;$_!*'%?#&|\\\\]*
        )*

        # Check if we have consumed all characters allowed in a URL
        (?![\w\d()+,-./:=@;$_!*'%?#&|\\\\])
    )

Esta expresión debe compilarse con los flags `re.IGNORECASE` y `re.VERBOSE` del
[módulo re][6].

Además de detectar las URLs cortas del tipo [t.co](t.co), sólo hace
_matching_ si el TLD de la URL es válido. Sin embargo, tiene la desventaja de
que si en un futuro cambiara la [lista de dominios superiores][4], sería
necesario actualizar la expresión regular.

*[TLD]: Top Level Domain

[1]: http://daringfireball.net/
[2]: http://daringfireball.net/projects/markdown/
[3]: http://daringfireball.net/2010/07/improved_regex_for_matching_urls
[4]: http://en.wikipedia.org/wiki/List_of_Internet_top-level_domains
[5]: http://www.codinghorror.com/blog/2008/10/the-problem-with-urls.html
[6]: http://docs.python.org/library/re.html


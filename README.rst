PypiClient
==========

PyPiClient is a simple XML-RPC client for Pypi.

a small Python application that will do the following:

 * provide a XML-RPC client that knows how to list all releases of a given project at PyPI (no need to implement the whole XML-RPC spec, but think about this as something we can reuse later during the GSOC, to implement the whole XML-RPC spec)
 * provide a script called "install_distribution.py" that will be used to  download the distribution and install it, using "python setup.py install"

The CLI can be used like this::

  $ install_distribution.py Foo
  Found versions of Foo:
        1.1
        1.2
  Which version do you want to install (hit enter for None)?

or::

  $ install_distribution.py Foo 1.1 

There code of the lib is fully documented and tested. See the pypiclient module. 

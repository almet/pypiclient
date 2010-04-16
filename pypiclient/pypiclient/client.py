import xmlrpclib
import sys

from exceptions import ProjectDoesNotExist

PYPI_XML_RPC_URL = 'http://python.org/pypi'

class XmlRpcClient:
    """Lib to the XML/RPC PyPi Webservice.

    Provides some simple methods to interact with the Pypi repositories directly
    in python.
    """

    def __init__(self, server_url=None):
        """Construct the class.

        If no server_url is specified, use the default PyPi XML-RPC URL, defined
        in the PYPI_XML_RPC_URL constant::
            
            >>> client = Client()
            >>> client.server_url == PYPI_XML_RPC_URL
            True

            >>> client = Client("http://someurl/")
            >>> client.server_url
            'http://someurl/'

        """
        if server_url == None:
            server_url = PYPI_XML_RPC_URL

        self.server_url = server_url
    
    def _get_server_proxy(self):
        """Return the server proxy for the url specified in the constructor.

        If no server proxy is defined yet, creates a new one::

            >>> client = Client()
            >>> client._get_server_proxy()
            <ServerProxy for python.org/pypi>

        """
        if not hasattr(self, '_server_proxy'):
            self._server_proxy = xmlrpclib.ServerProxy(self.server_url)

        return self._server_proxy

    def get_project_versions(self, project_name, show_hidden=True):
        """Return the list of existing versions for a specific project::

            >>> client = Client()
            >>> client.get_project_versions('Foo')
            ["1.1", "1.2"]

        If no such project exists, raise a ProjectDoesNotExist exception.
        """
        server = self._get_server_proxy()
        versions = server.package_releases(project_name, show_hidden)
        if not versions:
            raise ProjectDoesNotExist(project_name)
        return versions

    def get_project_url(self, project_name, version=None, packagetype='sdist'):
        """Return the url of the specified project version::

            >>> client = Client()
            >>> client.get_project_url('gunicorn')

        If no version is specified, provides the last version url.
        As some projects do not specify a way to download an archive of their
        code, if it's the case, raise a ProjectDownloadUrlDoesNotExist
        exception.

        By default this return only the url for the first sdist package found.
        It's possible to specify another packagetype.
        """
        if version == None:
            version = self.get_project_versions(project_name, False)[0]
        server = self._get_server_proxy()
        urls = server.release_urls(project_name, version)
        url_infos = [url for url in urls if url['packagetype'] == packagetype][0]

        if not url_infos.has_key('url'):
            raise ProjectDownloadUrlDoesNotExist(project_name)

        return url_infos['url'] 

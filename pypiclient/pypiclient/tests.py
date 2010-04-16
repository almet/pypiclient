"""Tests for the PyPiClient module"""

import unittest
import client
import exceptions
import xmlrpclib
from mock import Mock

class TestXmlRpcClient(unittest.TestCase):
    """Tests for the XmlRpc Client.

    We just test here the lib behavior, and to not depend on the real pypi
    XmlRpc interface, the xmlrpclib module.
    """

    def setUp(self):
        """Initialize the XmlRpcClient.

        """
        self.client = client.XmlRpcClient()

    def _mock_xmlrpc_method(method_name, return_value):
        self.client._get_server_proxy = Mock()
        proxy = Mock(xmlrpclib.ServerProxy())
        method = getattr(proxy, method_name)
        method.return_value = return_value
        return method
    
    def test_init(self):
        c = XmlRpcClient()
        self.assertEqual(c.server_url, client.PYPI_XML_RPC_URL, 
            "when no server_url is defined, should use client.PYPI_XML_RPC_URL")

        c = XmlRpcClient('http://a/test/url')
        self.assertEqual(c.server_url, 'http://a/test/url')

    def test_get_server_proxy(self):
        """get_server_proxy should build once the server proxy and stock it into
        a object member.

        """
        self.assertFalse(hasattr(self.client, '_server_proxy'))
        proxy1 = self.client._get_server_proxy()
        self.assertTrue(hasattr(self.client, '_server_proxy'))
        proxy2 = self.client._get_server_proxy()
        self.assertEqual(proxy1, proxy2)

    def test_get_project_versions(self):
        self._mock_xmlrpc_method('package_releases', ['1.1', '1.2', '1.3'])
        versions = self.client.get_project_versions('Foo')
        self.assertEqual(versions, ['1.1', '1.2', '1.3'], 
            'a list of value must remain a list of values')

        self._mock_xmlrpc_method('package_releases', [])
        self.assertRaises(exceptions.ProjectDoesNotExist, 
            self.client.get_project_versions, 'Foo')

    def test_get_project_url(self):
        self._mock_xmlrpc_method('release_urls', 
        [
            {
                'url': 'http://pypi.python.org/packages/source/g/foo/foo-1.3.tar.gz', 
                'filename': 'foo-1.3.tar.gz', 
                'packagetype': 'sdist', 
            }, 
            {
                'url': 'http://pypi.python.org/packages/source/g/foo/foo-1.3.egg', 
                'filename': 'foo-1.3.egg', 
                'packagetype': 'bdist', 
            }
        ])
        self.assertEqual(self.get_project_url('Foo', '1.3'), 
            'http://pypi.python.org/packages/source/g/foo/foo-1.3.tar.gz')

        self.client.get_project_versions = Mock()
        self.client.get_project_versions.return_value = ['1.1', '1.2', '1.3']

        self.assertEqual(self.get_project_url('Foo'), 
            'http://pypi.python.org/packages/source/g/foo/foo-1.3.tar.gz')

        self.assertTrue(self.client.get_project_versions.called)

if __name__ == '__main__':
    unittest.main()


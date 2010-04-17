import unittest
from mock import Mock, Sentinel

from optparse import OptionParser
from install_distribution import InstallDistribution, ProjectDoesNotExist
from pypiclient.client import XmlRpcClient

class InstallDistributionTestCase(unittest.TestCase):
    """Test the command line installer behavior.

    """

    def setUp(self):
        """Construct the object to test.

        """
        self.object = InstallDistribution()
        self.object.parser = Mock(OptionParser)()
        self.object.options = None
        self.object.client = Mock(XmlRpcClient)()

    def _test_run(self, name, version):
        """Test the run method when values are defined by the user.

        """
        self.object.args = Sentinel()
        self.object.get_distribution_name = Mock(return_value=name)
        self.object.get_distribution_version = Mock(return_value=version)
        self.object.install_distribution = Mock()

        self.object.run()

        self.object.get_distribution_name.assert_called_with(self.object.args)
        self.object.get_distribution_version.assert_called_with(
            self.object.args, name)
 
    def test_run(self):
        """Test the different ways to use the run method.

        """
        self._test_run("Foo", "1.1")
        self.object.install_distribution.assert_called_with("Foo", "1.1")
        
        self._test_run("Foo", None)
        self.assertFalse(self.object.install_distribution.called)

        self._test_run(None, "1.1")
        self.assertFalse(self.object.install_distribution.called)

    def test_get_distribution_name(self):
        for values in (["Foo"], ["Foo", "Bar"]):
            # return the fisrst value for values len between 1 and 2.
            self.object.parser.error = Mock()
            self.assertEqual(self.object.get_distribution_name(values), "Foo")
            self.assertFalse(self.object.parser.error.called)

        for values in ([], ["Foo", "Bar", "FooBar"]):
            # an error is registred in object.parser for values < 1 or > 2
            self.object.parser.error = Mock()
            self.assertEqual(self.object.get_distribution_name(values), None)
            self.assertTrue(self.object.parser.error.called)

    def test_get_distribution_version(self):
        return
        def raise_exception():
            raise ProjectDoesNotExist()

        self.assertEqual(self.object.get_distribution_version(
            ["Foo", "1.1"], "Foo"), "1.1")

        self.assertEqual(self.object.get_distribution_version(
            ["Foo", ""]), None)

        self.object.client.get_project_versions = Mock(
            return_value=["1.1", "1.2", "1.3"])



        self.object.client.get_project_versions = Mock(
            side_effect=raise_exception)
                
 
if __name__ == '__main__':
    unittest.main()


#!/usr/bin/env python

from optparse import OptionParser
from urllib import urlretrieve
import subprocess
import tarfile

from pypiclient import XmlRpcClient, ProjectDoesNotExist

class Main(object):
    """Main class, provides an entry point for the install_distribution script.

    """

    def __init__(self):
        # retreive options
        usage = '%prog packagename [version]'
        self.parser = OptionParser(usage=usage)
        self.options, self.args = self.parser.parse_args()
        
        self.client = XmlRpcClient()
        
        argslen = len(self.args)
        if 1 <= argslen <= 2:
            distribution_name = self.args[0]
        else:
            self.parser.error(
                "thanks to specify the package name as the first argument")
        
        if argslen == 2:
            distribution_version = self.args[1]
        elif 1 <= argslen < 2:
            # ask for the version number
            try:
                available_versions = self.client.get_project_versions(distribution_name)
                print "Found versions of %s:" % distribution_name
                for version in available_versions:
                    print "\t%s" % version
                
                distribution_version = \
                    raw_input("Which version do you want to install (hit enter for None)? ")
            except ProjectDoesNotExist as e:
                print "The specified distribution does not exists: %s" % distribution_name
                return
        
        if distribution_version == '':
            return

        self.install_distribution(distribution_name, distribution_version) 

    def install_distribution(self, name, version):
        """Download and install the distribution.

        """
        url = self.client.get_project_url(name, version)
        filename, headers = urlretrieve(url)
        tar = tarfile.open(filename)
        tar.extractall(path='/tmp/')
        path = '/tmp/%s' % tar.getnames()[0]
        tar.close()
        subprocess.call(["python", "%s/setup.py" % path, "clean"])


if __name__ == "__main__":
    main = Main()

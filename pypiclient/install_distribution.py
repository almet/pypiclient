#!/usr/bin/env python

from optparse import OptionParser
from client import Client
from urllib import urlretrieve
import tarfile

class Main(object):
    """Main class, provides an entry point for the install_distribution script.

    """

    def __init__(self):
        # retreive options
        self.options, self.args = self.get_options()
        self.client = Client()
        
        argslen = len(self.args)
        if 1 <= argslen <= 2:
            distribution_name = self.args[0]
        else:
            print "error."
            return
        
        if argslen == 2:
            distribution_version = self.args[1]
        elif 1 <= argslen < 2:
            # ask for the version number
            available_versions = self.client.get_project_versions(distribution_name)
            print "Found versions of %s:" % distribution_name
            for version in available_versions:
                print "\t%s" % version
            
            distribution_version = \
                raw_input("Which version do you want to install (hit enter for None)? ")
        
        if distribution_version == '':
            return

        self.install_distribution(distribution_name, distribution_version) 
         

    def get_options(self):
        """Retrieves the options using OptionParser

        """

        usage = '%prog name [version]'
        parser = OptionParser(usage=usage)
        return parser.parse_args()

    def install_distribution(self, name, version):
        """Download and install the distribution.

        """
        url = self.client.get_project_url(name, version)
        filename, headers = urlretrieve(url)
        tar = tarfile.open(filename)
        from ipdb import set_trace
        set_trace()
        tar.extractall(path='/tmp/')
        tar.close()

if __name__ == "__main__":
    main = Main()

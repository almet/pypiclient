#!/usr/bin/env python

from optparse import OptionParser
from urllib import urlretrieve
import subprocess
import tarfile
import tempfile
import os
import shutil

from pypiclient import XmlRpcClient, ProjectDoesNotExist

class InstallDistribution(object):
    """Main class, provides an entry point for the install_distribution script.

    """

    def __init__(self):
        """Retreive options, build the XmlRpcClient and launch the script.

        """
        usage = '%prog packagename [version]'
        self.parser = OptionParser(usage=usage)
        self.options, self.args = self.parser.parse_args()
        self.client = XmlRpcClient()
        
    def run(self):
        dist_name = self.get_distribution_name(self.args)
        dist_version = self.get_distribution_version(self.args, dist_name)

        if dist_name and dist_version:
            self.install_distribution(dist_name, dist_version)

    def get_distribution_name(self, args):
        """Get the name of the package from args.

        """
        if 1 <= len(args) <= 2:
            return args[0]
        else:
            self.parser.error(
                "thanks to specify the package name as the first argument")
            return None
    
    def get_distribution_version(self, args, distribution_name):
        """Get distribution version from args, or by asking the user if 
        needed, displaying a the list of existing versions from Pypi 
        XmlRpcClient.

        """
        argslen = len(args)
        if argslen == 2:
            distribution_version = args[1]
        elif 1 <= argslen < 2:
            # ask for the version number
            try:
                available_versions = self.client.get_project_versions(distribution_name)
                print "Found versions of %s:" % distribution_name
                for version in available_versions:
                    print "\t%s" % version
                
                distribution_version = \
                    raw_input("Which version do you want to install (hit " \
                    "enter for None)? ")

            except ProjectDoesNotExist as e:
                print "The specified distribution does not exists: %s" % distribution_name
                return None
        
        if distribution_version == '':
            distribution_version = None

        return distribution_version

    def install_distribution(self, name, version):
        """Download, extract and install the distribution by calling 
        python setup.py install

        """
        url = self.client.get_project_url(name, version)
        filename, headers = urlretrieve(url)
        tar = tarfile.open(filename)
        temppath = tempfile.mkdtemp()
        tar.extractall(path=temppath)
        path = '%s/%s/' % (temppath, tar.getnames()[0])
        tar.close()
        os.chdir(path)
        os.system('python setup.py install')
        shutil.rmtree(temppath)

if __name__ == "__main__":
    main = InstallDistribution()
    main.run()

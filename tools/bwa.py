" tool for bwa "

__author__ = "hlevitin@broadinstitute.org"

import tools
import util.file
import os, logging

log = logging.getLogger(__name__)

# magic vars for now, later can set with config variables
# legacy version is version used in pipeline recipes (see old_scripts dir)
# current is lates version as of 8/27/2014
USE_CURRENT = True
DOWNLOAD_URL = {
    'legacy':
        'http://sourceforge.net/projects/bio-bwa/files/bwa-0.6.2.tar.bz2',
    'current':
        'http://sourceforge.net/projects/bio-bwa/files/bwa-0.7.10.tar.bz2'
    }

URL = DOWNLOAD_URL['current'] if USE_CURRENT else DOWNLOAD_URL['legacy']
BWA_DIR = '.'.join( [ x for x in URL.split("/")[-1].split('.') if
                        x != "tar" and x != "bz2" and x != "gz"])

class Bwa(tools.ExecutableToolWithSubcommands) :
    execName = 'bwa'

    def __init__(self, install_methods = None) :
        log.debug("BWA_DIR: {}".format(BWA_DIR))
        if install_methods == None :
            install_methods = []
            install_methods.append( tools.DownloadPackage(
                URL, "{}/bwa".format(BWA_DIR),
                post_download_command="cd {}; make".format(BWA_DIR)))
            tools.Tool.__init__(self, install_methods = install_methods)

    def version(self) :
        return ''.join([c for c in BWA_DIR if c.isdigit() or c=='.'])

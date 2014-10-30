"Tools in the blast+ suite."
import tools
import os

VERSION='2.2.29+'
URL_BASE = ''.join([
    'ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-',
    VERSION
    ])

def get_url() :
    uname = os.uname()
    if uname[0] == 'Darwin' :
        osStr = 'universal-macosx'
    elif uname[0] == 'Linux' :
        if uname[4].endswith('64') :
            osStr = 'x64-linux'
        else :
            osStr = 'ia32-linux'
    else :
        raise NotImplementedError('OS {} not implemented'.format(uname[0]))
    return '{}-{}.tar.gz'.format(URL_BASE, osStr)

class BlastTools(tools.Tool) :
    """
    Base class for tools in the blast+ suite.
       Subclasses must define class member subtoolName.

    Previous note said that this was an 'Abstract' base class.  If we want
    that, we have to make the class abstract though...
    """
    def __init__(self, install_methods = None) :
        if install_methods == None :
            target_rel_path = 'ncbi-blast-{}/bin/{}'.format(VERSION,
                    self.subtoolName)
            url = get_url()
            install_methods = [tools.DownloadPackage(url, target_rel_path)]
        tools.Tool.__init__(self, install_methods = install_methods)

class BlastnTool(BlastTools) :
    subtoolName = 'blastn'

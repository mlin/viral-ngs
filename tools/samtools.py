import tools, util.file
import os

# eventually move version to config file
VERSION='0.1.19'

DIR_NAME = 'samtools-{}'.format(VERSION)
URL = ''.join([
    'http://sourceforge.net/projects/samtools/files/samtools/',
    VERSION,
    '/', DIR_NAME, '.tar.bz2'
    ])

"""
From original broad install:
path = '/idi/sabeti-data/software/samtools/samtools-0.1.19/samtools',
install_methods.append(tools.PrexistingUnixCommand(path))
TODO: either make this or don't and remove the comment
"""

class SamtoolsTool(tools.ExecutableToolWithSubcommands) :
    execName = 'samtools'

    def __init__(self, install_methods = None) :
        if install_methods == None :
            install_methods = []
            install_methods.append(
                tools.DownloadPackage(URL, '{}/samtools'.format(DIR_NAME),
                    post_download_command='cd {}; make'.format(DIR_NAME)))
        tools.Tool.__init__(self, install_methods = install_methods)


    def version(self):
        return VERSION

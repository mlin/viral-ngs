
#!/usr/bin/env python

__author__ = "hlevitin@broadinstitute.org"

import unittest, os, sys, tempfile
import util.file, tools.bwa

class TestToolSamtools(unittest.TestCase) :

    def setUp(self) :
        util.file.set_tmpDir('TestToolSamtools')
        self.samtools = tools.samtools.Samtools()
        self.samtools.install()

    def tearDown(self) :
        util.file.destroy_tmpDir()

    def test_tool_samtools_faidx(self) :
        referenceDir = util.file.get_test_input_path()
        expectedDir = util.file.get_test_input_path(self)

        fasta = os.path.join(referenceDir, 'ebola.fasta')
        self.samtools.execute('faidx', [fasta])

        result = open('{}.fai'.format(fasta), 'rb')
        expected = open( os.path.join(expectedDir, 'ebola_expected.fasta.fai'),
                         'rb')

        self.assertEqual(result.read(),
                         expected.read() )

        result.close(); expected.close()

if __name__ == '__main__':
    unittest.main()

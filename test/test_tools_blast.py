#!/usr/bin/env python

__author__ = "hlevitin@broadinstitute.org"

import unittest, os, sys, tempfile
import util.file, tools.bwa

class TestToolBlastN(unittest.TestCase) :

    def setUp(self) :
        util.file.set_tmpDir('TestToolBlastN')
        self.blastn = tools.blast.BlastN()
        self.blastn.install()

    def tearDown(self) :
        util.file.destroy_tmpDir()

    def test_tool_blastn(self) :
        pass

if __name__ == '__main__':
    unittest.main()

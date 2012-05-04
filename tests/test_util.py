import os
from os import path
import unittest
import logging
import pprint

import config
from alnvu import util

infile = path.join(config.datadir, '10patients_aln.fasta')

class TestFastaObject(unittest.TestCase):
    def test01(self):
        self.assertTrue(path.isfile(infile))

    def test02(self):
        with open(infile) as f:
            seqs = util.readfasta(f)
            self.assertTrue(all(isinstance(seq, util.Seqobj) for seq in seqs))

    def test03(self):
        with open(infile) as f:
            seqs = util.readfasta(f)
            seq = seqs.next()

        self.assertTrue(hasattr(seq, 'name'))
        self.assertTrue(hasattr(seq, 'seq'))


class TestReadFasta(unittest.TestCase):
    def setUp(self):
        self.fobj = open(infile)

    def tearDown(self):
        self.fobj.close()

    def test01(self):
        seqs = util.readfasta(self.fobj)
        self.assertTrue('H59735' == seqs.next().name)

    def test02(self):
        seqs = util.readfasta(self.fobj, name_split = False)
        self.assertTrue('H59735 one|1' == seqs.next().name)

    def test03(self):
        seqs = util.readfasta(self.fobj, name_split = '|')
        self.assertTrue('H59735 one' == seqs.next().name)

class TestReformat(unittest.TestCase):
    def setUp(self):
        self.fobj = open(infile)
        self.seqs = util.readfasta(self.fobj)
        
    def tearDown(self):
        self.fobj.close()

    def test01(self):
        reformatted = util.reformat(self.seqs)


import os
from os import path
import unittest
import logging
import pprint

import config
from alnvu import util

infile = path.join(config.datadir, '10patients_aln.fasta')
treefile = path.join(config.datadir, '10patients_aln.tre')

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

    def test04(self):
        seqs = util.readfasta(self.fobj)
        self.assertTrue(len(list(seqs)) == 10)

    def test05(self):
        with open(path.join(config.datadir, 'one.fasta')) as f:
            seqs = util.readfasta(f)
            self.assertTrue(len(list(seqs)) == 1)

    def test06(self):
        with open(path.join(config.datadir, 'none.fasta')) as f:
            seqs = util.readfasta(f)
            self.assertRaises(ValueError, seqs.next)

            
class TestReformat(unittest.TestCase):
    def setUp(self):
        self.fobj = open(infile)
        self.seqs = util.readfasta(self.fobj)
        
    def tearDown(self):
        self.fobj.close()

    def test01(self):
        reformatted = util.reformat(self.seqs)

if util.treeorder:
    class TestTreeOrder(unittest.TestCase):
        def setUp(self):
            self.fobj = open(treefile)

        def tearDown(self):
            self.fobj.close()

        def test01(self):
            names = util.treeorder(self.fobj)
            self.assertTrue(len(names) == 10)

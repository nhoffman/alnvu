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
            self.assertRaises(StopIteration, seqs.next)

    def test07(self):
        with open(path.join(config.datadir, 'none.fasta')) as f:
            seqs = util.readfasta(f)
            self.assertEqual(list(seqs), [])

def render(seqlist, vnumstrs):
    for page in util.pagify(seqlist, vnumstrs, ncol=150):
        print ''
        for line in page:
            print line.rstrip()
        break

def render(*args):
    pass


class TestReformat(unittest.TestCase):
    def setUp(self):
        self.fobj = open(infile)
        self.seqs = util.readfasta(self.fobj)

    def tearDown(self):
        self.fobj.close()

    def test01(self):
        seqlist, vnumstrs, mask = util.reformat(self.seqs)
        render(seqlist, vnumstrs)

    def test02(self):
        seqlist, vnumstrs, mask = util.reformat(self.seqs, compare=False)
        render(seqlist, vnumstrs)

    def test03(self):
        seqlist, vnumstrs, mask = util.reformat(self.seqs, compare_to='H59735')
        render(seqlist, vnumstrs)

    def test04(self):
        seqlist, vnumstrs, mask = util.reformat(self.seqs, simchar=' ')
        render(seqlist, vnumstrs)

    def test05(self):
        seqlist, vnumstrs, mask = util.reformat(self.seqs, simchar='')
        render(seqlist, vnumstrs)

    def test06(self):
        seqlist, vnumstrs, mask = util.reformat(self.seqs, exclude_invariant=True)
        render(seqlist, vnumstrs)


if util.treeorder:
    class TestTreeOrder(unittest.TestCase):
        def setUp(self):
            self.fobj = open(treefile)

        def tearDown(self):
            self.fobj.close()

        def test01(self):
            names = util.treeorder(self.fobj)
            self.assertTrue(len(names) == 10)

from os import path
import unittest
import logging

from . import config
from alnvu import util

log = logging.getLogger(__name__)

infile = path.join(config.datadir, 'aln.fasta')
treefile = path.join(config.datadir, 'aln.tre')


class TestGetExtent(unittest.TestCase):
    def test01(self):
        seqs = [
            '----AAAA---',
            'AAAA---',
            '----AAAA',
            'AAAA',
        ]

        for s in seqs:
            start, stop = util.get_extent(s)
            self.assertEqual(s[start:stop], s.strip('-'))


class TestTabulate(unittest.TestCase):
    def test01(self):
        with open(infile) as f:
            seqs = list(util.readfasta(f))

        tabs = util.tabulate(seqs)
        cons = ''.join(util.consensus(tab) for tab in tabs)
        self.assertEqual(len(seqs[0].seq), len(cons))


class TestFastaObject(unittest.TestCase):
    def test01(self):
        self.assertTrue(path.isfile(infile))

    def test02(self):
        with open(infile) as f:
            seqs = util.readfasta(f)
            self.assertTrue(all(hasattr(seq, 'name') for seq in seqs))

    def test03(self):
        with open(infile) as f:
            seqs = util.readfasta(f)
            seq = next(seqs)

        self.assertTrue(hasattr(seq, 'name'))
        self.assertTrue(hasattr(seq, 'seq'))


class TestReadFasta(unittest.TestCase):
    def setUp(self):
        self.fobj = open(infile)

    def tearDown(self):
        self.fobj.close()

    def test01(self):
        seqs = util.readfasta(self.fobj)
        self.assertEqual('59735', seqs.next().name)

    def test02(self):
        seqs = util.readfasta(self.fobj, name_split='none')
        self.assertEqual('59735 one|1', seqs.next().name)

    def test03(self):
        seqs = util.readfasta(self.fobj, name_split='|')
        self.assertEqual('59735 one', seqs.next().name)

    def test04(self):
        seqs = util.readfasta(self.fobj)
        self.assertEqual(len(list(seqs)), 10)

    def test05(self):
        with open(path.join(config.datadir, 'one.fasta')) as f:
            seqs = util.readfasta(f)
            self.assertEqual(len(list(seqs)), 1)

    def test06(self):
        with open(path.join(config.datadir, 'none.fasta')) as f:
            seqs = util.readfasta(f)
            self.assertRaises(StopIteration, seqs.__next__)

    def test07(self):
        with open(path.join(config.datadir, 'none.fasta')) as f:
            seqs = util.readfasta(f)
            self.assertEqual(list(seqs), [])


# def render(seqlist, vnumstrs):
#     for page in util.pagify(seqlist, vnumstrs, ncol=150):
#         print ''
#         for line in page:
#             print line.rstrip()
#         break

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
        seqlist, vnumstrs, mask = util.reformat(self.seqs, compare_to='59735')
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

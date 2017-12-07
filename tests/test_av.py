from os import path
import os
import unittest
import logging
import sys
import shutil
from io import StringIO

from alnvu.av import main

from . import config

log = logging.getLogger(__name__)

infile = path.join(config.datadir, 'aln.fasta')
treefile = path.join(config.datadir, 'aln.tre')
renamefile = path.join(config.datadir, 'rename.csv')


def mkdir(dirpath, clobber=False):
    """
    Create a (potentially existing) directory without errors. Raise
    OSError if directory can't be created. If clobber is True, remove
    dirpath if it exists.
    """

    if clobber and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)

    try:
        os.makedirs(dirpath)
    except OSError as msg:
        log.debug(msg)

    if not path.exists(dirpath):
        raise OSError('Failed to create %s' % dirpath)

    return dirpath


class TestCLI(unittest.TestCase):
    outputdir = 'test_output'

    def outdir(self):
        """
        Name an outputdir as outpudir/module.class.method
        """
        funcname = '.'.join(self.id().split('.')[-3:])
        return path.join(self.outputdir, funcname)

    def mkoutdir(self, clobber=True):
        """
        Create output directory (destructively if clobber is True)
        """

        outdir = self.outdir()
        mkdir(outdir, clobber)
        return outdir

    def suppress_stdout(self):
        self.old_stdout = sys.stdout
        sys.stdout = StringIO()

    def suppress_stderr(self):
        self.old_stderr = sys.stderr
        sys.stderr = StringIO()

    def run_cmd(self, args):
        with open(path.join(self.outdir(), 'cmd.txt'), 'w') as f:
            f.write(' '.join(args) + '\n')

        main(args)

    def setUp(self):
        outdir = self.mkoutdir()
        self.args = [
            infile,
            '-o', path.join(outdir, 'out.txt'),
            '--html', path.join(outdir, 'out.html'),
            '--pdf', path.join(outdir, 'out.pdf'),
        ]

    def tearDown(self):
        if hasattr(self, 'old_stdout'):
            sys.stdout = self.old_stdout
        if hasattr(self, 'old_stderr'):
            sys.stdout = self.old_stderr

    def test01(self):
        self.run_cmd(self.args)

    def test02(self):
        self.run_cmd(self.args + ['--exclude-invariant'])

    def test03(self):
        self.run_cmd(self.args + ['--simchar', '.'])

    def test04(self):
        self.run_cmd(self.args + ['--exclude-invariant', '--simchar', '.'])

    def test05(self):
        self.run_cmd(
            self.args +
            ['--exclude-invariant', '--simchar', '.', '--consensus'])

    def test06(self):
        self.run_cmd(
            self.args +
            ['--exclude-invariant', '--simchar', '.', '--compare-to', '62024', '-i'])

    def test07(self):
        self.run_cmd(
            self.args +
            ['--exclude-invariant', '--simchar', '.', '--compare-to', '5', '-i'])

    def test08(self):
        self.run_cmd(
            self.args +
            ['--exclude-invariant', '--simchar', '.', '--blocks-per-page', '5'])

    def test09(self):
        self.run_cmd(self.args + ['--color'])

    def test10(self):
        self.run_cmd(self.args + ['--rename-from-file', renamefile])

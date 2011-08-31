#!/usr/bin/env python

import sys
import logging
from optparse import OptionParser
import pprint
import time

import Seq
log = logging

def main():

    usage = """%prog [options]

Create formatted sequence alignments with optional pdf output.
"""

    parser = OptionParser(usage=usage, version="$Id: findDuplicates.py 3354 2010-04-12 18:11:22Z nhoffman $")

    parser.set_defaults(
        add_consensus = False,
        compare_to = 0,
        # number_by = 0,
        exclude_invariant = False,
        exclude_gapcols = False,
        min_subs = 1,
        name_max= 35,
        ncol = 115,
        fontsize = 7,
        case = None,
        nrow = 75,
        orientation = 'portrait',
        blocks_per_page = 1,
        verbose = 0,
        quiet = False,
        seqnums = False
    )

    parser.add_option("-f", "--infile", dest="infile",
        help="input FILE containing sequence alignment")

    parser.add_option("-o", "--outfile", dest="outfile",
        help="Write output to a pdf file.")

    parser.add_option("-c", "--add_consensus", dest="add_consensus",
        help="Include show a consensus sequence [%default]",
        action='store_true')

    parser.add_option("-d", "--compare-to", dest="compare_to",
        help="""
Number of the sequence to use as a reference. Nucleotide positions
identical to the reference will be shown as a '.' The default behavior is
to use the consensus sequence as a reference. Use the -i option to display
the sequence numbers for reference. A value of -1 suppresses this behavior.
""", type='int')

#     parser.add_option("-N", "--number_by", dest="number_by",
#         help="""Number columns according to this sequence (uses the consensus by default).
# This option is useful for generating an alignment numbered according
# to a reference strain, for example.""", type='int')

    parser.add_option("-i", "--number-sequences", dest="seqnums",
        help="Show sequence number to left of name. [%default]",
        action='store_true')

    parser.add_option("-x", "--exclude-invariant", dest="exclude_invariant",
        help="""only show columns with at least min_subs non-consensus
bases (set min_subs using the -s option)""",
        action='store_true')

    parser.add_option("-g", "--exclude-gapcols", dest="exclude_gapcols",
        help="Remove columns containing only gap characters.",
        action='store_true')

    parser.add_option("-s", "--min_subs", dest="min_subs",
        help="minimum NUMBER of substitutions required to define a position as variable. [%default]",
        metavar="NUMBER", type='int')

    parser.add_option("-n", "--name-max", dest="name_max",
        help="maximum width of sequence name",
        metavar="NUMBER", type='int')

    parser.add_option("-w", "--width", dest="ncol",
        help="Width of sequence to display in each block in characters [%default]",
        metavar="NUMBER", type='int')

    parser.add_option("-F", "--fontsize", dest="fontsize",
        help="Font size for pdf output [%default]",
        metavar="NUMBER", default=7, type='int')

    parser.add_option("-C", "--case", dest="case",
        help="Convert all characters to a uniform case ('upper','lower') [%default]",
        metavar='CASE', choices=['upper','lower'])

    parser.add_option("-p", "--per-page", dest="nrow",
        help="Sequences (lines) per page of pdf output. [%default]",
        metavar="NUMBER", type='int')

    parser.add_option("-r", "--range", dest="rawrange",
        help="Range of aligned positions to display (eg '-r start,stop')",
                      metavar='RANGE')

    parser.add_option("-O", "--orientation", dest="orientation",
        help="Choose from portrait or landscape",
        metavar="ORIENTATION")

    parser.add_option("-b", "--blocks-per-page", dest="blocks_per_page",
                      metavar="NUMBER", type='int',
                      help="Number of aligned blocks of sequence per page [%default]")

    parser.add_option("-q", "--quiet", dest="quiet",
        help="Suppress output of alignment to screen.",
        action='store_true')

    parser.add_option("-v", "--verbose",
                      action="count", dest="verbose",
                      help="increase verbosity of screen output (eg, -v is verbose, -vv is more so)")


    options, args = parser.parse_args()

    loglevel = {0:logging.WARNING,
                1:logging.INFO,
                2:logging.DEBUG}.get(options.verbose, logging.DEBUG)

    verbose_format = '%(levelname)s %(funcName)s %(lineno)s %(message)s'
    logformat = {0:'%(message)s',
        1:verbose_format,
        2:verbose_format}.get(options.verbose, verbose_format)

    if __debug__:
        logformat = verbose_format

    # set up logging
    logging.basicConfig(file=sys.stdout,
        format=logformat,
        level=loglevel)

    instr = open(options.infile).read()
    seqs = Seq.io_fasta.read(instr)

    log.info('Read %s sequences from %s' % (len(seqs), options.infile))

    if options.rawrange:
        try:
            seqrange = [int(x) for x in options.rawrange.split(',')]
            if len(seqrange) != 2:
                raise ValueError
        except ValueError:
            log.error('Error in "-r %s": argument requires two integers separated by a comma.' % options.rawrange)
            sys.exit(1)
        else:
            log.info('Restricting alignment to positions %s' % str(seqrange))
    else:
        seqrange = None

    pages = Seq.sequtil.reformat(
        seqs,
        name_min = 10,
        name_max = options.name_max,
        nrow = options.nrow,
        ncol = options.ncol,
        add_consensus = options.add_consensus,
        compare_to = options.compare_to,
        exclude_gapcols = options.exclude_gapcols,
        exclude_invariant = options.exclude_invariant,
        min_subs = options.min_subs,
        simchar = '.',
        # number_by = options.number_by,
        countGaps = False,
        case = options.case,
        seqrange = seqrange,
        seqnums = options.seqnums)

    if not options.quiet:
        for page in pages:
            for line in page:
                print line.rstrip()
            print ''

    if options.outfile:
        log.info('Writing %s' % options.outfile)
        Seq.pdfutils.pdf_align(
            pages,
            outfile = options.outfile,
            fontsize = options.fontsize,
            orientation = options.orientation,
            blocks_per_page = options.blocks_per_page
            )

if __name__ == '__main__':
    main()

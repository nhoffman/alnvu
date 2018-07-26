#!/usr/bin/env python

"""
Create formatted sequence alignments with optional pdf output.
"""

import sys
import argparse
import csv

from alnvu import util, pdf, html, package_data
from alnvu import __version__, exit_on_sigint, exit_on_sigpipe


def get_range(rawrange):

    try:
        start, stop = [int(x) for x in rawrange.split(',')]
    except (ValueError, AttributeError):
        print((
            'Error in "-r/--range {}": argument requires two '
            'integers separated by a comma.'.format(rawrange)))
        sys.exit(1)

    return [start, stop]


def main(arguments=None):

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-V', '--version', action='version', version='alnvu {}'.format(__version__))

    parser.add_argument(
        "infile", type=argparse.FileType('r'), nargs='?',
        default=sys.stdin,
        help="Input file in fasta format (reads stdin if missing)")

    parser.add_argument(
        "-o", "--outfile", metavar='FILE', type=argparse.FileType('w'),
        default=sys.stdout,
        help="""output file for text (stdout by default, use -q/--quiet to suppress)""")

    parser.add_argument(
        "-q", "--quiet", dest="quiet", action='store_true', default=False,
        help="Suppress output of alignment to screen.")

    parser.add_argument(
        "--empty-ok", action='store_true', default=False,
        help="Exit with zero status if infile contains no sequences")

    # layout
    layout_options = parser.add_argument_group('Layout (applies to text and pdf)')

    layout_options.add_argument(
        "-w", "--width", dest="ncol", metavar="NUMBER", type=int, default=115,
        help="""Width of sequence to display in each block 'in
        characters [%(default)s]""")

    layout_options.add_argument(
        "-L", "--lines-per-block", dest="nrow", metavar="NUMBER", type=int, default=75,
        help="Sequences (lines) per block. [%(default)s]")

    # columns
    column_options = parser.add_argument_group('Column selection')

    column_options.add_argument(
        "-x", "--exclude-invariant",
        action='store_true', default=False,
        help="""Show only columns with at least N non-consensus bases
        (set N using '-a/--min-subs')""")

    column_options.add_argument(
        "-g", "--include-gapcols",
        action='store_true', default=False,
        help="Show columns containing only gap characters.")

    column_options.add_argument(
        "-r", "--range", dest="rawrange", metavar='INTERVAL',
        help="Range of columns to display (eg '-r start,stop')")

    column_options.add_argument(
        "-R", "--trim-to", metavar='SEQUENCE',
        help="""Trim alignment to the extent of this sequence
        identified by name or 1-based index (use
        `-i/--number-sequences` to display line numbers). """)

    column_options.add_argument(
        "-s", "--min-subs", dest="min_subs", metavar="NUMBER", type=int, default=1,
        help="""Minimum NUMBER of substitutions required to define a
        position as variable. [%(default)s]""")

    # consensus
    consensus_options = parser.add_argument_group(
        'Consensus display and sequence appearance')

    consensus_options.add_argument(
        "-c", "--consensus", dest="add_consensus", action='store_true', default=False,
        help="Show the consensus sequence [%(default)s]")

    consensus_options.add_argument(
        "-d", "--compare-to", dest="compare_to", metavar='SEQUENCE',
        help="""Identify the reference sequence by name or 1-based
        index (use `-i/--number-sequences` to display line
        numbers). Nucleotide positions identical to the reference will
        be replaced with `--simchar`. The default behavior is to use
        the consensus sequence as a reference.""")

    consensus_options.add_argument(
        "-D", "--no-comparison", action='store_false', dest='compare',
        default=True,
        help='Show all bases (ie, suppress comparsion with the reference sequence).')

    consensus_options.add_argument(
        "-G", "--ignore-gaps", dest="include_gaps", action="store_false",
        default=True, help='Ignore gaps in the calculation of a consensus.')

    consensus_options.add_argument(
        "-C", "--simchar", metavar='CHARACTER', default=None,
        help="""Character representing a base identical to the
        consensus. The default behavior is to identify differences
        using lower case.""")

    consensus_options.add_argument(
        '-t', '--reference-top', action='store_true',
        default=False,
        help="Place the reference/consensus sequence on the top of the alignment")

    # annotation
    name_options = parser.add_argument_group('Sequence annotation')

    name_options.add_argument(
        "-i", "--number-sequences", dest="seqnums", action='store_true', default=False,
        help="Show sequence number to left of name.")

    name_options.add_argument(
        "-n", "--name-max", dest="name_max", metavar="NUMBER", type=int, default=35,
        help="""Maximum width of sequence name in characters [%(default)s]""")

    name_options.add_argument(
        "-N", "--name-split", dest="name_split", metavar="CHARACTER",
        help="""Specify a character delimiting sequence names. By
        default, the name of each sequence is the first
        whitespace-delimited word. '--name-split=none' causes the
        entire line after the '>' to be displayed.""")

    name_options.add_argument(
        "-S", "--sort-by-name", type=argparse.FileType('r'), metavar='FILE',
        help="""File containing sequence names defining the sort-order
        of the sequences in the alignment.""")

    name_options.add_argument(
        "--rename-from-file", type=argparse.FileType('r'), metavar='FILE',
        help="""headerless csv file with columns 'old-name','new-name'
        to use for renaming the input sequences. If provided, renaming
        occurs immediately after reading the input sequences.""")

    if util.treeorder:
        name_options.add_argument(
            "-T", "--sort-by-tree", type=argparse.FileType('r'), metavar='FILE',
            help="""File containing a newick-format tree defining the
            sort-order of the sequences in the alignment (requires
            biopython).""")

    # for html output
    html_options = parser.add_argument_group('HTML output')
    html_options.add_argument(
        '--html', metavar='FILE', help="HTML output file")

    if html.default_brewer:
        html_options.add_argument(
            '--annotation-file', type=argparse.FileType('r'), metavar='FILE',
            help="""csv file with headers ("group", "col") specifying
            columns that should be colored in the html output. Each row
            identifies a label (group) and a corresponding column
            (1-indexed). Requires installation of the 'colorbrewer'
            package, which is python2 only.""")

    html_options.add_argument(
        '--table-only', action='store_true', default=False,
        help="""Don't produce a full html document, just the
        alignment table and style tags. Handy if you'd like to
        include in another document.""")

    html_options.add_argument(
        '--color', action='store_true', default=False,
        help='color nucleotides in output using default palette')

    html_options.add_argument(
        '--char-colors', type=argparse.FileType('r'), metavar='FILE',
        help="""csv file containing mapping of characters to
        HTML-defined colors (implies --color).""")

    html_options.add_argument(
        "--fontsize-html", metavar="NUMBER", default=7, type=int,
        help="Font size for html output [%(default)s]")

    # pdf options (only if reportlab is installed)
    if pdf.print_pdf:
        pdf_options = parser.add_argument_group(
            'PDF output',
            'These options require reportlab.')

        pdf_options.add_argument(
            '--pdf', metavar='FILE', help="PDF output file")

        pdf_options.add_argument(
            "-O", "--orientation", default='portrait',
            choices=('portrait', 'landscape'),
            help="Set page orientation; choose from portrait, landscape [%(default)s]")

        pdf_options.add_argument(
            "-b", "--blocks-per-page",
            metavar="NUMBER", type=int, default=1,
            help="Number of aligned blocks of sequence per page [%(default)s]")

        pdf_options.add_argument(
            "--fontsize-pdf", metavar="NUMBER", default=7, type=int,
            help="Font size for pdf output [%(default)s]")

    args = parser.parse_args(arguments or sys.argv[1:])

    # Ignore SIGPIPE, for head support
    exit_on_sigpipe()
    exit_on_sigint()

    seqs = util.readfasta(args.infile, name_split=args.name_split)

    if not seqs:
        if not args.quiet:
            print('No sequences in input')
        return 0 if args.empty_ok else 1

    if args.sort_by_name:
        sortdict = dict((line.strip(), i)
                        for i, line in enumerate(args.sort_by_name))
    elif getattr(args, 'sort_by_tree', None):
        names = util.treeorder(args.sort_by_tree)
        sortdict = dict((line.strip(), i) for i, line in enumerate(names))
    else:
        sortdict = {}

    if sortdict:
        seqs = iter(sorted(seqs, key=lambda seq: (sortdict.get(seq.name), seq.name)))

    if args.rename_from_file:
        namedict = dict(row for row in csv.reader(args.rename_from_file))
        seqs = (util.Seq(name=namedict.get(seq.name, seq.name), seq=seq.seq)
                for seq in seqs)

    formatted_seqs, vnumstrs, mask = util.reformat(
        seqs,
        add_consensus=args.add_consensus,
        compare=args.compare,
        compare_to=args.compare_to,
        exclude_gapcols=not args.include_gapcols,
        exclude_invariant=args.exclude_invariant,
        min_subs=args.min_subs,
        simchar=args.simchar,
        count_gaps=args.include_gaps,
        seqrange=get_range(args.rawrange) if args.rawrange else None,
        trim_to=args.trim_to,
        reference_top=args.reference_top)

    if args.html:
        if html.default_brewer and args.annotation_file:
            annotations = html.AnnotationSet.from_mapping_file(
                args.annotation_file, mask)
        else:
            annotations = None

        if args.char_colors:
            char_colors = html.parse_character_color_file(args.char_colors)
        elif args.color:
            with open(package_data('na_colors.csv')) as f:
                char_colors = html.parse_character_color_file(f)
        else:
            char_colors = None

        html.print_html(formatted_seqs, vnumstrs, mask,
                        outfile=args.html,
                        annotations=annotations,
                        fontsize=args.fontsize_html,
                        seqnums=args.seqnums,
                        charcolors=char_colors,
                        tableonly=args.table_only)

    all_numstrs = args.exclude_invariant or not args.include_gapcols

    pages = util.pagify(formatted_seqs, vnumstrs,
                        nrow=args.nrow,
                        ncol=args.ncol,
                        name_min=10,
                        name_max=args.name_max,
                        seqnums=args.seqnums,
                        all_numstrs=all_numstrs)

    if not args.quiet:
        for page in pages:
            for line in page:
                args.outfile.write(line.rstrip() + '\n')
            args.outfile.write('\n')

    if args.pdf:
        pdf.print_pdf(
            pages,
            outfile=args.pdf,
            fontsize=args.fontsize_pdf,
            orientation=args.orientation,
            blocks_per_page=args.blocks_per_page
        )

    for name, arg in args.__dict__.items():
        if hasattr(arg, 'close') and arg not in {sys.stdin, sys.stdout}:
            arg.close()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

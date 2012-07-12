=======
 alnvu
=======

``alnvu`` makes a multiple alignment of biological sequences more
easily readable by condensing it and highlighting variability.

dependencies
============

Required:

 * Python 2.7

Optional:

 * ``reportlab`` (http://www.reportlab.com/software/opensource/) for pdf output.
 * ``biopython`` (http://biopython.org/) to sort alignments in tree order.

installation
============

Using ``setup.py``::

    cd alnvu
    python setup.py install

examples
========

All of these examples can be run from within the package directory::

    % cd alnvu
    % ./av --help

    usage: av [-h] [-v] [-q] [-w NUMBER] [-L NUMBER] [-x] [-g] [-r INTERVAL]
	      [-s NUMBER] [-c] [-d NUMBER] [-D] [-C CASE] [-G] [-i] [-n NUMBER]
	      [-N CHARACTER] [-S FILE] [-T FILE] [-o OUTFILE] [-F NUMBER]
	      [-O ORIENTATION] [-b NUMBER]
	      [infile]

    Create formatted sequence alignments with optional pdf output.

    positional arguments:
      infile                Input file in fasta format (reads stdin if missing)

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -q, --quiet           Suppress output of alignment to screen.

    Layout:
      -w NUMBER, --width NUMBER
			    Width of sequence to display in each block in
			    characters [115]
      -L NUMBER, --lines-per-block NUMBER
			    Sequences (lines) per block. [75]

    Column selection:
      -x, --exclude-invariant
			    Show only columns with at least N non-consensus bases
			    (set N using the '-a/--min-subs')
      -g, --include-gapcols
			    Show columns containing only gap characters.
      -r INTERVAL, --range INTERVAL
			    Range of columns to display (eg '-r start,stop')
      -s NUMBER, --min-subs NUMBER
			    Minimum NUMBER of substitutions required to define a
			    position as variable. [1]

    Consensus display and sequence appearance:
      -c, --consensus       Show the consensus sequence [False]
      -d NUMBER, --compare-to NUMBER
			    Identify the reference sequence. Nucleotide positions
			    identical to the reference will be shown as a '.' The
			    default behavior is to use the consensus sequence as a
			    reference. Use the -i option to display the sequence
			    numbers for reference.
      -D, --no-comparison   Show all bases (ie, suppress comparsion with the
			    reference sequence).
      -C CASE, --case CASE  Convert all characters to a uniform case
			    ('upper','lower')
      -G, --ignore-gaps     Ignore gaps in the calculation of a consensus.

    Sequence annotation:
      -i, --number-sequences
			    Show sequence number to left of name.
      -n NUMBER, --name-max NUMBER
			    Maximum width of sequence name in characters [35]
      -N CHARACTER, --name-split CHARACTER
			    Specify a character delimiting sequence names. By
			    default, the name of each sequence is the first
			    whitespace-delimited word. '--name-split=none' causes
			    the entire line after the '>' to be displayed.
      -S FILE, --sort-by-name FILE
			    File containing sequence names defining the sort-order
			    of the sequences in the alignment.
      -T FILE, --sort-by-tree FILE
			    File containing a newick-format tree defining the
			    sort-order of the sequences in the alignment (requires
			    biopython).

    PDF output:
      These options require reportlab.

      -o OUTFILE, --outfile OUTFILE
			    Write output to a pdf file.
      -F NUMBER, --fontsize NUMBER
			    Font size for pdf output [7]
      -O ORIENTATION, --orientation ORIENTATION
			    Set page orientation; choose from portrait, landscape
			    [portrait]
      -b NUMBER, --blocks-per-page NUMBER
			    Number of aligned blocks of sequence per page [1]


The default output. Note that columns are numbered (column 8 is the first shown, column 122 is the last)::

    % ./av testfiles/10patients_aln.fasta | head -n 15
	     # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
	     # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111
	     # 0011111111112222222222333333333344444444445555555555666666666677777777778888888888999999999900000000001111111111222
	     # 8901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012
	H59735 AGAGTTTGATCCTGGCTCAGGACGAACGC.......GT.......................A.G..GCGGT....GCACCGTGGATT..........................T.
	T70875 ...........................---------------------------------------------------.----..--......--------------......T.
	F58095 AGAGTTTGATCCTGGCTCAGAGCGAACGC.......AT...................C....GTGGTTTCG..CATC-.----..--.............G.............G
	T70854 ...........................--.......AG..C.................G...ATG.CGGG.....GCTCCTTGATTC........C....G............TG
	F62024 AGAGTTTGATCCTGGCTCAGGACGAACGC.......GT.......................A.G..GCCTTT.GGGGTGGATT..--............................
	H59895 ...........................------------------------............G..AGAG.....AGCTCTCTGGATC...........................
	F57728 ...........................--------------------------------TT-----------------.----..--...........................G
	M10734 ...........................GC..A....GT........................GATCCATT...GCTTTTGTGTTTTTGGTGAG......................
	T71041 ..........................CGC.......AG.......................A.G..GTCT.....GCTAGACGGATT..........................TG
	M6161O ...........................--......T-G..C.....................ATCCTTCGG.A..---.----..--.............G..............


The input file can be provided via stdin::

   % cat testfiles/10patients_aln.fasta | ./av

Exercising some of the options (show sequence numbers and a consensus; show differences with sequence number 1, restrict to columns 200-300)::

    % ./av testfiles/10patients_aln.fasta --number-sequences --consensus --compare-to 1 --range 200,300
		   # 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
		   # 22222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222223
		   # 00000000001111111111222222222233333333334444444444555555555566666666667777777777888888888899999999990
		   # 01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
     1 -ref-> H59735 TGGGGtG-TTGGTgGAAAGCgttatgga------------GTGGTTTTAGATGGGCTCACGGCCTATCAGCTTGTTGGTGAGGTAATGGCTTACCAAGGCG
     2        T70875 G..T---.------.....T.GGGGACCGCAAGGCCTC..AC.CAGCAG..GC...CG.T.T.TG..T....A.......G.....A...CC.........
     3        F58095 G.CC---.------C.....CGA.A.--.............C.CC...G..GC...CTG..T..G..T..G.A.......G.....A...C.......C.T
     4        T70854 G..A---.------......AGGGGACCTTCGGGCCTT...C.C.A.C.....A..CT.G.T.GG..T....A.......G..........C.........
     5        F62024 ....A-C.GG...TA.....TCCG----.............C...GAAG....A..C.G.....................G.........C..........
     6        H59895 .CTTCA..CA.C.......AA..-----............TC...CAGG....A....G................................C.........
     7        F57728 .C.A.-.A.A.A.-.....GTGGCCTCTACATGTAAGCTATCAC.GAAG..G...A.TG..T.TG..T....A.....A.G.....C...CC.........
     8        M10734 .....-T..GTTG......GT..T.T--............C...A..GG.........G....T................G...G...............T
     9        T71041 GA.A---.------.....G.GGC.TTTAGCTC.......TC.C.AA......A..CT.A.T.GG..T....A.......G.....A...C..........
    10        M6161O G...---.------.....AT...----............TC.CCA..G..GC...C.G..T.TG..T....A.......G.....A....C.........
    11     CONSENSUS X..X.X.A.X.X.......XXXXXXXCXXXXXGXXXXXTAXC.C.XXXG.......CXG..T.XG..T....A.......G.....X...XX.........


Write a single-page pdf file::

    % ./av testfiles/10patients_aln.fasta --outfile=test.pdf --quiet --blocks-per-page=5

Same as above::

    % ./av testfiles/10patients_aln.fasta -o test.pdf -q -b 5

And do you know about ``seqmagick``? If not, run, don't walk to
https://github.com/fhcrc/seqmagick and check it out, so that you can
do this::

    % seqmagick convert testfiles/ae_like.sto --output-format=fasta - | ./av -cx
		   # 000000000000000000000000000000000
		   # 445555555555566666666666666667777
		   # 990111111155813445566778888991122
		   # 791123678914209568907050235891215
      GA05AQR01D2ULR ...............TTGGT.GT..AG...A..
      GA05AQR01DFGSE ........................T.TAAGT..
      GA05AQR01CI0QB ...........A.....................
      GA05AQR01DW22X .TC..G.T.T.......................
      GA05AQR01A5WF4 ....................A........-T..
      GA05AQR01BUV2U ---..............................
      GA05AQR01B1R8I .............T...............CT..
      GA05AQR02JASPX ........A........................
      GCX02B001AYSTJ .............................-TA.
      GCX02B001DP9EQ ............A..........CA.......T
      GCX02B001AFAY1 ..............G..................
      GCX02B002J489C ...-......A......................
      GLKT0ZE01EDLCP AT...ATT.T.......................
      GLKT0ZE02I8LRD ---GA............................
    -ref-> CONSENSUS TCTAGCGCGCGGGGACGAACGAGGCGCGCTGGA

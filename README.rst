=======
 alnvu
=======

``alnvu`` makes a multiple alignment of biological sequences more
easily readable by condensing it and highlighting variability.

dependencies
============

 * Python 2.7
 * ``reportlab`` (http://www.reportlab.com/software/opensource/) for pdf output.

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
    Usage: av [options] fasta_file

    Create formatted sequence alignments with optional pdf output.


    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -o OUTFILE, --outfile=OUTFILE
			    Write output to a pdf file.
      -c, --consensus       Include show a consensus sequence [False]
      -d COMPARE_TO, --compare-to=COMPARE_TO
			     Number of the sequence to use as a reference.
			    Nucleotide positions identical to the reference will
			    be shown as a '.' The default behavior is to use the
			    consensus sequence as a reference. Use the -i option
			    to display the sequence numbers for reference. A value
			    of -1 suppresses this behavior.
      -i, --number-sequences
			    Show sequence number to left of name. [False]
      -x, --exclude-invariant
			    only show columns with at least min_subs non-consensus
			    bases (set min_subs using the -s option)
      -g, --include-gapcols
			    Show columns containing only gap characters.
      -s NUMBER, --min_subs=NUMBER
			    minimum NUMBER of substitutions required to define a
			    position as variable. [1]
      -n NUMBER, --name-max=NUMBER
			    maximum width of sequence name in characters [35]
      -N CHARACTER, --name-split=CHARACTER
			    Specify a character delimiting sequence names. By
			    default, the name of each sequence is the first
			    whitespace-delimited word. '--name-split=none' causes
			    the entire line after the '>' to be displayed.
      -w NUMBER, --width=NUMBER
			    Width of sequence to display in each block in
			    characters [115]
      -F NUMBER, --fontsize=NUMBER
			    Font size for pdf output [7]
      -C CASE, --case=CASE  Convert all characters to a uniform case
			    ('upper','lower') [none]
      -L NUMBER, --lines-per-block=NUMBER
			    Sequences (lines) per block. [75]
      -r RANGE, --range=RANGE
			    Range of aligned positions to display (eg '-r
			    start,stop')
      -O ORIENTATION, --orientation=ORIENTATION
			    Choose from portrait or landscape
      -b NUMBER, --blocks-per-page=NUMBER
			    Number of aligned blocks of sequence per page [1]
      -q, --quiet           Suppress output of alignment to screen.
      -v, --verbose         increase verbosity of screen output (eg, -v is
			    verbose, -vv is more so)

The default output. Note that columns are numbered (column 8 is the first shown, column 122 is the last)::

    % ./av testfiles/10patients_aln.fasta
         # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111
         # 0011111111112222222222333333333344444444445555555555666666666677777777778888888888999999999900000000001111111111222
         # 8901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012
    H59735 ....................GA..............GT.......................A.G..GCGGT......ACCGTG.A..------....................T.
    T70875 -----------------------------------------------------------------------------------------------------------......T.
    F58095 ....................AG..............AT...................C....GTGGTTTCG..CAT.----------------.......G.............G
    T70854 -----------------------------.......AG..C.................G...ATG.CGGG........CCTTGAT.C------..C....G............TG
    F62024 ....................GA..............GT.......................A.G..GCCTTT.GG.G.GGATT----------......................
    H59895 ---------------------------------------------------............G..AGAG.....AGCTCTCT.GA.C-----......................
    F57728 -----------------------------------------------------------TT--------------------------------.....................G
    M10734 ---------------------------....A....GT........................GATCCATT...GCTT.TGTGTTT..G...........................
    T71041 --------------------------..........AG.......................A.G..GTCT........AGACG.A..------....................TG
    M6161O -----------------------------......T-G..C.....................ATCCTTCGG.A..------------------.......G..............
    
    ...

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

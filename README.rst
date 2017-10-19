=======
 alnvu
=======

``alnvu`` makes a multiple alignment of biological sequences more
easily readable by condensing it and highlighting variability.

Produces formatted multiple alignments in plain text, html, and pdf.

.. image:: https://travis-ci.org/nhoffman/alnvu.svg?branch=master
    :target: https://travis-ci.org/nhoffman/alnvu

authors
=======

 * Noah Hoffman
 * Chris Small
 * Connor McCoy
 * Tim Holland


dependencies
============

Required:

 * Python 2.7, 3.5+
 * ``fastalite`` (https://github.com/nhoffman/fastalite)

Optional:

 * ``reportlab`` (http://www.reportlab.com/software/opensource/) for pdf output.
 * ``biopython`` (http://biopython.org/) to sort alignments in tree order.
 * ``Jinja2`` (http://jinja.pocoo.org/) for rendering html templates.

installation
============

Installation is easiest using ``pip``::

  pip install alnvu

To install from the sources on GitHub, first clone the repository.

Using ``setup.py``::

  cd alnvu
  python setup.py install

Using ``pip``::

  cd alnvu
  pip install .


examples
========

    % cd alnvu

The default output. Note that columns are numbered (column 8 is the first shown, column 122 is the last)::

    % ./av -w 80 testfiles/aln.fasta | head -n 15
         # 00000000000000000000000000000000000000000000000000000000000000000000000000000000
         # 00000000000000000000000000000000000000000000000000000000000000000000000000000000
         # 00111111111122222222223333333333444444444455555555556666666666777777777788888888
         # 89012345678901234567890123456789012345678901234567890123456789012345678901234567
     59735 agagtttgatcctggctcaggacgaacgcTGGCGGCgtGCTTAACACATGCAAGTCGAACGaTgAAgcggtGCTTgcacc
     70875 --------------------------------------------------------------------------------
     58095 agagtttgatcctggctcagagcgaacgcTGGCGGCatGCTTAACACATGCAAGTCGcACGGgtggtttcgGCcatc---
     70854 -----------------------------TGGCGGCagGCcTAACACATGCAAGTCGAgCGGatgAcgggAGCTTgctcc
     62024 agagtttgatcctggctcaggacgaacgcTGGCGGCgtGCTTAACACATGCAAGTCGAACGaTgAAgcctttCggggtgg
     59895 ---------------------------------------------------AAGTCGAACGGTgAAagagAGCTTagctc
     57728 -----------------------------------------------------------tt-------------------
     10734 ---------------------------gcTGaCGGCgtGCTTAACACATGCAAGTCGAACGGgatccattAGCgcttttg
     71041 --------------------------cgcTGGCGGCagGCTTAACACATGCAAGTCGAACGaTgAAgtctAGCTTgctag
     6161O -----------------------------TGGCGGt-gGCcTAACACATGCAAGTCGAACGGatccttcggGaTT-----

The input file can be provided via stdin::

   % cat testfiles/aln.fasta | av

Exercising some of the options (show sequence numbers and a consensus; show differences with first sequence, restrict to columns 200-280)::

  % av testfiles/aln.fasta --number-sequences --consensus --range 200,280 --compare-to 59735
		  # 000000000000000000000000000000000000000000000000000000000000000000000000000000000
		  # 222222222222222222222222222222222222222222222222222222222222222222222222222222222
		  # 000000000011111111112222222222333333333344444444445555555555666666666677777777778
		  # 012345678901234567890123456789012345678901234567890123456789012345678901234567890
   1 ==REF==> 59735 TGGGGtG-TTGGTgGAAAGCgttatgga------------GTGGTTTTAGATGGGCTCACGGCCTATCAGCTTGTTGGTGA
   2          70875 gGGt----------GAAAGtGggggaccgcaaggcctc--acGcagcagGAgcGGCcgAtGtCtgATtAGCTaGTTGGTGg
   3          58095 gGcc----------cAAAGCcgaAaG--------------GcGccTTTgGAgcGGCctgCGtCCgATtAGgTaGTTGGTGg
   4          70854 gGGa----------GAAAGCaggggaccttcgggcctt--GcGcTaTcAGATGaGCctAgGtCggATtAGCTaGTTGGTGg
   5          62024 TGGGa-c-ggGGTtaAAAGCtccg----------------GcGGTgaagGATGaGCcCgCGGCCTATCAGCTTGTTGGTGg
   6          59895 TcttcaG-caGcTGGAAAGaaTT-----------------tcGGTcaggGATGaGCTCgCGGCCTATCAGCTTGTTGGTGA
   7          57728 TcGaG-GaTaGaT-GAAAGgtggcctctacatgtaagctatcacTgaagGAgGGGaTtgCGtCtgATtAGCTaGTTGGaGg
   8          10734 TGGGG-t-TgttgGGAAAGgtTTtTt--------------cTGGaTTggGATGGGCTCgCGGCtTATCAGCTTGTTGGTGg
   9          71041 gaGa----------GAAAGgGggcTtttagctc-------tcGcTaaTAGATGaGCctAaGtCggATtAGCTaGTTGGTGg
  10          6161O gGGG----------GAAAGatTTA----------------tcGccaTTgGAgcGGCcCgCGtCtgATtAGCTaGTTGGTGg
  11      CONSENSUS xGGx------x-x-GAAAGxxxxxxx--------------xcGcTxxxgGATGGGCcxgCGtCxgATtAGCTaGTTGGTGg


The above alignment rendered as colored html (thanks @timholl)::

  % av testfiles/aln.fasta --number-sequences --consensus --range 200,280 --compare-to 59735 -q --html aln.html

.. image:: https://github.com/nhoffman/alnvu/raw/master/doc/html.png

Write a single-page pdf file::

  % av testfiles/aln.fasta --pdf test.pdf --quiet --blocks-per-page=5

And do you know about ``seqmagick``? If not, run, don't walk to
https://github.com/fhcrc/seqmagick and check it out, so that you can
do this::

    % seqmagick convert testfiles/ae_like.sto --output-format=fasta - | av -cx
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

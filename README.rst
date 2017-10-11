=======
 alnvu
=======

``alnvu`` makes a multiple alignment of biological sequences more
easily readable by condensing it and highlighting variability.


authors
=======

 * Noah Hoffman
 * Chris Small
 * Connor McCoy
 * Tim Holland


dependencies
============

Required:

 * Python 2.7

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

All of these examples can be run from within the package directory::

    % cd alnvu

The default output. Note that columns are numbered (column 8 is the first shown, column 122 is the last)::

    % ./av testfiles/10patients_aln.fasta | head -n 15

         # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
         # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011111111111111111111111
         # 0011111111112222222222333333333344444444445555555555666666666677777777778888888888999999999900000000001111111111222
         # 8901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012
     59735 agagtttgatcctggctcaggacgaacgcTGGCGGCgtGCTTAACACATGCAAGTCGAACGaTgAAgcggtGCTTgcaccgtggatt------AGTGGCGAACGGGTGAGTAAtA
     70875 -----------------------------------------------------------------------------------------------------------GAGTAAtA
     58095 agagtttgatcctggctcagagcgaacgcTGGCGGCatGCTTAACACATGCAAGTCGcACGGgtggtttcgGCcatc----------------AGTGGCGgACGGGTGAGTAACg
     70854 -----------------------------TGGCGGCagGCcTAACACATGCAAGTCGAgCGGatgAcgggAGCTTgctccttgattc------AGcGGCGgACGGGTGAGTAAtg
     62024 agagtttgatcctggctcaggacgaacgcTGGCGGCgtGCTTAACACATGCAAGTCGAACGaTgAAgcctttCggggtggatt----------AGTGGCGAACGGGTGAGTAACA
     59895 ---------------------------------------------------AAGTCGAACGGTgAAagagAGCTTagctctctggatc-----AGTGGCGAACGGGTGAGTAACA
     57728 -----------------------------------------------------------tt--------------------------------AGTGGCGAACGGGTGAGTAACg
     10734 ---------------------------gcTGaCGGCgtGCTTAACACATGCAAGTCGAACGGgatccattAGCgcttttgtgtttttggtgagAGTGGCGAACGGGTGAGTAACA
     71041 --------------------------cgcTGGCGGCagGCTTAACACATGCAAGTCGAACGaTgAAgtctAGCTTgctagacggatt------AGTGGCGAACGGGTGAGTAAtg
     6161O -----------------------------TGGCGGt-gGCcTAACACATGCAAGTCGAACGGatccttcggGaTT------------------AGTGGCGgACGGGTGAGTAACA

The input file can be provided via stdin::

   % cat testfiles/10patients_aln.fasta | ./av

Exercising some of the options (show sequence numbers and a consensus; show differences with first sequence, restrict to columns 200-300)::

  % ./av testfiles/10patients_aln.fasta --number-sequences --consensus --range 200,300 --compare-to 59735
		  # 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
		  # 22222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222223
		  # 00000000001111111111222222222233333333334444444444555555555566666666667777777777888888888899999999990
		  # 01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
   1 ==REF==> 59735 TGGGGtG-TTGGTgGAAAGCgttatgga------------GTGGTTTTAGATGGGCTCACGGCCTATCAGCTTGTTGGTGAGGTAATGGCTTACCAAGGCG
   2          70875 gGGt----------GAAAGtGggggaccgcaaggcctc--acGcagcagGAgcGGCcgAtGtCtgATtAGCTaGTTGGTGgGGTAAaGGCccACCAAGGCG
   3          58095 gGcc----------cAAAGCcgaAaG--------------GcGccTTTgGAgcGGCctgCGtCCgATtAGgTaGTTGGTGgGGTAAaGGCcTACCAAGcCt
   4          70854 gGGa----------GAAAGCaggggaccttcgggcctt--GcGcTaTcAGATGaGCctAgGtCggATtAGCTaGTTGGTGgGGTAATGGCTcACCAAGGCG
   5          62024 TGGGa-c-ggGGTtaAAAGCtccg----------------GcGGTgaagGATGaGCcCgCGGCCTATCAGCTTGTTGGTGgGGTAATGGCcTACCAAGGCG
   6          59895 TcttcaG-caGcTGGAAAGaaTT-----------------tcGGTcaggGATGaGCTCgCGGCCTATCAGCTTGTTGGTGAGGTAATGGCTcACCAAGGCG
   7          57728 TcGaG-GaTaGaT-GAAAGgtggcctctacatgtaagctatcacTgaagGAgGGGaTtgCGtCtgATtAGCTaGTTGGaGgGGTAAcGGCccACCAAGGCG
   8          10734 TGGGG-t-TgttgGGAAAGgtTTtTt--------------cTGGaTTggGATGGGCTCgCGGCtTATCAGCTTGTTGGTGgGGTgATGGCTTACCAAGGCt
   9          71041 gaGa----------GAAAGgGggcTtttagctc-------tcGcTaaTAGATGaGCctAaGtCggATtAGCTaGTTGGTGgGGTAAaGGCcTACCAAGGCG
  10          6161O gGGG----------GAAAGatTTA----------------tcGccaTTgGAgcGGCcCgCGtCtgATtAGCTaGTTGGTGgGGTAAaGGCTcACCAAGGCG
  11      CONSENSUS xGGx------x-x-GAAAGxxxxxxx--------------xcGcTxxxgGATGGGCcxgCGtCxgATtAGCTaGTTGGTGgGGTAAxGGCxxACCAAGGCG


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

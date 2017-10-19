import re
import math
import itertools
from collections import Counter, namedtuple

from fastalite import fastalite

Seq = namedtuple('Seq', ['name', 'seq'])

SIMCHAR = '.'
GAPCHAR = '-'
ERRCHAR = 'X'

try:
    from Bio import Phylo
except ImportError:
    treeorder = None
else:
    def treeorder(infile):
        tree = next(Phylo.parse(infile, 'newick'))
        tree.ladderize()
        return [leaf.name for leaf in tree.get_terminals()]


def get_seq_from_list(compare_to, seqlist):
    """
    Return an item from 'seqlist' identified by string 'compare_to', defines as either:

    - a substring matching the name of a single sequence (case-sensitive)
    - the 1-based index if > 0
    - the 0-based index if < 1

    Raises ValueError if 'compare_to' doesn't meet one of the above criteria.
    """

    # assume that compare_to is the index of a sequence if it can be
    # coerced to an int, and the resulting index is in the range of
    # len(seqlist)
    try:
        ref_ix = int(compare_to)
        # assumes 1-based index if positive, or 0-based offset from
        # end if 0 or negative
        _s = seqlist[ref_ix - 1] if ref_ix > 0 else seqlist[ref_ix]
    except (ValueError, IndexError):
        pass
    else:
        return _s

    # doesn't seem to be an index... is it a string uniquely matching
    # a sequence name?
    matches = [i for i, seq in enumerate(seqlist) if compare_to in seq.name]
    if len(matches) == 1:
        return seqlist[matches[0]]

    # getting this far indicates an error
    raise ValueError(
        '"{}" must be either a string matching the name of a *single* sequence, '
        'or 1-based index of a sequence')

    return _s


def get_extent(seqstr):
    """Return (start, end) identifying the 0-based extent of seqstr
    excluding end-gaps.

    """

    start = re.search(r'[a-z]', seqstr, flags=re.I).start()
    stop = len(re.sub(r'[^a-z]+$', '', seqstr, flags=re.I))
    return start, stop


def reformat(seqs,
             add_consensus=True,
             compare=True,
             compare_to=None,
             exclude_gapcols=True,
             exclude_invariant=False,
             min_subs=1,
             simchar=SIMCHAR,
             gapchar=GAPCHAR,
             count_gaps=False,
             seqrange=None,
             trim_to=None,
             reference_top=False):
    """
    Reformat an alignment of sequences for display. Return a list of
    lists of strings; the outer list corresponds to pages.

    * seqs - list of objects with attributes 'name' and 'seq'
    * add_consensus - If True, include consensus sequence.
    * compare - if True (default), compare each character to
      corresponding position in the sequence specified by `compare_to`
      and replace with `simchar` if identical.
    * compare_to - Name or 1-based index of a reference sequence. None
      (the default) specifies the consensus. Ignored if `compare` is False.
    * exclude_gapcols - if True, mask columns with no non-gap characters
    * exclude_invariant - if True, mask columns without minimal polymorphism
    * min_subs -
    * simchar - character indicating identity to corresponding position in compare_to
    * gapchar - character representing gaps
    * count_gaps - include gaps in calculation of consensus and columns to display
    * seqrange - optional two-tuple specifying start and ending
      coordinates (1-index, inclusive)
    * trim_to - trim the alignment to the start and end positions of
      this sequence identified by name or 1-based index (ignored if
      seqrange is provided).
    * seqnums - show sequence numbers (1-index) to left of name if True
    * reference_top - put reference/consensus sequence at top instead of bottom
    """

    seqlist = list(seqs)
    nseqs = len(seqlist)

    # a list of Counter objects
    tabulated = tabulate(seqlist)

    cons = Seq(
        name='CONSENSUS',
        seq=''.join([consensus(d, count_gaps=count_gaps) for d in tabulated])
    )

    if add_consensus:
        if reference_top:
            seqlist.insert(0, cons)
        else:
            seqlist.append(cons)

    if compare:
        # replace bases identical to reference; make a copy of the
        # sequence for comparison because the original sequences will
        # be modified.
        if compare_to:
            compare_to_name, compare_to_str = get_seq_from_list(compare_to, seqlist)
        else:
            compare_to_name, compare_to_str = cons

        # replace characters identical to the reference
        for i, seq in enumerate(seqlist):
            name, seqstr = seq
            if name == compare_to_name:
                name = '==REF==> ' + name
            else:
                seqstr = seqdiff(seqstr, compare_to_str, simchar=simchar)

            seqlist[i] = Seq(name, seqstr)

    if seqrange:
        start, stop = seqrange
        start -= 1  # seqrange is 1-indexed
    elif trim_to:
        start, stop = get_extent(get_seq_from_list(trim_to, seqlist).seq)
    else:
        start, stop = 0, len(tabulated)

    mask = []
    for i, counts in enumerate(tabulated):
        show = start <= i < stop

        if exclude_gapcols:
            show &= counts.get(gapchar, 0) < nseqs

        if exclude_invariant:
            show &= count_subs(counts, count_gaps=count_gaps) >= min_subs

        mask.append(show)

    vnumstrs = [apply_mask(s, mask) for s in get_vnumbers(cons.seq)]
    seqlist = [Seq(s.name, apply_mask(s.seq, mask)) for s in seqlist]

    return (seqlist, vnumstrs, mask)


def apply_mask(instr, mask):
    return ''.join(c for c, m in zip(instr, mask) if m)


def pagify(seqlist, vnumstrs,
           name_min=10,
           name_max=35,
           nrow=65,
           ncol=70,
           all_numstrs=True,
           seqnums=False):
    """ This does the work of taking the mostly formatted sequences
    (still as seqobjs) and joining them together with names for the
    pdf and stdout outputs."""

    # XXX - todo, improve docs here ^

    seqcount = len(seqlist)

    longest_name = max([len(s.name) for s in seqlist])
    name_width = max([name_min, min([longest_name, name_max])])

    num_width = math.floor(math.log10(seqcount)) + 1

    fstr = '%%(name)%(name_width)ss %%(seqstr)-%(ncol)ss' % locals()
    if seqnums:
        fstr = ('%%(count)%(num_width)is ' % locals()) + fstr

    colstop = len(seqlist[0].seq)

    out = []
    # start is leftmost column for each block of columns
    for start in range(0, colstop, ncol):
        stop = min([start + ncol, colstop])

        # breaks into vertical blocks of sequences
        counter = itertools.count(1)
        for first in range(0, seqcount, nrow):
            out.append([])
            last = min([first + nrow, seqcount])

            msg = ''
            if seqcount > nrow:
                msg += 'sequences %s to %s of %s' % (first + 1, last, seqcount)

            if msg:
                out[-1].append(msg)

            this_seqlist = seqlist[first:last]

            if all_numstrs:
                # label each position
                for s in vnumstrs:
                    out[-1].append(
                        fstr % {'count': '', 'name': '#', 'seqstr': s[start:stop]})
            else:
                # label position at beginning and end of block
                half_ncol = int((stop - start) / 2)
                numstr = ' ' * name_width + \
                    ' %%-%(half_ncol)ss%%%(half_ncol)ss\n' % locals()
                out[-1].append(numstr % (start + 1, stop))

            for seq in this_seqlist:
                count = next(counter)
                seqstr = seq.seq[start:stop]
                name = seq.name[:name_width]
                out[-1].append(fstr % locals())

    return out


def readfasta(infile, name_split=None):
    """Returns an iterator of namedtuple objects with attributes 'name'
    and 'seq'.  'name_split' is a string on which to split sequence
    names, or "none" to define seq.name as the entire header line.

    """

    seqs = fastalite(infile)
    if name_split == 'none':
        seqs = (Seq(seq.description, seq.seq) for seq in seqs)
    elif name_split:
        seqs = (Seq(seq.description.split(name_split)[0], seq.seq) for seq in seqs)
    else:
        seqs = (Seq(seq.id, seq.seq) for seq in seqs)

    return seqs


def tabulate(seqs):
    """Return a list of Counter() objects describing the base frequency
    at each position in seqs.

    """

    seqs = list(seqs)
    lengths = {len(seq.seq) for seq in seqs}
    if len(lengths) > 1:
        raise ValueError('all sequences must be the same length')

    seqlen = lengths.pop()
    counters = [Counter() for i in range(seqlen)]
    for seq in seqs:
        for i, c in enumerate(seq.seq.upper()):
            counters[i].update([c])

    return counters


def consensus(count, count_gaps=False, plurality=2, gapchar='-', errchar='X'):
    """Calculates the consensus chacater at a position.

    * count - a Counter() object from tabulate() representing
      character frequencies at a single position
    * count_gaps - boolean indicating whether to include gap characters
      in tabulation of the consensus character.
    * plurality - minimum difference in frequency between most common and
      second most common characters
    * gapchar - the character representing a gap
    * errchar - character representing a position at which consensus
      could not be calculated (ie, count_gaps is False and all
      characters are gaps, or the difference in frequency between the
      first and second most common characaters is < plu)

    """

    if not count_gaps:
        try:
            del count[gapchar]
        except KeyError:
            pass

    if len(count) == 0:
        conschar = errchar
    elif len(count) == 1:
        conschar = count.most_common(1)[0][0]
    else:
        (char_1, count_1), (char_2, count_2) = count.most_common(2)
        if count_1 - count_2 < plurality:
            conschar = errchar
        else:
            conschar = char_1

    return conschar


def count_subs(tabdict, count_gaps=False, gap='-'):
    """Given a dict representing character frequency at a
    position of an alignment, returns 1 if more than
    one character is represented, 0 otherwise; excludes gaps
    if not count_gaps. There must be at least minchars present for
    a position to be considered variable"""

    tabdict = tabdict.copy()

    if not count_gaps:
        try:
            del tabdict[gap]
        except KeyError:
            pass

    if len(tabdict) <= 1:
        return 0

    # calculate count of most frequent character
    vals = sorted(tabdict.values())
    total = sum(vals)
    majority_char_count = vals.pop(-1)

    substitutions = total - majority_char_count

    return substitutions


def seqdiff(seq, templateseq, simchar=SIMCHAR, gapchar=GAPCHAR):
    """Compares strings seq and templateseq and returns a string in which
    non-gap characters in seq that are identical at that position to
    templateseq are replaced with simchar. Returned string is the
    length of the shorter of seq and templateseq.

    """

    if simchar and len(simchar) > 1:
        raise ValueError('simchar must contain a single character only')

    if simchar:
        seqstr = seq.upper()
        templatestr = templateseq.upper()

        def diff(s, t):
            return simchar if s == t and s != gapchar else s
    else:
        seqstr = seq.lower()
        templatestr = templateseq.lower()

        def diff(s, t):
            return s.upper() if s == t else s

    return ''.join(diff(s, t) for s, t in zip(seqstr, templatestr))


def get_vnumbers(seqstr, ignore_gaps=True, leadingZeros=True, gapchar=GAPCHAR):

    seqlen = len(seqstr)

    digs = len(repr(seqlen + 1))
    if leadingZeros:
        fstr = '%%0%si' % digs
    else:
        fstr = '%%%ss' % digs

    gapstr = gapchar * digs

    numchars = []
    i = 1
    for c in seqstr:
        if not ignore_gaps and c == gapchar:
            numchars.append(gapstr)
        else:
            numchars.append(fstr % i)
            i += 1

    if ignore_gaps:
        assert numchars == [fstr % x for x in range(1, seqlen + 1)]

    return [''.join([x[n] for x in numchars]) for n in range(digs)]

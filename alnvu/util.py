import math
import itertools
from itertools import imap

try:
    from Bio import Phylo
except ImportError:
    treeorder = None
else:
    def treeorder(infile):
        tree = Phylo.parse(infile, 'newick').next()
        tree.ladderize()
        return [leaf.name for leaf in tree.get_terminals()]


def reformat(seqs,
             add_consensus = True,
             compare=True,
             compare_to = None,
             exclude_gapcols = True,
             exclude_invariant = False,
             min_subs = 1,
             simchar = '.',
             countGaps = False,
             seqrange = None,
             reference_top=False
             ):

    """
    Reformat an alignment of sequences for display. Return a list of
    lists of strings; the outer list corresponds to pages.

    * seqs - list of objects with attributes 'name' and 'seq'
    * add_consensus - If True, include consensus sequence.
    * compare - if True (default), compare each character to corresponding position
      in the sequence specified by `compare_to` and replace with `simchar` if identical.
    * compare_to - Name of a reference sequence. None (the default) specifies the consensus.
    * exclude_gapcols - if True, mask columns with no non-gap characters
    * exclude_invariant - if True, mask columns without minimal polymorphism
    * min_subs -
    * simchar - character indicating identity to corresponding position in compare_to
    * countGaps - include gaps in calculation of consensus and columns to display
    * seqrange - optional two-tuple specifying start and ending coordinates (1-index, inclusive)
    * seqnums - show sequence numbers (1-index) to left of name if True
    * reference_top - put reference/consensus sequence at top instead of bottom
    """

    seqlist = [Seqobj(seq.name, seq.seq) for seq in seqs]
    nseqs = len(seqlist)

    # a list of dicts
    tabulated = tabulate(seqlist)

    consensus_str = ''.join([consensus(d, countGaps=countGaps) for d in tabulated]).upper()
    consensus_name = 'CONSENSUS'

    if add_consensus:
        consensus_seq = Seqobj(consensus_name, consensus_str)
        if reference_top:
            seqlist.insert(0, consensus_seq)
        else:
            seqlist.append(consensus_seq)

    if compare:
        # replace bases identical to reference; make a copy of the
        # sequence for comparison because the original sequences will
        # be modified.
        if compare_to is None:
            compare_to_name, compare_to_str = consensus_name, consensus_str[:]
        else:
            _s = seqlist[[s.name for s in seqlist].index(compare_to)]
            compare_to_name, compare_to_str = _s.name, _s.seq[:]

        for seq in seqlist:
            if seq.name == compare_to_name:
                seq.name = '==REF==> ' + seq.name
                seq.reference = True
            else:
                seq.seq = seqdiff(seq, compare_to_str, simchar)
                # seq.seq = seqdiff(
                #     seq, compare_to_str, simchar = None,
                #     wrap_variant="<span class='variant'>{}</span>")

    ii = range(len(seqlist[0]))
    mask = [True for i in ii]
    if seqrange:
        start, stop = seqrange
        mask = [start <= i + 1 <= stop for i in ii]

    if exclude_gapcols:
        mask1 = [d.get('-', 0) != nseqs for d in tabulated]
        mask = [m and m1 for m, m1 in zip(mask, mask1)]

    if exclude_invariant:
        mask1 = [count_subs(d, countGaps=countGaps) >= min_subs
                 for d in tabulated]
        mask = [m and m1 for m, m1 in zip(mask, mask1)]

    def apply_mask(instr):
        return ''.join(c for c, m in zip(instr, mask) if m)
    number_by_str = consensus_str
    vnumstrs = [apply_mask(s)
                for s in get_vnumbers(number_by_str, leadingZeros=True)]
    if seqrange or exclude_invariant or exclude_gapcols:
        for seq in seqlist:
            seq.seq = apply_mask(seq)

    return (seqlist, vnumstrs, mask)


def pagify(seqlist, vnumstrs,
             name_min = 10,
             name_max = 35,
             nrow = 65,
             ncol = 70,
             all_numstrs = True,
             seqnums = False):

    """ This does the work of taking the mostly formatted sequences (still as seqobjs) and joining them
    together with names for the pdf and stdout outputs."""

    # XXX - todo, improve docs here ^

    seqcount = len(seqlist)

    longest_name = max([len(s.name) for s in seqlist])
    name_width = max([name_min, min([longest_name, name_max])])

    num_width = math.floor(math.log10(seqcount)) + 1

    fstr = '%%(name)%(name_width)ss %%(seqstr)-%(ncol)ss' % locals()
    if seqnums:
        fstr = ('%%(count)%(num_width)is ' % locals()) + fstr

    colstop = len(seqlist[0])

    out = []
    # start is leftmost column for each block of columns
    for start in xrange(0, colstop, ncol):
        stop = min([start + ncol, colstop])

        # breaks into vertical blocks of sequences
        counter = itertools.count(1)
        for first in xrange(0, seqcount, nrow):
            out.append([])
            last = min([first + nrow, seqcount])

            msg = ''
            if seqcount > nrow:
                msg += 'sequences %s to %s of %s' % \
                (first+1, last, seqcount)

            if msg:
                out[-1].append(msg)

            this_seqlist = seqlist[first:last]

            if all_numstrs:
                # label each position
                for s in vnumstrs:
                    out[-1].append(
                    fstr % {'count':'','name':'#','seqstr':s[start:stop]} )
            else:
                # label position at beginning and end of block
                half_ncol = int((stop-start)/2)
                numstr = ' '*name_width + \
                    ' %%-%(half_ncol)ss%%%(half_ncol)ss\n' % locals()
                out[-1].append( numstr % (start + 1, stop) )

            for seq in this_seqlist:
                count = counter.next()
                seqstr = seq[start:stop]
                name = seq.name[:name_width]
                out[-1].append( fstr % locals() )

    return out

class Seqobj(object):
    """
    A minimal container for biological sequences.
    """

    def __init__(self, name, seq = None):
        self.name = name
        self.seq = seq or ''
        self.reference = False

    def __len__(self):
        return len(self.seq)

    def __iter__(self):
        return iter(self.seq)

    def __getitem__(self, index):
        return self.seq[index]

    def __getslice__(self, start, end):
        return self.seq[start:end]

    def __repr__(self):
        return '<Seqobj %s>' % (self.name,)

    # def __str__(self):
    #     return '>%s\n%s\n' % (self.name, self.seq)



def readfasta(infile, degap = False, name_split = None):
    """
    Lightweight fasta parser. Returns iterator of Seqobj objects given open file 'infile'.

    * degap - remove gap characters if True
    * name_split - string on which to split sequence names, or False
      to define seq.name as the entire header line.
    """

    name, seq = '', ''
    for line in imap(str.strip, infile):
        if line.startswith('>'):
            if name:
                yield Seqobj(name, seq)

            if name_split is False:
                name, seq = line.lstrip('> '), ''
            else:
                name, seq = line.lstrip('> ').split(name_split, 1)[0], ''
        else:
            seq += line.replace('-','') if degap else line

    if name:
        yield Seqobj(name, seq)

def tabulate( seqList ):
    """calculate the abundance of each character in the columns of
    aligned sequences; tallies are returned as a list of dictionaries
    indexed by position (position 1 = index 0). Keys of dictionaries are
    characters appearing in each position (so dictionaries are
    of variable length).

    seqList:            a list of sequence objects

    returns a list of dictionaries corresponding to each position"""

    # get length of alignment
    maxLength = max([len(seq) for seq in seqList])

    # initialize a data structure for storing the tallies
    dictList = [{} for i in xrange(maxLength)]

    for seq in seqList:
        #make sure seq is padded
        seqString = seq.seq
        seqString += '-'*(maxLength - len(seqString))

        # increment the dictionaries for this sequence
        # dict[char] = dict.get(char, 0) + 1
        # dict <--> dictList[i]
        # char <--> seqString[i]

        for i, c in enumerate(seqString):
            dictList[i][c] = dictList[i].get(c, 0) + 1

    return dictList

def consensus( tabdict, countGaps=False, plu=2, gap='-', errorchar='X', use_ambi=False ):
    """Given a dictionary from tabulate representing character frequencies
    at a single position, returns the most common char at
    that position subject to the rules below.

    countGaps       { 0 | 1 }
    plu            plurality for calling a consensus character

    Special cases:
    1) The most abundant character at a position is a gap
        if countGaps=0, uses the next most common character
            or 'x' if all chars are gaps
        if countGaps=1, puts a gap character ('-') at this position

    use_ambi - uses IUPAC ambiguity codes if possible in place of errorchar
    """


    tabdict = tabdict.copy()

    if not countGaps:
        try:
            del tabdict[gap]
        except KeyError:
            pass

        if len(tabdict) == 0:
            return errorchar

    # don't worry about gaps from here on
    if len(tabdict) == 1:
        return tabdict.keys()[0]

    rdict = dict([(v,k) for k,v in tabdict.items()])

    vals = sorted(tabdict.values())
    vals.reverse() #largest value is first

    majority, second = vals[:2]

    if majority-second < plu:
        if use_ambi:
            return IUPAC_rev.get(tuple(sorted(tabdict.keys())), errorchar)
        else:
            return errorchar
    else:
        return rdict[majority]

def count_subs(tabdict, countGaps=False, gap='-'):
    """Given a dict representing character frequency at a
    position of an alignment, returns 1 if more than
    one character is represented, 0 otherwise; excludes gaps
    if not countGaps. There must be at least minchars present for
    a position to be considered variable"""

    tabdict = tabdict.copy()

    if not countGaps:
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


def seqdiff(seq, templateseq, simchar='.'):
    """Compares seq and templateseq (can be Seq objects or strings)
    and returns a string in which non-gap characters in seq that are
    identical at that position to templateseq are replaced with
    simchar. Returned string is the length of the shorter of seq and
    templateseq."""

    if simchar and len(simchar) > 1:
        raise ValueError('simchar must contain a single character only')

    if simchar:
        seqstr = seq[:].upper()
        templatestr = templateseq[:].upper()
        def diff(s, t):
            return simchar if s == t and s != '-' else s
    else:
        seqstr = seq[:].lower()
        templatestr = templateseq[:].lower()
        def diff(s, t):
            return s.upper() if s == t else s

    return ''.join(diff(s, t) for s, t in zip(seqstr, templatestr))


# def seqdiff(seq, templateseq, simchar='.', wrap_variant=None):
#     """Compares seq and templateseq (can be Seq objects or strings)
#     and returns a string in which non-gap characters in seq that are
#     identical at that position to templateseq are replaced with
#     simchar. Returned string is the length of the shorter of seq and
#     templateseq"""

#     if simchar and len(simchar) > 1:
#         raise ValueError('simchar must contain a single character only')

#     seqstr = seq[:].upper()
#     templatestr = templateseq[:].upper()

#     if simchar:
#         def diff(s, t):
#             return simchar if s == t and s != '-' else s
#     elif wrap_variant:
#         def diff(s, t):
#             return wrap_variant.format(s) if s == t else s
#     else:
#         def diff(s, t):
#             return s.lower() if s == t else s

#     return ''.join(diff(s, t) for s, t in zip(seqstr, templatestr))


def get_vnumbers(seqstr, ignore_gaps=True, leadingZeros=True):

    seqlen = len(seqstr)

    digs = len(`seqlen+1`)
    if leadingZeros:
        fstr = '%%0%si' % digs
    else:
        fstr = '%%%ss' % digs

    gapstr = '-'*digs

    numchars = []
    i = 1
    for c in seqstr:
        if not ignore_gaps and c == '-':
            numchars.append(gapstr)
        else:
            numchars.append(fstr % i)
            i += 1

    if ignore_gaps:
        assert numchars == [fstr % x for x in xrange(1,seqlen+1)]

    return [''.join([x[i] for x in numchars]) for i in range(digs)]

import csv
import re

from jinja2 import Environment, PackageLoader

try:
    import colorbrewer
except ImportError:
    default_brewer = None
else:
    default_brewer = colorbrewer.Spectral

_env = Environment(loader=PackageLoader(__package__, 'data'))


def regex_replace(s, pattern, replace):
    """ Enable regex replacement in jinja template """
    _re = re.compile(pattern)
    return _re.sub(replace, s)


_env.filters['regex_replace'] = regex_replace


def rgb_from_triplet(triplet):
    return "#" + format((triplet[0] << 16) | (triplet[1] << 8) | triplet[2], '06x')


def load_template():
    """ Loads the template file, ready for rendering. """
    return _env.get_template('html_template.jinja')


def print_html(formatted_seqs, vnumstrs, mask, outfile, annotations=None,
               fontsize=12, seqnums=None, charcolors=None, tableonly=False):
    # XXX - Uhh... what are seqnums?
    render_dict = dict(seqlist=formatted_seqs, vnumstrs=vnumstrs,
                       mask=mask, annotations=annotations, colors=charcolors,
                       tableonly=tableonly)
    with open(outfile, 'w') as handle:
        load_template().stream(render_dict).dump(handle)


def parse_character_color_file(char_color_file):
    """ Parses file into a dict map of characters to css colors """
    reader = csv.DictReader(char_color_file, fieldnames=['name', 'color'])
    mapping = dict()
    for row in reader:
        mapping[row['name']] = row['color']

    if hasattr(char_color_file, 'close'):
        char_color_file.close()

    return mapping


def parse_mapping_file(mapping_handle):
    """ Parses into a dict map of col numbers to groups """
    reader = csv.DictReader(mapping_handle)
    mapping = dict()
    for row in reader:
        # later will want to support col formats like 23-45
        mapping[int(row['col'])] = row['group']

    mapping_handle.close()

    return mapping


class AnnotationSet(object):

    @classmethod
    def from_mapping_file(cls, handle, mask, color_mapping=None,
                          brewer=default_brewer):
        """ Convenience method for loading directly from files. """
        mapping = parse_mapping_file(handle)
        return cls(mapping, mask, color_mapping)

    def __init__(self, col_mapping, mask, color_mapping=None, brewer=default_brewer):
        """col_mapping is a mapping of 1-index based columns to group
        names. mask is the mask to be applied to sequences and number
        string rows.

        """
        self.col_mapping = col_mapping
        self.mask = mask
        self.mask_cols = [i + 1 for i in range(len(mask)) if mask[i]]
        self.groups = list(
            set(self.col_mapping[c] for c in list(self.col_mapping.keys())))

        if color_mapping:
            self.color_mapping = color_mapping
        else:
            n = len(self.groups)
            try:
                pallette = brewer[n]
            except KeyError:
                pallette = brewer[min(brewer.keys())]

            colors = [rgb_from_triplet(t) for t in pallette]
            self.color_mapping = dict()
            for i in range(n):
                self.color_mapping[self.groups[i]] = colors[i]

    def masked_index(self, col):
        return self.mask_cols.index(col)

    def get_color(self, group):
        if group is None:
            return None
        return self.color_mapping[group]

    def iterate(self, iterable):
        """ Iterate over a seq or number string """
        latest_region = []
        last_group = None

        def join_region(l):
            return ''.join(str(x) for x in l)

        for i in range(len(self.mask)):
            col = i + 1
            if not self.mask[i]:
                # If masked, we just skip
                continue

            try:
                group = self.col_mapping[col]
            except KeyError:
                group = None

            index = self.masked_index(col)
            item = iterable[index]
            if group == last_group:
                latest_region.append(item)
                last_yield = False
                # import pdb; pdb.set_trace()

            else:
                last_yield = True
                yield (join_region(latest_region),
                       last_group,
                       self.get_color(last_group))
                latest_region = [item]
                last_group = group

        if not last_yield:
            # Hmm... do we actually need the check here?
            yield (join_region(latest_region), last_group, self.get_color(last_group))


from jinja2 import Template
import os

def load_template():
    abspath = os.path.abspath(__file__)
    path_parts = abspath.split('/')[:-1]
    path_parts.insert(0, '/')
    path_parts.append('html_template.jinja')
    template_fn = os.path.join(*path_parts)
    text = file(template_fn).read()
    return Template(text)

def print_html(formatted_seqs, vnumstrs, mask, outfile, annotations=None, fontsize=12, seqnums=None):
    # XXX - Uhh... what are seqnums?
    render_dict = dict(seqlist=formatted_seqs, vnumstrs=vnumstrs, mask=mask)
    handle = file(outfile, 'w')
    template = load_template()
    rendered = template.render(render_dict)
    handle.write(rendered)
    handle.close()

class AnnotationSet(object):
    @classmethod
    def from_mapping_file(cls, mapping_file):
        pass
            
    def __init__(self, col_mapping, mask, color_mapping=None):
        self.col_mapping = col_mapping
        self.mask = mask
        self.color_mapping = color_mapping

    def iterate(self, iterable):
        """ Iterate over a seq or number string """
        pass



import sequtil
import os
import logging
import sys
log = logging

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch, cm
    from reportlab.lib.pagesizes import letter, landscape, portrait
except ImportError, msg:
    #log.error(msg)
    pass

def pdf_align(pages, outfile, fontsize = 7, orientation='portrait',
              blocks_per_page=1):

    if orientation == 'portrait':
        pagesize = portrait(letter)
    elif orientation == 'landscape':
        pagesize = landscape(letter)

    #precalculate some basics
    top_margin = pagesize[1] - .75*inch
    bottom_margin = 0.75*inch
    left_margin = 0.5*inch
    right_margin = pagesize[0] - 0.5*inch
    frame_width = right_margin - left_margin

    top_margin_offset = 0

    document_font = 'Courier'

    def drawPageFrame(canv):

        # pagecount = len(pages)
        pagecount = len(pageIter)
        pg = canv.getPageNumber()
        ofn = os.path.split(outfile)[-1]

        page_center = 0.5 * pagesize[0]

        canv.drawCentredString(page_center, top_margin + 0.3*inch,
            '%(ofn)s' % locals())

        lineycoord = top_margin + 0.25*inch
        canv.line(left_margin, lineycoord, right_margin, lineycoord)
#       canv.setFont(document_font,fontsize)

        canv.drawCentredString(page_center, 0.5*inch,
            'Page %(pg)s of %(pagecount)s' % locals())

    canv = canvas.Canvas(outfile, invariant=1, pagesize=pagesize)
    canv.setPageCompression(1)

    pageIter = list(sequtil.grouper(blocks_per_page, pages, pad=False))

    for pagegroup in pageIter:
        drawPageFrame(canv)
        canv.setFont(document_font, fontsize)
        tx = canv.beginText(left_margin, top_margin - top_margin_offset)

        for i, page in enumerate(pagegroup):
            for line in page:
                tx.textLine(line)
            # separate blocks
            if blocks_per_page > 1 and i + 1 < blocks_per_page:
                tx.textLine('')

        canv.drawText(tx)
        canv.showPage()



    canv.save()

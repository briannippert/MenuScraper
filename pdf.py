import re
from urllib.request import urlretrieve
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import sys
from datetime import date
import calendar


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text


def handler(event, context):
    urlretrieve("http://corporatecafeboston.com/linked/woburn.pdf",
                "download.pdf")
    text = convert_pdf_to_txt("download.pdf")
    my_date = date.today()
    date = event['currentIntent']['slots']['date']
    if not date:
        date = calendar.day_name[my_date.weekday()]
    results = re.findall(r'{0}[\w\W]+?Sandwich:  (.*)?\n'.format(), text)
    if results:
        result = results[0]
    else:
        result = "No Food For You"
    return {
        'message': result
    }

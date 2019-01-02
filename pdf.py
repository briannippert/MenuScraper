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


urlretrieve("http://corporatecafeboston.com/linked/woburn.pdf", "download.pdf")
text = convert_pdf_to_txt("download.pdf")
try:
    date = sys.argv[1]
    print(date)
except:
    my_date = date.today()
    date = calendar.day_name[my_date.weekday()]
    print(date)
results = re.match( r'{}[\w\W]+?Sandwich:  (.*)?\n'.format(date),text)
print(results)
results.group(1)





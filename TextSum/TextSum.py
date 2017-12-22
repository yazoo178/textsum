import PyPDF2
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import re
import nltk.data

class pdf:
    def __init__(self):
        self.lines = []
        self.intrstingLines = []
        self.name = ""





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



if __name__ == "__main__":
    pdfs = []

    for file in os.listdir("pdfs/"):
        text = convert_pdf_to_txt("pdfs/" + file)
        pd = pdf()
        pd.name =  file.split(".")[0]
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        text = text.replace('\n', '')
        text = tokenizer.tokenize(text)
        [pd.lines.append(x) for x in text]

        pdfs.append(pd)


    for pd in pdfs:
        for i, line in enumerate(pd.lines):
            if len(re.findall("[0-9]+", line)) > 0:
                pd.intrstingLines.append(i)


    if not os.path.isdir("sums/"):
        os.mkdir("sums")


    for pd in pdfs:
        pdFile = open("sums/" + pd.name + "_int_lines" + ".txt", "w", encoding='utf-8')
        for intLine in pd.intrstingLines:
            pdFile.write(pd.lines[intLine] + "\t:" + str(intLine) + "\n")
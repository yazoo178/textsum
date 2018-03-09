import PyPDF2
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import re
import nltk.data
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class stats:
    def __init__(self):
        self.marks = []


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


def getMark (strA):
    marks = []
    for pot in strA:
        spl = pot.split("/")

        if(spl[1] == "25"):
            (marks.append(int(spl[0])))

        if(spl[1] == "15"):
            (marks.append(int(spl[0])))

        if(spl[1] == "10"):
            (marks.append(int(spl[0])))


    return marks


if __name__ == "__main__":
    pdfs = []
    path = "C:\\Users\\william\\Downloads\\marking-20180108T123215Z-001\\marking\\"
    sta = stats()

    for file in os.listdir(path):
        if ".pdf" in file:
            markedBy = "William"
            if "_j" in file:
                markedBy = "James"

            text = convert_pdf_to_txt(path + file)
            text = text.replace('\n', '')
            strMark = re.findall("[0-9]{1,2}/[0-9]{2}", text)

            mark = getMark(strMark)

            sta.marks.append((markedBy, mark))




    results = open("resultsFile.txt", "w")

    marks = []
    marks_report = []
    marks_code = []

    wmarks = []
    wmarks_report = []
    wmarks_code = []

    jmarks = []
    jmarks_report = []
    jmarks_code = []


    for x in sta.marks:
        if x[0] == "William":
            wmarks.append(x[1][0])
            wmarks_code.append(x[1][1])
            wmarks_report.append(x[1][2])

        else:
            jmarks.append(x[1][0])
            jmarks_code.append(x[1][1])
            jmarks_report.append(x[1][2])

        marks.append(x[1][0])
        marks_code.append(x[1][1])
        marks_report.append(x[1][2])


    print(len(marks))
    mean = sum(marks) / len(marks)
    print(mean)
    c_mean = sum(marks_code) / len(marks_code)
    r_mean = sum(marks_report) / len(marks_report)
    print(mean)

    fails = [x for x in marks if x < 13]



    print(len(marks))
    w_mean = sum(wmarks) / len(wmarks)
    w_c_mean = sum(wmarks_code) / len(wmarks_code)
    w_r_mean = sum(wmarks_report) / len(wmarks_report)

    print(w_mean)
    w_fails = [x for x in wmarks if x < 13]

    print(len(marks))
    j_mean = sum(jmarks) / len(jmarks)
    j_c_mean = sum(jmarks_code) / len(jmarks_code)
    j_r_mean = sum(jmarks_report) / len(jmarks_report)

    print(j_mean)
    j_fails = [x for x in jmarks if x < 13]



    results.write("Overall: " + "\n")
    results.write("Number Marked: " + str(len(marks))  + "\n")
    results.write("Mean: " + str(mean) + "\n")
    results.write("Highest Mark: " + str(max(marks)) + "\n")
    results.write("Lowest Mark: " + str(min(marks)) + "\n")
    results.write("Fails: " + str(len(fails)) + "\n")
    results.write("Code Style Mean: " + str(c_mean) + "\n")
    results.write("Report Mean: " + str(r_mean) + "\n")
    results.write("Report Highest: " +  str(max(marks_report)) + "\n")
    results.write("Report Lowest: " +  str(min(marks_report)) + "\n")
    results.write("Code Mean: " + str(c_mean) + "\n")
    results.write("Code Highest: " +  str(max(marks_code)) + "\n")
    results.write("Code Lowest: " +  str(min(marks_code)) + "\n")

    results.write("\n")  
    results.write("William: " + "\n")
    results.write("Number Marked: " + str(len(wmarks))  + "\n")
    results.write("Mean: " + str(w_mean) + "\n")
    results.write("Highest Mark: " + str(max(wmarks)) + "\n")
    results.write("Lowest Mark: " + str(min(wmarks)) + "\n")
    results.write("Fails: " + str(len(w_fails)) + "\n")
    results.write("Code Style Mean: " + str(w_c_mean) + "\n")
    results.write("Report Mean: " + str(w_r_mean) + "\n")
    results.write("Report Highest: " +  str(max(wmarks_report)) + "\n")
    results.write("Report Lowest: " +  str(min(wmarks_report)) + "\n")
    results.write("Code Mean: " + str(w_c_mean) + "\n")
    results.write("Code Highest: " +  str(max(wmarks_code)) + "\n")
    results.write("Code Lowest: " +  str(min(wmarks_code)) + "\n")

    results.write("\n")  
    results.write("James:" + "\n")
    results.write("Number Marked:  " + str(len(jmarks))  + "\n")
    results.write("Mean: " + str(j_mean) + "\n")
    results.write("Highest Mark: " + str(max(jmarks)) + "\n")
    results.write("Lowest Mark: " + str(min(jmarks)) + "\n")
    results.write("Fails: " + str(len(j_fails)) + "\n")
    results.write("Code Style Mean: " + str(j_c_mean) + "\n")
    results.write("Report Mean: " + str(j_r_mean) + "\n")
    results.write("Report Highest: " +  str(max(jmarks_report)) + "\n")
    results.write("Report Lowest: " +  str(min(jmarks_report)) + "\n")
    results.write("Code Mean: " + str(j_c_mean) + "\n")
    results.write("Code Highest: " +  str(max(jmarks_code)) + "\n")
    results.write("Code Lowest: " +  str(min(jmarks_code)) + "\n")

    mean,std=norm.fit(marks)
    plt.hist(marks, bins=30, normed=True)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    y = norm.pdf(x, mean, std)
    plt.plot(x, y)
    plt.show()

    results.close()
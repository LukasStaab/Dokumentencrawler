#!/usr/bin/python
# coding=utf-8
import re, urllib, os
from urllib2 import urlopen, URLError, HTTPError
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


#Methode zum Konvertieren von PDFs
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


#Methode zum DL von URLs
def dlPDFAndConvert(url,abschluss):
    # Open the url
    try:
        f = urlopen(url)
        print "downloading: " + url

        # Open our local file for writing PDF
        with open("../res/"+ abschluss +"pdf/" + os.path.basename(url), "wb") as local_file:
            local_file.write(f.read())

        print "converting..."
        #Open local file for convert pdf to txt
        with open("../res/"+ abschluss + "txt/" + os.path.basename(url) + ".txt", "wb") as local_file:
            local_file.write(convert_pdf_to_txt("../res/" + abschluss + "pdf/" + os.path.basename(url)))

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url


#Auf diesen beiden Seiten sind alle Studiengaenge verlinkt
#urlBA = "https://www.tu-ilmenau.de/studierende/studium/studienangebot/bachelor/"
#urlMA = "https://www.tu-ilmenau.de/studierende/studium/studienangebot/master/"
url =  "https://www.tu-ilmenau.de/studierende/studium/studienangebot/"

#Regexp für die Art von Links nach denen ich suche
searchStud ="<a href=\"studierende/studium/studienangebot/(.+?)\"" #Links zu Studiengaengen
searchPDFs = "<a href=\"fileadmin(.+?).pdf" #Relevante Files

for abschluss in ["bachelor/","master/"]:
    for stud in re.findall(searchStud, urllib.urlopen(url + abschluss).read(), re.I):
        print stud
        studURL = url + stud
        print studURL
        for pdffile in re.findall(searchPDFs, urllib.urlopen(studURL).read(), re.I):
            dlPDFAndConvert("http://tu-ilmenau.de/fileadmin" + pdffile + ".pdf",abschluss)





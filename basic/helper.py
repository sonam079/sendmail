from basic.models import EmailTemplates
from django.shortcuts import get_object_or_404
from django.conf import settings
from bs4 import BeautifulSoup
import os

# Opens file in read mode
def open_file(pk):
    filename = get_addr(pk)
    testFile = open(filename)
    return testFile

# Opens file in write mode
def write_in_file(pk, soup):
    filename = get_addr(pk)
    testFile = open(filename, 'w+')
    for line in soup.prettify():
        testFile.write(line)
    testFile.close()

# Gets the address of the file to be opened
def get_addr(pk):
    emailTemplates = get_object_or_404(EmailTemplates, id=pk)
    BASE_DIR = settings.MEDIA_ROOT
    template_addr = os.path.join(BASE_DIR, str(emailTemplates))
    return template_addr

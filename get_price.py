import bs4 as bs
import sys
import schedule
import time
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl

import winsound

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second


class Page(QWebEnginePage):
    def __init__(self):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''


    def new_url(self, url):
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()

page = Page()

def exact_url(url):
    index = url.find("B0")
    index = index + 10
    current_url = ""
    current_url = url[:index]
    return current_url


def mainprogram(url):
    exacturl = exact_url(url)  # main url to extract data
    page.new_url(exacturl)
    soup = bs.BeautifulSoup(page.html, 'html.parser')
    js_test = soup.find('span', id='priceblock_ourprice')
    if js_test is None:
        js_test = soup.find('span', id='priceblock_dealprice')
    name = soup.find('span', id='productTitle')
    str = ""
    for line in js_test.stripped_strings:
        str = line
    product = ''
    for line in name.stripped_strings:
        product = line
    print(product)
        # convert to integer
    str = str.replace(", ", "")
    your_price = 600
    print(str)
    return (product, str)



def job(url):
    print("Tracking....")
    return mainprogram(url)

def get_price(url):
    return job(url)





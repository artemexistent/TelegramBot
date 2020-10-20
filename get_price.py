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

    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def exact_url(url):
    index = url.find("B0")
    index = index + 10
    current_url = ""
    current_url = url[:index]
    return current_url


def mainprogram(url):
    # url = "https://www.amazon.com/Bose-QuietComfort-Wireless-Headphones-Cancelling/dp/B0756CYWWD/ref=sr_1_3?dchild=1&fst=as%3Aoff&pf_rd_i=16225009011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=82d03e2f-30e3-48bf-a811-d3d2a6628949&pf_rd_r=MGTEMX5Z31DSRNZVME50&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1486423355&refinements=p_n_shipping_option-bin%3A3242350011&rnid=493964&s=electronics&sr=1-3"
    exacturl = exact_url(url)  # main url to extract data
    page = Page(exacturl)
    soup = bs.BeautifulSoup(page.html, 'html.parser')
    js_test = soup.find('span', id='priceblock_ourprice')
    if js_test is None:
        js_test = soup.find('span', id='priceblock_dealprice')
    str = ""
    for line in js_test.stripped_strings:
        str = line

        # convert to integer
    str = str.replace(", ", "")
    # current_price = int(float(str))
    your_price = 600
    print(str)
    return str



def job(url):
    print("Tracking....")
    return mainprogram(url)

def get_price(url):
    return job(url)





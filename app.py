import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import db_init
import send_email


def search_url(search='python'): #full web scraping

    site = 'http://www.rzeszowiak.pl/Praca-Zatrudnie-3040011505'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 '
                             'Safari/537.17'}
    values = {'z': search}
    data = urllib.parse.urlencode(values)
    url = site + '?' + data
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    resp_data = resp.read()
    parsed_html = BeautifulSoup(resp_data, "lxml")
    listLinks = []

    for div in parsed_html.find_all('div', class_='normalbox-title-left'):
        listLinks.append('http://www.rzeszowiak.pl' + div.a.get('href'))

    return listLinks[::-1]


class DataAdvertisement:
    """

    Scraping important data from advertisement

    """
    def __init__(self, link):
        self.link = link
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko)'
                                      ' Chrome/24.0.1312.27 Safari/537.17'}
        self.req = urllib.request.Request(self.link, headers=self.headers)
        self.resp = urllib.request.urlopen(self.req)
        self.respData = self.resp.read()
        self.parsedHtml = BeautifulSoup(self.respData, "lxml")
        self.value = self.parsedHtml.find_all('div', class_='value')

    def take_title(self):
        title = self.value[1].text
        return title

    def take_date(self):
        date = self.value[2].text[0:17]
        return date

    def take_cash(self):  # salary
        cash = self.value[4].text
        return cash

    def take_content(self):
        cont = self.parsedHtml.find('div', class_='content')
        content = cont.text
        return content


def add_new_records():
    db_init.create_table()
    db_init.clear_new()
    for oneLink in search_url():
        loopLink = DataAdvertisement(oneLink)
        if db_init.find_record(oneLink) is None:
            db_init.data_entry(loopLink.take_title(),loopLink.take_date(), loopLink.take_cash(),
                                          loopLink.take_content(), oneLink)
    send_email.create_msg()  # send email


add_new_records()


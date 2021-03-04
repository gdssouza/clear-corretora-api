import requests
from bs4 import BeautifulSoup

url_login = 'https://login.clear.com.br/pit/login/'

class clear:
    def __init__(self, idNumber, dob, password):
        self._payload = {   'Username': idNumber,\
	                        'DoB':      dob,\
	                        'Password': password, }
        self._session = requests.Session()
        self._session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

    def login(self):
        # construindo _payload
        r = self._session.get(url_login)
        html_doc = r.content
        soup = BeautifulSoup(html_doc,'html.parser')
        self._payload['ClientId'] = soup.find(id='ClientId')['value']
        self._payload['SessionId'] = soup.find(id='sessionId')['value']
        self._payload['__RequestVerificationToken'] = soup.find_all("input")[-1]['value']
        self._payload['RedirectType'] = soup.find(id='RedirectType')['value']
        self._payload['ReturnUrl'] = soup.find(id='ReturnUrl')['value']
        # post 302
        r = self._session.post(url_login, data=self._payload)
        return self._session

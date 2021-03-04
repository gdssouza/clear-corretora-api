import requests
from bs4 import BeautifulSoup

url_login = 'https://login.clear.com.br/pit/login/'
url_token = 'https://login.clear.com.br/pit/login/api/token'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

def read_access(response):
    data = {}
    for item in response.url.split("?")[1].split("&"):
        item = item.split("=")
        key = item[0].lower()
        value = item[1]
        data[key] = value
    return data

class clear:
    def __init__(self, idNumber, dob, password):
        self._payloadLogin = {  'Username': idNumber,\
	                            'DoB':      dob,\
	                            'Password': password, }
        self._session = requests.Session()
        self._session.headers['User-Agent'] = user_agent
        self._dataAccess = {}

    def login(self):
        # construindo payload
        r = self._session.get(url_login)
        html_doc = r.content
        soup = BeautifulSoup(html_doc,'html.parser')
        self._payloadLogin['ClientId'] = soup.find(id='ClientId')['value']
        self._payloadLogin['SessionId'] = soup.find(id='sessionId')['value']
        self._payloadLogin['__RequestVerificationToken'] = soup.find_all("input")[-1]['value']
        self._payloadLogin['RedirectType'] = soup.find(id='RedirectType')['value']
        self._payloadLogin['ReturnUrl'] = soup.find(id='ReturnUrl')['value']
        # post 302
        r = self._session.post(url_login, data=self._payloadLogin)
        # salvando dados de acesso
        self._dataAccess = read_access(r)
        return self._session

    def getDataAccess(self):
        return self._dataAccess

    def token(self):
        # construindo payload
        payload = {'ClientId': self._payloadLogin['ClientId']}
        payload["Source"] = 1
        payload["RefreshToken"] = self._dataAccess['refresh_token']
        # post
        data = self._session.post(url_token, json=payload).json()
        # atualizando dados de acesso
        for key in data: self._dataAccess[key.lower()] = data[key]
        return self._dataAccess

import requests
from bs4 import BeautifulSoup
from API.urls import URL_LOGIN, URL_TOKEN, USER_AGENT

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
        """Clear API

        Args:
            idNumber (string): cpf without dots
            dob (string): dd/mm/yyyy
            password (string): password
        """
        self._payloadLogin = {  'Username': idNumber,\
	                            'DoB':      dob,\
	                            'Password': password, }
        self._session = requests.Session()
        self._session.headers['User-Agent'] = USER_AGENT
        self._dataAccess = {}

    def login(self):
        """Log in to Clear

        Returns:
            requests session: session
        """
        # construindo payload
        r = self._session.get(URL_LOGIN)
        html_doc = r.content
        soup = BeautifulSoup(html_doc,'html.parser')
        self._payloadLogin['ClientId'] = soup.find(id='ClientId')['value']
        self._payloadLogin['SessionId'] = soup.find(id='sessionId')['value']
        self._payloadLogin['__RequestVerificationToken'] = soup.find_all("input")[-1]['value']
        self._payloadLogin['RedirectType'] = soup.find(id='RedirectType')['value']
        self._payloadLogin['ReturnUrl'] = soup.find(id='ReturnUrl')['value']
        # post 302
        r = self._session.post(URL_LOGIN, data=self._payloadLogin)
        # salvando dados de acesso
        self._dataAccess = read_access(r)
        return self._session

    def getDataAccess(self):
        """Last response access data

        Returns:
            dict: Keys:
                        string: acess_token
                        string: token_type
                        string: Bearer
                        string: refresh_toke
                        string: client_id
                        string: login
        """
        return self._dataAccess

    def token(self):
        """Refresh token

        Returns:
            dict: access data updated with the new token 
        """
        # construindo payload
        payload = {'ClientId': self._payloadLogin['ClientId']}
        payload["Source"] = 1
        payload["RefreshToken"] = self._dataAccess['refresh_token']
        # post
        data = self._session.post(URL_TOKEN, json=payload).json()
        # atualizando dados de acesso
        for key in data: self._dataAccess[key.lower()] = data[key]
        return self._dataAccess

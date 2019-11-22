from abc import ABCMeta
import requests
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup
from .Error import IncorrectAssertionError
import re
import sys
import logging

if ((3, 0) <= sys.version_info <= (3, 9)):
    from urllib.parse import urlparse
elif ((2, 0) <= sys.version_info <= (2, 9)):
    from urlparse import urlparse


class ConnectionType(object):
    @staticmethod
    def ntlm():
        # type: () -> str
        return 'ntlm'

    @staticmethod
    def web_form():
        # type: () -> str
        return 'web_form'


class ADFSConnection:
    __metaclass__ = ABCMeta

    def __init__(self, identity_url, username, password):
        # type: (str, str, str) -> None
        self.__annotation = None
        self.__identity_url = identity_url
        self.__username = username
        self.__password = password
        self.logger = logging.getLogger(name='awssaml.ADFSConnection')

    def connect(self):
        pass

    def get_username(self):
        # type: () -> str
        return self.__username

    def get_password(self):
        # type: () -> str
        return self.__password

    def get_assertion(self):
        # type: () -> str
        return self.__assertion

    def get_identity_url(self):
        # type: () -> str
        return self.__identity_url

    def save_assertion(self, response):
        # type: (str) -> None
        # Decode the response and extract the SAML assertion
        soup = BeautifulSoup(response.text, "html.parser")
        self.__assertion = False

        # Look for the SAMLResponse attribute of the input tag (determined by
        # analyzing the debug print lines above)
        for inputtag in soup.find_all('input'):
            if inputtag.get('name') == 'SAMLResponse':
                self.__assertion = inputtag.get('value')

        if not self.__assertion:
            response_error = re.findall(r"\W+<span id=\"errorText\"[\w\ \"=]*>([\w\ \.]+)", response.text)

            self.logger.info("URL: '%s'" % self.get_identity_url())
            self.logger.info("Username, password: '%s', %d digts" % (self.get_username(), len(self.get_password())))
            self.logger.info("Status '%d'" % response.status_code)

            if len(response_error) > 0:
                message = response_error[0]
            else:
                message = response.text

            self.logger.error("Incorrect response. Cannot get Assertion.")
            self.logger.debug("Message: %s" % message)

            raise IncorrectAssertionError(message)


class NtlmADFSConnection(ADFSConnection):
    def connect(self):
        # Initiate session handler
        session = requests.Session()

        # Programmatically get the SAML assertion
        # Set up the NTLM authentication handler by using the provided credential
        session.auth = HttpNtlmAuth(self.get_username(), self.get_password(), session)

        # Opens the initial AD FS URL and follows all of the HTTP302 redirects
        response = session.get(self.get_identity_url(), verify=True)

        if response.status_code == 401:
            print("Incorrect username or password.")
            exit(1)

        if response.status_code != 200:
            print("Incorrect response status code. \nStatus '%d'\nContent:\n" % (response.status_code, response.text))
            exit(1)

        self.save_assertion(response)


class WebFormADFSConnection(ADFSConnection):
    def connect(self):
        # Initiate session handler
        session = requests.Session()

        # Programmatically get the SAML assertion
        # Opens the initial IdP url and follows all of the HTTP302 redirects, and
        # gets the resulting login page
        formresponse = session.get(self.get_identity_url(), verify=True)
        # Capture the idpauthformsubmiturl, which is the final url after all the 302s
        idpauthformsubmiturl = formresponse.url

        # Parse the response and extract all the necessary values
        # in order to build a dictionary of all of the form values the IdP expects
        formsoup = BeautifulSoup(formresponse.text,features="html.parser")
        payload = {}

        for inputtag in formsoup.find_all(re.compile('(INPUT|input)')):
            name = inputtag.get('name','')
            value = inputtag.get('value','')
            if "user" in name.lower():
                #Make an educated guess that this is the right field for the username
                payload[name] = self.get_username()
            elif "email" in name.lower():
                #Some IdPs also label the username field as 'email'
                payload[name] = self.get_username()
            elif "pass" in name.lower():
                #Make an educated guess that this is the right field for the password
                payload[name] = self.get_password()
            else:
                #Simply populate the parameter with the existing value (picks up hidden fields in the login form)
                payload[name] = value

        # Some IdPs don't explicitly set a form action, but if one is set we should
        # build the idpauthformsubmiturl by combining the scheme and hostname
        # from the entry url with the form action target
        # If the action tag doesn't exist, we just stick with the
        # idpauthformsubmiturl above
        for inputtag in formsoup.find_all(re.compile('(FORM|form)')):
            action = inputtag.get('action')
            loginid = inputtag.get('id')
            if (action and loginid == "loginForm"):
                parsedurl = urlparse(self.get_identity_url())
                idpauthformsubmiturl = parsedurl.scheme + "://" + parsedurl.netloc + action

        # Performs the submission of the IdP login form with the above post data
        response = session.post(
            idpauthformsubmiturl, data=payload, verify=True)

        self.save_assertion(response)



import requests
import base64
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


class ADFSService:
    assertion: str

    def __init__(self, identity_url: str):
        self.identity_url = identity_url

    def connect(self, username: str, password: str):
        # Initiate session handler
        session = requests.Session()

        # Programmatically get the SAML assertion
        # Set up the NTLM authentication handler by using the provided credential
        session.auth = HttpNtlmAuth(username, password)

        # Opens the initial AD FS URL and follows all of the HTTP302 redirects
        response = session.get(self.identity_url, verify=True)

        # Decode the response and extract the SAML assertion
        soup = BeautifulSoup(response.text, "html.parser")
        self.assertion = ''

        # Look for the SAMLResponse attribute of the input tag (determined by
        # analyzing the debug print lines above)
        for inputtag in soup.find_all('input'):
            if inputtag.get('name') == 'SAMLResponse':
                self.assertion = inputtag.get('value')

    def get_assertion(self):
        return self.assertion

    def get_aws_roles(self):
        # Parse the returned assertion and extract the authorized roles
        awsroles = []
        root = ET.fromstring(base64.b64decode(self.assertion))

        for saml2attribute in root.iter('{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
            if saml2attribute.get('Name') == 'https://aws.amazon.com/SAML/Attributes/Role':
                for saml2attributevalue in saml2attribute.iter('{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
                    awsroles.append(saml2attributevalue.text)

        # Note the format of the attribute value should be role_arn,principal_arn
        # but lots of blogs list it as principal_arn,role_arn so let's reverse
        # them if needed
        for awsrole in awsroles:
            chunks = awsrole.split(',')
            if'saml-provider' in chunks[0]:
                newawsrole = chunks[1] + ',' + chunks[0]
                index = awsroles.index(awsrole)
                awsroles.insert(index, newawsrole)
                awsroles.remove(awsrole)

        return awsroles

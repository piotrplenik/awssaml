import requests
import base64
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from .ADFSConnection import ConnectionType, ADFSConnection, NtlmADFSConnection, WebFormADFSConnection


class ADFSService:
    def __init__(self, identity_url):
        # type: (str) -> None
        self.identity_url = identity_url
        self.connection = None

    def connect(self, type_name, username, password):
        # type: (str, str, str) -> None
        if type_name == ConnectionType.web_form():
            self.connection = WebFormADFSConnection(self.identity_url, username, password)
        else:
            self.connection = NtlmADFSConnection(self.identity_url, username, password)

        self.connection.connect()

    def get_aws_roles(self):
        # Parse the returned assertion and extract the authorized roles
        awsroles = []
        root = ET.fromstring(base64.b64decode(self.connection.get_assertion()))

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

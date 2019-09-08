import configparser
from os.path import expanduser, isfile


class AwsCredentials:
    aws_credentials_section: str
    aws_credentials_file: str = '/.aws/credentials'

    credentials = None

    def __init__(self, section: str = 'saml'):
        self.aws_credentials_section = section

        home = expanduser("~")

        credentials_filename = home + self.aws_credentials_file
        if isfile(credentials_filename):
            credentials = configparser.RawConfigParser()
            credentials.read(home + self.aws_credentials_file)
            self.credentials = credentials

    def get_section(self):
        return self.aws_credentials_section

    def set_output(self, value):
        self.__set_config('output', value)

    def set_region(self, value):
        self.__set_config('region', value)

    def set_access_key_id(self, value):
        self.__set_config('aws_access_key_id', value)

    def set_secret_access_key(self, value):
        self.__set_config('aws_secret_access_key', value)

    def set_session_token(self, value):
        self.__set_config('aws_session_token', value)

    def save(self):
        home = expanduser("~")

        credentials_filename = home + self.aws_credentials_file

        with open(credentials_filename, 'w+') as configfile:
            self.credentials.write(configfile)

    def __set_config(self, name, value):
        if not self.credentials.has_section(self.aws_credentials_section):
            self.credentials.add_section(self.aws_credentials_section)

        self.credentials.set(self.aws_credentials_section, name, value)

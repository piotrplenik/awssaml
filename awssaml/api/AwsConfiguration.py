import configparser
from os.path import expanduser, isfile


class AwsConfiguration:
    aws_config_file = '/.aws/config'
    aws_config_section = 'samlapi'

    config = None
    credentials = None
    profile = None

    def __init__(self, profile: str = None):
        home = expanduser("~")

        if not isfile(self.__get_config_filename()):
            self.print_configuration_instruction()
            exit(1)

        config = configparser.RawConfigParser()
        config.read(home + self.aws_config_file)
        self.config = config
        self.profile = profile

    def get_username(self):
        return self.__get_config_value('username')

    def get_pep_file(self):
        return self.__get_config_value('pemfile')

    def get_password_file(self):
        return self.__get_config_value('password_file')

    def get_identity_url(self):
        url = self.__get_config_value('identity_url')

        if url is None:
            self.print_configuration_instruction()
            exit(1)

        return url

    def get_region(self):
        region = self.__get_config_value('region')

        if region is None:
            region = "eu-west-1"

        return region

    def get_role_arn(self):
        return self.__get_config_value('role_arn')

    def get_principal_arn(self):
        return self.__get_config_value('principal_arn')

    def get_source_profile(self):
        return self.__get_profile_config_value('source_profile')

    def get_session_duration(self):
        duration = self.__get_config_value('session_duration')

        if duration is None:
            return 3600

        return int(duration)

    def get_profiles_by_arn(self):
        profiles = self.get_profiles()

        return dict(map(lambda profile: (self.__get_profile_config_value('role_arn', profile), profile), profiles))

    def get_profiles(self):
        profiles = list(filter(lambda x: x.startswith('profile '), self.config.sections()))

        return list(map(lambda x: x[8:], profiles))

    def print_configuration_instruction(self):
        # Give the user some basic info as to what has just happened
        print('Missing `awssaml` configuration.')
        print('\nPlease setup `%s` configuration file, and provide:' % self.__get_config_filename())
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('[samlapi]')
        print('identity_url = https://adfs.example.com/adfs/ls/IdpInitiatedSignOn.aspx?loginToRp=urn:amazon:webservices')
        print('region = eu-west-1')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('\nWhere:')
        print(' - `identity_url` is AD FS 2.0 URL. ')
        print(' - `region` is your default region. ')
        print('\nFor more information see:')
        print('\thttps://aws.amazon.com/blogs/security/'
              'how-to-implement-federated-api-and-cli-access-using-saml-2-0-and-ad-fs/\n')

    def __get_config_filename(self):
        home = expanduser("~")

        return home + self.aws_config_file

    def __get_config_value(self, name: str):
        value = self.__get_profile_config_value(name)

        if not value:
            value = self.__get_section_config_value(name)

        return value

    def __get_profile_config_value(self, name: str, profile: str = None):
        if not profile:
            profile = self.profile

        profile_key = 'profile %s' % profile if profile and self.config.has_section('profile %s' % profile) else None

        if self.config is None:
            return None

        if profile_key and self.config.has_option(profile_key, name):
            return self.config.get(profile_key, name)

        return None

    def __get_section_config_value(self, name: str):
        section = self.aws_config_section

        if not self.config.has_section(section):
            return None

        if not self.config.has_option(section, name):
            return None

        return self.config.get(section, name)
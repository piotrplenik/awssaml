from __future__ import print_function
import sys
from .AwsConfiguration import AwsConfiguration
from .ADFSService import ADFSService
from .AwsStsService import AwsStsService
from getpass import getpass
from .Error import IncorrectAssertionError
import keyring


class Authentication:
    def __init__(self, profile=None):
        # type: (str) -> None
        self.configuration = AwsConfiguration(profile)
        self.service = ADFSService(self.configuration.get_identity_url())
        self.profile = profile
        keyring.get_keyring()

    def authenticate(self):
        username = self.get_username()

        connected = False
        force_ask = False
        for x in range(0, 3):
            if not connected:
                try:
                    password = self.get_password(force_ask=force_ask)
                    connection = self.get_connection()
                    self.service.connect(connection, username, password)
                    connected = True
                except IncorrectAssertionError as err:
                    print("Error: %s" % err.message)
                    force_ask = True
                    connected = False

        if not connected:
            print("Exiting")
            exit(1)

        role_principal_arn = self.get_role_principal_arn()
        role_arn = role_principal_arn[0]
        principal_arn = role_principal_arn[1]
        session_duration = self.configuration.get_session_duration()

        print('Role ARN: {0}'.format(role_arn))
        print('Principal ARN: {0}'.format(principal_arn))
        print('Session duration: {0}sec'.format(session_duration))

        # Use the assertion to get an AWS STS token using Assume Role with SAML
        sts = AwsStsService()
        sts.sign_in(
            issuer=self.configuration.get_identity_url(),
            role_arn=role_arn,
            principal_arn=principal_arn,
            saml_assertion=self.service.connection.get_assertion(),
            duration_seconds=session_duration,
            region=self.configuration.get_region()
        )

        return sts

    def get_username(self):
        username = self.configuration.get_username()

        if username:
            print("Saved username: '%s'" % username)
            return username

        print("Username: ", end=" ")
        return input()

    def get_password(self, force_ask=False):
        password = None

        if not force_ask:
            password = keyring.get_password("awssaml", "saml-password")

        if not password:
            password = getpass(prompt='Password: ')
            keyring.set_password("awssaml", "saml-password", password)
            print('Password saved.')
        else:
            print('Use saved password.')

        return password

    def get_role_principal_arn(self):
        if self.configuration.get_role_arn() is not None and self.configuration.get_principal_arn() is not None:
            print('Use ARN from "{0}" configuration file.'.format(self.configuration.aws_config_file))

            return [
                self.configuration.get_role_arn(),
                self.configuration.get_principal_arn()
            ]
        else:
            awsroles = self.service.get_aws_roles()
            profiles = self.configuration.get_profiles_by_arn()

            # If I have more than one role, ask the user which one they want,
            # otherwise just proceed
            print("")
            if len(awsroles) > 1:
                i = 0
                print("Please choose the role you would like to assume:")
                for awsrole in awsroles:
                    role_name = awsrole.split(',')[0]
                    if role_name in profiles.keys():
                        role_name = '%s (profile: %s)' % (role_name, profiles[role_name])
                    print('[%d]: %s' % (i, role_name))
                    i += 1

                print("Selection: ")
                selectedroleindex = input()

                # Basic sanity check of input
                if int(selectedroleindex) > (len(awsroles) - 1):
                    print('You selected an invalid role index, please try again')
                    sys.exit(0)

                return awsroles[int(selectedroleindex)].split(',')

            else:
                return awsroles[0].split(',')

    def get_source_profile(self):
        # type: () -> str
        profile = self.configuration.get_source_profile()
        if profile:
            return profile

        return "saml"

    def get_connection(self):
        # type: () -> str
        value = self.configuration.get_connection_type()

        connection = value.lower() if value else 'ntlm'

        print("Connection: '%s'" % connection)

        return connection

import sys
from .AwsConfiguration import AwsConfiguration
from .ADFSService import ADFSService
from .AwsStsService import AwsStsService
from .PasswordDecrypt import decrypt


class Authentication:
    configuration: AwsConfiguration
    service: ADFSService
    profile: str = None

    def __init__(self, profile: str = None):
        self.configuration = AwsConfiguration(profile)
        self.service = ADFSService(self.configuration.get_identity_url())
        self.profile = profile

    def authenticate(self):
        username = self.get_username()
        password = self.get_password()

        self.service.connect(username, password)

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
            saml_assertion=self.service.get_assertion(),
            duration_seconds=session_duration,
            region=self.configuration.get_region()
        )

        return sts

    def get_username(self):
        username = self.configuration.get_username()

        if username:
            print("Username: '%s'" % username)
            return username

        print("Username: ")
        return input()

    def get_password(self):
        if self.configuration.get_pep_file() and self.configuration.get_password_file():
            print("Password: <hidden>")
            return decrypt(self.configuration.get_password_file(), self.configuration.get_pep_file())

        print("Password: ")
        return input()

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
        profile = self.configuration.get_source_profile()
        if profile:
            return profile

        return "saml"
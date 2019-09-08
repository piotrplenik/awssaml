"""Api command"""

from .Base import Base
import platform
from awssaml.api.Authentication import Authentication
from awssaml.api.AwsCredentials import AwsCredentials


class ApiCommand(Base):
    """Say hello, world!"""

    def run(self):
        authentication = Authentication(self.get_profile())
        sts = authentication.authenticate()

        aws_credentials = AwsCredentials(authentication.get_source_profile())

        # Put the credentials into a specific profile instead of clobbering
        # the default credentials
        aws_credentials.set_output('json')
        aws_credentials.set_region(sts.get_region())
        aws_credentials.set_access_key_id(sts.credentials['AccessKeyId'])
        aws_credentials.set_secret_access_key(sts.credentials['SecretAccessKey'])
        aws_credentials.set_session_token(sts.credentials['SessionToken'])
        aws_credentials.save()

        type = "set" if platform.system() == "Windows" else "export"

        # Give the user some basic info as to what has just happened
        print('\n----------------------------------------------------------------')
        print('Your new access key pair has been stored in the AWS configuration file {0} under the {1} profile.'
              .format(aws_credentials.aws_credentials_file, aws_credentials.get_section()))
        print('Note that it will expire at {0}.'.format(sts.credentials['Expiration']))
        print('After this time you may safely rerun this script to refresh your access key pair.')
        print('To use this credential:')
        print(' - call the AWS CLI with the --profile option (e.g. `aws --profile %s ec2 describe-instances`);'
              % aws_credentials.get_section())
        print(' - set environment variable (e.g. `%s AWS_PROFILE=%s`).'
              % (type, aws_credentials.get_section()))
        print('----------------------------------------------------------------')

import sys
import boto3
import json
import requests

if ((3, 0) <= sys.version_info <= (3, 9)):
    from urllib.parse import quote
elif ((2, 0) <= sys.version_info <= (2, 9)):
    from urllib import pathname2url as quote


class AwsStsService:
    signin_token = []
    credentials = []

    def sign_in(self, issuer, role_arn, principal_arn, saml_assertion, duration_seconds, region):
        # type: (str, str, str, str, int, str) -> None

        self.issuer = None
        self.region = None

        conn = boto3.client('sts')

        token = conn.assume_role_with_saml(
            RoleArn=role_arn,
            PrincipalArn=principal_arn,
            SAMLAssertion=saml_assertion,
            DurationSeconds=duration_seconds
        )

        credentials = token['Credentials']

        temporary_credentils = (
            '{{'
            '"sessionId":"{}",'
            '"sessionKey":"{}",'
            '"sessionToken":"{}"'
            '}}'
        ).format(credentials['AccessKeyId'], credentials['SecretAccessKey'], credentials['SessionToken'])

        request_url = (
            "https://signin.aws.amazon.com/federation"
            "?Action=getSigninToken"
            "&SessionDuration={}"
            "&Session={}"
        ).format(duration_seconds, quote(temporary_credentils))

        r = requests.get(request_url)

        # Returns a JSON document with a single element named SigninToken.
        self.issuer = issuer
        self.signin_token = json.loads(r.text)
        self.credentials = credentials
        self.region = region

    def get_console_url(self):
        request_url = (
            'https://signin.aws.amazon.com/federation'
            '?Action=login'
            '&Issuer={}'
            '&Destination={}'
            '&SigninToken={}'
        ).format(
            quote(self.issuer),
            quote("https://console.aws.amazon.com/"),
            self.signin_token["SigninToken"]
        )

        return request_url

    def get_credentials(self):
        # type: () -> str
        return self.credentials

    def get_region(self):
        # type: () -> str
        return self.region




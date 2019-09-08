import boto3
import json
import requests
from urllib import parse


class AwsStsService:
    signin_token = []
    credentials = []
    issuer: str
    region: str

    def sign_in(self, issuer: str, role_arn: str, principal_arn: str, saml_assertion: str, duration_seconds: int,
                region: str):
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
        ).format(duration_seconds, parse.quote_plus(temporary_credentils))

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
            parse.quote_plus(self.issuer),
            parse.quote_plus("https://console.aws.amazon.com/"),
            self.signin_token["SigninToken"]
        )

        return request_url

    def get_credentials(self):
        return self.credentials

    def get_region(self):
        return self.region




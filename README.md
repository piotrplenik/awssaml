# Purpose

Access to the AWS Management Console and AWS API for my Active Directory users using federation (AD FS).

# Usage

## Requirements

 - Linux (not tested on Windows OS, hope work)
 - Python 3 - [latest version 3.x](https://www.python.org/downloads/)

## Installation

> pip3 install -i https://test.pypi.org/simple/ awssaml

## Configuration file
~~~~
> nano ~/.aws/config

[samlapi]
identity_url = https://adfs.example.com/adfs/ls/IdpInitiatedSignOn.aspx?loginToRp=urn:amazon:webservices
region = eu-west-1

username = [SAML User]
pemfile = [pem filename]
password_file = /home/[username]/.aws/secret      # This is secret file for decrypt your password
~~~~

## Usage

## Access to AWS Console

~~~~
> awssaml console
~~~~

## Get AWS Api Credentials

~~~~
> awssaml api
~~~~


## Setup automatic login

1. Generate your private RSA key (there is a lot [documentation](https://support.microfocus.com/kb/doc.php?id=7013103) how to do it) 
2. Execute "set-samlapi-access.py" to safe your credentials:
~~~~
> python3 set-samlapi-access.py
Full path to your PEM file: C:\<full-path-to-your-file>.pem
Username: <SAML User>
Password:
Configuration updated.
~~~~

## Setup static ARN

To set manual set to your credentials:
````
[samlapi.py]
username = ....
pemfile = ....
password = ....
manual_role_arn = arn:aws:iam::[ID]:role/[role]
manual_principal_arn = arn:aws:iam::[ID]:saml-provider/[provider]
````

## More information
 - [How to Implement Federated API](https://aws.amazon.com/blogs/security/how-to-implement-federated-api-and-cli-access-using-saml-2-0-and-ad-fs/)
 - [How to grant my Active Directory users access to the API or AWS CLI with AD FS?](https://aws.amazon.com/premiumsupport/knowledge-center/adfs-grant-ad-access-api-cli/)
 
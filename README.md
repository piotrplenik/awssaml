# Purpose

Access to the AWS Management Console and AWS API for my Active Directory users using federation (AD FS).

# Usage

## Requirements

 - Linux (not tested on Windows OS, hope work)
 - Python - [latest version 3.x](https://www.python.org/downloads/)
 - A minimal [AWS credentials file](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) 
   (for example, `~/.aws/credentials`)

## Install all requirements

> pip3 install -r requirements.txt

## Configuration file
~~~~
> nano ~/.aws/config

[samlapi]
identity_url = https://adfs.example.com/adfs/ls/IdpInitiatedSignOn.aspx?loginToRp=urn:amazon:webservices
region = eu-west-1

username = [AD username]
pemfile = [pem filename]
password_file = /home/[username]/.aws/secret      # This is secret file for decrypt your password
~~~~

~~~~
> nano ~/.aws/credentials
...
[default]
output = json
region = eu-west-1
aws_access_key_id = 
aws_secret_access_key = ap-southeast-2

[saml]
output = json
region = eu-west-1
aws_access_key_id = x
aws_secret_access_key = x
aws_session_token = x

~~~~

## Executable

~~~~
> python3 samlapi
Username: `<SAML User>`
Password: `<SAML Password>`

Please choose the role you would like to assume:
[ 0 ]:  arn:aws:iam::123456789012:role/ADFS-DevAdmin
Selection:  0

----------------------------------------------------------------
Your new access key pair has been stored in the AWS configuration file `~/.aws/credentials` under the saml profile.
Note that it will expire at 2018-12-27T15:53:43Z.
After this time you may safely rerun this script to refresh your access key pair.
To use this credential call the AWS CLI with the `--profile` option (e.g. `aws --profile saml ec2 describe-instances`).
----------------------------------------------------------------
~~~~

Or try to refresh API key every 55 minutes (3300 seconds)

~~~~
> watch -n 3300 samlapi
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
 
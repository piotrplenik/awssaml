# Purpose

Access to the AWS Management Console and AWS API for my Active Directory users using federation (AD FS).

# Usage

## Requirements

 - Linux (tested on Ubuntu 19.04+) or Windows (tested on 10)
 - Python 3 - [latest version 3.x](https://www.python.org/downloads/)
 - on Windows, `pycrypto` require [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/downloads/)

## Installation

> pip3 install awssaml

## Configuration file

All configuration is stored in `~/.aws/config` file. 

#### Basic configuration
~~~~
[samlapi]
identity_url = https://adfs.example.com/adfs/ls/IdpInitiatedSignOn.aspx?loginToRp=urn:amazon:webservices
region = eu-west-1
~~~~

#### Advanced samlapi configuration 

##### Default username
~~~~
[samlapi]
#...
username = [SAML User]
~~~~

#### Default session duration
Setup 12 hours (it's 43200 seconds): 
~~~~
[samlapi]
#...
session_duration = 43200
~~~~

#### Keep encrypted password

To generate password, use `set-samlapi-access.py` script. 
Application store password encrypted, using PEM certificate.

Before you use script, generate your private RSA key  ([more info](https://support.microfocus.com/kb/doc.php?id=7013103))

~~~~
> python3 set-samlapi-access.py
Full path to your PEM file: <full-path-to-your-file>.pem
Username: <SAML User>
Password:
Configuration updated.
~~~~

#### Advanced profile configuration 

You can setup custom profiles to reuse. 
Sample configuration entry for profile:

~~~~
[profile nonprod-application1]
role_arn = arn:aws:iam::[ID]:role/[role]
principal_arn = arn:aws:iam::[ID]:saml-provider/[provider]
source_profile = nonprod
session_duration = 43200
~~~~

Usage:
~~~~
> awssaml api nonprod-application1
> awssaml console nonprod-application1
~~~~

## Reference
 - [How to Implement Federated API](https://aws.amazon.com/blogs/security/how-to-implement-federated-api-and-cli-access-using-saml-2-0-and-ad-fs/)
 - [How to grant my Active Directory users access to the API or AWS CLI with AD FS?](https://aws.amazon.com/premiumsupport/knowledge-center/adfs-grant-ad-access-api-cli/)
 
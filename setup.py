#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

requires = [
    "docopt>=0.6.0,<=0.6.2",
    "Crypto>=1.4.1,<1.5.0",
    "beautifulsoup4>=4.7.1,<4.8.0",
    "requests-ntlm>=1.1.0,<1.2.0",
    "pycryptodome>=3.8.2,<3.9.0",
    "requests>=2.22.0,<2.23.0",
    "configparser>=3.7.4,<3.8.0",
    "boto3>=1.9.184,<1.10.0"
]

setup(
    name="awssaml",
    version="0.0.14",
    author="Piotr Plenik",
    author_email="piotr.plenik@gmail.com",
    description="Security Assertion Markup Language (SAML) for Amazon.",
    long_description=long_description,
    include_package_data=True,
    long_description_content_type="text/markdown",
    url="https://github.com/jupeter/awssaml",
    packages=find_packages(),
    scripts=['bin/awssaml'],
    install_requires=requires,
    entry_points={
        "console_scripts": [
            "awssaml=awssaml.__main__:main"
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Utilities',
    ]
)
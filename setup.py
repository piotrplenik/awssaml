#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

requires = [
    "docopt>=0.6.0,<=0.6.2"
]

setup(
    name="aws-saml",
    version="0.0.7",
    author="Piotr Plenik",
    author_email="piotr.plenik@gmail.com",
    description="Security Assertion Markup Language (SAML) for Amazon.",
    long_description=long_description,
    include_package_data=True,
    long_description_content_type="text/markdown",
    url="https://github.com/jupeter/awssaml",
    packages=['awssaml', 'awssaml.api', 'awssaml.commands'],
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
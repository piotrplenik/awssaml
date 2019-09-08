import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

requires = [
    "docopt>=0.6.0,<=0.6.2"
]

packages = [
    "client",
    "client.commands",
    "client.helpers"
]

setuptools.setup(
    name="aws-saml",
    version="1.0.0",
    author="Piotr Plenik",
    author_email="piotr.plenik@gmail.com",
    description="Security Assertion Markup Language (SAML) for Amazon.",
    long_description=long_description,
    include_package_data=True,
    long_description_content_type="text/markdown",
    url="https://github.com/jupeter/awssaml",
    packages=packages,
    install_requires=requires,
    entry_points={
        "console_scripts": [
            "client=client.__main__:main"
        ]
    }
)
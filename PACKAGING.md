# Deploy new version

~~~~
> python3 setup.py bdist_wheel --universal
> python3 -m keyring set https://upload.pypi.org/legacy/ your-username
> twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
~~~~
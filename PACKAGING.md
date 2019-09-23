# Deploy new version

~~~~
> python3 setup.py bdist_wheel --universal
> twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
~~~~
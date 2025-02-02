To start to contribute, install the dependencies (Python >= 3.11)
```
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt -r test-requirements.txt
```

Fork this repository, make the changes into the forked repository and push a new Merge Request to 'main' branch.
Open an issue in case of big MRs.

## Install pre-commit

It formats the code on each commit.

```
pre-commit install
```

## Testing

```
python -m pytest
```

## Linter
```
flake8 --exclude venv,.tox --max-line-length 100
```

# Tox
Use tox to run the unit tests and linter
```
tox
```


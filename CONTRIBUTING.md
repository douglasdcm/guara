To start to contribute, install the dependencies (Python >= 3.11)
```
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt -r test-requirements.txt
```

Fork this repository, make the changes into the forked repository and push a new Merge Request to 'main' branch.
Open an issue in case of big MRs.

## Testing

```
python -m pytest
```

## Linter
```
flake8 --exclude venv --max-line-length 100
```


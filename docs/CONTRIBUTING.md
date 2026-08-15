# Contributing

Fork this repository, make the changes into the forked repository and push a new Merge Request to 'main' branch.
Open an issue in case of big MRs.

## Install pre-commit

To start to contribute, install the dependencies (Python >= 3.8)

```bash
make install
```

## Testing

```bash
make test
```

## Linter
```bash
make linter
```

## List commands
```bash
make
```

Output
```
  make install             - Setup venv and install dependencies
  make test                - Run unit tests using pytest
  make linter              - Run linter via tox
  make tox                 - Run entire test and linter suite via tox
  make all                 - Run all commands
```

## Building documentation
```bash
cd doc
rm -rf _build/; make html; xdg-open _build/html/index.html
```
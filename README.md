# dev_python

## Initialization
Site: https://pipenv.pypa.io/

On PyPI: https://pypi.org/project/pipenv/
```bash
pipenv install --dev
```

## Tests
Site: https://docs.pytest.org/

On PyPI: https://pypi.org/project/pytest/

**Run tests**
```bash
PYTHONPATH=. pipenv run pytest --verbose --full-trace -r A
```

**Script encapsulation**
Run [script](./run_tests.sh)
```bash
./run_tests.sh
```

## Coverage
Site: https://coverage.readthedocs.io/

On PyPI: https://pypi.org/project/coverage/

Configuration in: [`.coveragerc`](./.coveragerc) file

**Run coverage**
Based on pytest
```bash
PYTHONPATH=. pipenv run coverage run -m pytest --verbose --tb=long -r A
```

**View text report**
```bash
pipenv run coverage report -m
```

**Run coverage and generate XML report**
```bash
pipenv run pytest --cov-config=./.coveragerc --cov-report xml:./coverage.xml --cov mydict --cov myexec
```

**Generate HTML report and see it**
```
pipenv run coverage html
firefox htmlcov/index.html
```

**Script encapsulation**
Run [script](./run_coverage.sh)
```bash
./run_coverage.sh
```

## Visual Studio Code parameters
```json
{
    "files.associations": {
        "*.env": "shellscript",
        ".coveragerc": "toml"
    },
    "python.languageServer": "Pylance",
    "shellcheck.customArgs": [
        "-x"
    ],
    "python.analysis.inlayHints.variableTypes": true,
    "python.analysis.inlayHints.functionReturnTypes": true,
    "python.linting.flake8Args": [
        "--max-line-length",
        "150",
        "--verbose"
    ],
    "[python]": {
        "editor.formatOnType": true
    },
    "python.linting.flake8Enabled": true
}
```

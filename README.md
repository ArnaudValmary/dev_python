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
pipenv run pytest --cov-config=./.coveragerc --cov-report xml:./coverage.xml --cov .
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

## Visual Studio Code

### Extensions
* Python
    * [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    * [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
    * [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)
    * [autopep8](https://marketplace.visualstudio.com/items?itemName=ms-python.autopep8)
    * [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)
    * [Python Environment Manager](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-environment-manager)
* Shell
    * [ShellCheck](https://marketplace.visualstudio.com/items?itemName=timonwong.shellcheck)
* TOML
    * [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml)
* Others
    * [Render Line Endings](https://marketplace.visualstudio.com/items?itemName=medo64.render-crlf)
    * [Todo Tree](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree)

### Parameters
```json
{
    "files.associations": {
        "*.env": "shellscript",
        ".coveragerc": "toml"
    },

    // EOL
    "code-eol.decorateBeforeEol": true,
    "code-eol.highlightExtraWhitespace": true,

    // Python
    "python.defaultInterpreterPath": "/usr/bin/python",
    "python.languageServer": "Pylance",
    "python.analysis.inlayHints.variableTypes": true,
    "python.analysis.inlayHints.functionReturnTypes": true,

    // Python linting
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--max-line-length", "150",
        "--verbose"
    ],

    // Python formatting
    "[python]": {
        "editor.formatOnType": true,
        "editor.defaultFormatter": "ms-python.autopep8",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        },
    },
    "isort.args": [
        "--profile", "black"
    ],

    // ShellCheck
    "shellcheck.customArgs": [
        "-x"
    ],

    // TOML
    "evenBetterToml.formatter.arrayAutoCollapse": false,
    "evenBetterToml.formatter.allowedBlankLines": 1,
    "evenBetterToml.formatter.columnWidth": 120
}
```

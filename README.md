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
PYTHONPATH=. pipenv run pytest --verbose --tb=long -r A
```
or run [script](./run_tests.sh)
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

**Generate HTML report and see it**
```
pipenv run coverage html
firefox htmlcov/index.html
```
or run [script](./run_coverage.sh)
```bash
./run_coverage.sh
```

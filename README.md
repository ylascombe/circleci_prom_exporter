
# Dev Setup

## Create virtual env and install deps
```
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Tests

```
python3 -m unittest tests/prom_circleci_test.py
```

# Local launch

```
export CIRCLECI_TOKEN=xxxx
python3 app.py
```

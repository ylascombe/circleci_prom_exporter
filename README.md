
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
export CIRCLECI_CONTAINER_NAMESPACE=yyy
python3 app.py
```

Go to http://127.0.0.1:8000
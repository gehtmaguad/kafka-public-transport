# Start Services

## Install Dependencies
* Make sure docker is installed
* Install Python on Mac with `brew install python@3.7`
* Install virtualenv with Python Package Manager `pip install virtualenv`

## Run containers
* `docker-compose up`

## Run `producer`:

1. `cd producers`
2. `virtualenv -p /usr/local/opt/python@3.7/bin/python3 venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python simulation.py`

#### Run Faust Stream Processing Application:
1. `cd consumers`
2. `virtualenv -p /usr/local/opt/python@3.7/bin/python3 venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `faust -A faust_stream worker -l info`

#### Run the KSQL Creation Script:
1. `cd consumers`
2. `virtualenv -p /usr/local/opt/python@3.7/bin/python3 venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python ksql.py`

#### Run the `consumer`:
1. `cd consumers`
2. `virtualenv -p /usr/local/opt/python@3.7/bin/python3 venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python server.py`

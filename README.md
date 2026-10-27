# Orders service exercise

## What do you need to do

You need to implement Orders service lookup API. This repo serves as a template:
- it has defined but not implemented API endpoints in `app/api.py`
- db models are not defined (`app/models.py`)
- incoming data examples you can find in `app/consumer.py`
- db session is configured for the app and tests

Focus on implementing:
- `app/api.py`
- `app/models.py`
- and anything else you think is relevant

## Setup and tests
Install Python 3.11 or newer. 

macOS/Linux:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pytest -q
```

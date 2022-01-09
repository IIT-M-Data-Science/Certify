# Certify
IITM-POD Certificate Verification System Portal


# Setup
Require **Python 3.8+**. Create a virtualenv,

```bash
python -m virtualenv env
cd env
```

Install [Poetry](https://python-poetry.org/) (`pip install poetry`), and run poetry to install dependencies.

```bash
poetry install
```

Deploy the server using `uvicorn`

```bash
uvicorn main:app
```
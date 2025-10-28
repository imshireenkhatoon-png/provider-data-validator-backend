# Provider Data Validator Backend

A Flask-based mock backend for validating healthcare provider data for hackathon MVP.

## Setup

```bash
pip install -r requirements.txt
export FLASK_APP=app/app.py
flask run
```

## Endpoints
- `/health`
- `/upload` — upload CSV (Name, Phone, Address, Specialty)
- `/report` — generate PDF summary
- `/summary` — aggregated stats

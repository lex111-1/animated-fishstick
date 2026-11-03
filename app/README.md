Simple overwatch self-match tracker

Can POST matches like:

```bash
curl -X POST http://127.0.0.1:5000/matches \
  -H "Content-Type: application/json" \
  -d '{"hero": "Tracer", "map": "Hanamura", "time": 12, "date": "2026-11-03", "outcome": "win"}'
```

Matches will be saved to a .db and can be viewed at  `/stats/view`

legacy page (nofrontend) at `/stats`

The frontend (template + css for /stats/view) were generated with Claude code, the backend database and tests are my own work

# Setup

Create and activate a python venv, then run `pip install -r requirements.txt`

Run `flask --app app run`

To run the tests `pytest -v`

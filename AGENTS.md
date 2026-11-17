# hakuchat

Single-file Python script: `weather.py` calls OpenRouter (OpenAI-compatible client) with a weather function tool.

## Run

```bash
source .venv/bin/activate        # or: .venv\Scripts\activate on Windows
pip install openai               # no requirements.txt; install on first run
export OPEN_ROUTER_UUS="sk-or-..."   # weather.py:24 reads this exact var name
python weather.py
```

## Gotchas

- `api.env` defines `OPENROUTER_API_KEY`, but `weather.py` reads `OPEN_ROUTER_UUS` — they do not match. Set `OPEN_ROUTER_UUS` in the shell or a `.env` file (both are gitignored).
- Model is hardcoded: `nvidia/nemotron-3.5-super-vl:free` (weather.py:28), base URL `https://openrouter.ai/api/v1` (weather.py:23).
- `.venv/`, `__pycache__/`, and `.env` are gitignored; `api.env` is tracked.

## No

No tests, lint, typecheck, CI, README, or packaging config exist in this repo. Don't look for them.

## Säännöt
Tietoturvasäännöt: 1. web_search käyttää AINA subprocess.run-kutsua listamuodossa, EI KOSKAAN shell=True. 2. Hakusanat on URL-enkoodattava. 3. Curl-kutsuilla on oltava 10 sekunnin aikaraja (--max-time 10). 4. Tool use -silmukka saa pyöriä enintään 5 kierrosta. 5. API-avain luetaan AINA ympäristömuuttujasta (os.environ.get).
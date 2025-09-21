# LaunchPad AI Decision Engine (FastAPI + OpenAI)

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add OPENAI_API_KEY (optional for offline demo)
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Place your source docs at repo root:
```
VUE Services 2026.docx
Biases.docx
VUE_Services_SKU_Prices.xlsx  # optional
```
Then build KB:
```bash
curl -X POST http://localhost:8000/admin/reload-kb
```

### Endpoints
- `POST /intake/lighting`
- `POST /intake/deep-dive`
- `POST /export/docx`
- `GET /schemas`
- `GET /healthz`

### Wix Velo integration
See README body in chat message (omitted here for brevity).

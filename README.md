# Voice-Activated Image Search System via Real-Time Speech Recognition

## Quickstart
```bash
pip install -r requirements.txt
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gcp/keys/<your-key>.json"
uvicorn backend.fastapi_server_google_cloud_stt:app --reload
```

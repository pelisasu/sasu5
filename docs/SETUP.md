# SETUP

## 1. Telegram
Buat bot melalui BotFather, ambil token, lalu dapatkan chat ID.
Masukkan sebagai GitHub Secrets:
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

## 2. OpenAI
Opsional. Jika diaktifkan, AI menjadi validator ketat. Masukkan:
- OPENAI_API_KEY
- OPENAI_MODEL

Jangan commit API key ke repository.

## 3. GitHub Actions
Pastikan Actions enabled. Jalankan `Tests` dulu. Setelah itu jalankan `XAUUSD AI Signal Scan` manual sekali.

Schedule:
- 07,22,37,52 setiap jam UTC
- Senin-Jumat
- 15-minute cadence, offset 7 minutes untuk menghindari top-of-hour congestion.

## 4. Secret/state
GitHub-hosted runners are ephemeral. `state.json` and `journal.jsonl` are local to a run and are not persistent across scheduled jobs unless explicitly stored as an artifact/cache/database. Therefore the included workflow is a stateless scanner. For true persistent anti-spam and performance journal, use a VPS or add a persistent storage backend.

## 5. 24/7
For truly continuous tick streaming, use `python main.py` on a VPS/PC that stays on. GitHub Actions is a scheduled runner, not a permanent daemon.

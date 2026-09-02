# XAUUSD AI DERIV SIGNAL BOT PRO

Bot signal-only untuk XAUUSD:
- Sumber harga utama: Deriv public market-data WebSocket.
- Timeframe: M15 + M30.
- Eksekusi: MANUAL melalui MT5/terminal trader. Tidak ada fungsi auto-order.
- Telegram: hanya VALID SIGNAL dan ERROR.
- Dynamic SL/TP.
- Anti-spam + duplicate fingerprint.
- Weekend OFF, Monday-Friday ON.
- Performance gate untuk menjaga kualitas sinyal.
- AI optional validator: AI tidak membuat harga; AI hanya memvalidasi data numerik yang sudah dihitung engine.
- Backtest dan journal tersedia.

## PENTING
Target akurasi 95% diperlakukan sebagai TARGET VALIDASI, bukan angka yang dipalsukan. Bot tidak akan mengklaim 95% sebelum jurnal forward/backtest membuktikannya. Performance gate dapat menghentikan signal jika hasil rolling turun di bawah threshold.

## Data real
Deriv API saat ini menyediakan active_symbols, ticks dan ticks_history melalui public WebSocket market-data. Bot memakai endpoint tersebut dan menolak data stale/invalid.

## GitHub Actions
GitHub Actions scheduled workflow memiliki interval minimum 5 menit dan schedule dapat mengalami delay ketika beban GitHub tinggi. Karena itu workflow ini memindai pada interval 5 menit dan mengambil CLOSED M15/M30 candles; jangan menganggap scheduled Actions sebagai tick-by-tick server 24/7.

Untuk kebutuhan tick-by-tick 24/7, jalankan `python main.py` pada VPS/PC yang selalu hidup. Repository tetap menjadi source of truth.

## Setup
1. Copy `.env.example` menjadi `.env` untuk local/VPS.
2. Isi Telegram token/chat ID.
3. Isi OPENAI_API_KEY jika ingin AI validator.
4. Install:
   `pip install -r requirements.txt`
5. Test:
   `python -m tests.test_all`
6. Run one scan:
   `python main.py --once`
7. Run continuous:
   `python main.py`

## GitHub Secrets
Untuk Actions, simpan:
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID
- OPENAI_API_KEY (opsional)
- DERIV_APP_ID (opsional; public market data tidak memerlukannya)

## Symbol
Bot mencari exact XAUUSD dari `active_symbols`. Default preference:
`frxXAUUSD`
Jika exact symbol tidak tersedia, bot TIDAK memakai proxy secara diam-diam. Daftar kandidat akan dilaporkan sebagai error.

## MT5 price alignment
GitHub runner tidak mempunyai akses langsung ke MT5 desktop lokal milik trader. Karena itu bot tidak boleh mengarang bahwa harga Deriv identik dengan broker MT5. Signal berisi:
- Deriv symbol
- Deriv price
- pip_size
- digit-normalized entry/SL/TP
Untuk alignment broker MT5 yang benar-benar sama, jalankan optional MT5 bridge pada mesin Windows/VPS yang memiliki terminal MT5 dan masukkan harga broker ke bridge. Tanpa bridge, gunakan Deriv quote sebagai reference price.

## Signal policy
Bot hanya mengirim signal jika:
- market day
- data fresh
- candle M15/M30 lengkap
- M30 bias valid
- M15 setup valid
- structure valid
- liquidity/momentum/volatility filters lolos
- dynamic target memenuhi minimum distance
- risk/reward lolos
- score engine lolos
- AI validator (jika diaktifkan) lolos
- performance gate tidak sedang pause
- signal fingerprint belum pernah dikirim

Jika salah satu hard gate gagal: NO SIGNAL.

## Accuracy gate
`MIN_TARGET_WIN_RATE=0.95` hanya diterapkan setelah jumlah resolved trades minimum tercapai. Sebelum itu, bot memakai strict confidence/score gates dan mencatat hasil. Jangan mengubah angka gate untuk memaksa signal.

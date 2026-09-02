import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    deriv_app_id: str = os.getenv("DERIV_APP_ID", "")
    deriv_symbol: str = os.getenv("DERIV_SYMBOL", "frxXAUUSD")
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
    min_tp_pips: float = float(os.getenv("MIN_TP_PIPS", "200"))
    min_rr: float = float(os.getenv("MIN_RR", "2.0"))
    strategy_score_threshold: float = float(os.getenv("STRATEGY_SCORE_THRESHOLD", "88"))
    ai_confidence_threshold: float = float(os.getenv("AI_CONFIDENCE_THRESHOLD", "90"))
    min_resolved_for_gate: int = int(os.getenv("MIN_RESOLVED_FOR_PERFORMANCE_GATE", "100"))
    min_target_win_rate: float = float(os.getenv("MIN_TARGET_WIN_RATE", "0.95"))
    max_data_age_seconds: int = int(os.getenv("MAX_DATA_AGE_SECONDS", "90"))
    lookback_m15: int = int(os.getenv("LOOKBACK_M15", "500"))
    lookback_m30: int = int(os.getenv("LOOKBACK_M30", "500"))
    cooldown_minutes: int = int(os.getenv("SIGNAL_COOLDOWN_MINUTES", "30"))

SETTINGS = Settings()

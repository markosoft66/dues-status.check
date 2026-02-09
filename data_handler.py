import pandas as pd
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# --- LOAD ENV ---
env_loaded = load_dotenv()
if not env_loaded:
    print("⚠️ Warning: .env file not loaded")

# --- AUTO-DISCOVER *_URL VARIABLES ---
SHEET_URLS = [
    value
    for key, value in os.environ.items()
    if key.endswith("_URL") and value
]

if not SHEET_URLS:
    raise RuntimeError("❌ No *_URL variables found in environment variables")

print(f"✅ Loaded {len(SHEET_URLS)} sheet URLs")

# --- CACHE ---
_cached_df = None
_last_fetch_time = None
CACHE_DURATION = timedelta(minutes=10)

# --- EXPECTED COLUMNS ---
EXPECTED_COLUMNS = [
    "ID",
    "NAME",
    "PAID DATE",
    "PAID AMOUNT",
    "PAYMENT METHOD",
    "COLLECTOR'S NAME",
]

def get_combined_data(force_refresh: bool = False):
    global _cached_df, _last_fetch_time
    now = datetime.now()

    # --- CACHE HIT ---
    if (
        not force_refresh
        and _cached_df is not None
        and _last_fetch_time is not None
        and now - _last_fetch_time < CACHE_DURATION
    ):
        return _cached_df, _last_fetch_time.strftime("%I:%M %p")

    all_dfs = []

    for url in SHEET_URLS:
        try:
            print(f"📥 Fetching: {url}")
            df = pd.read_csv(url)

            df.columns = (
                df.columns
                .str.strip()
                .str.upper()
                .str.replace("’", "'", regex=False)
            )

            all_dfs.append(df)

        except Exception as e:
            print(f"❌ Failed to fetch {url}")
            print(f"   → {e}")

    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)

        for col in EXPECTED_COLUMNS:
            if col not in combined_df.columns:
                combined_df[col] = pd.NA

        combined_df = combined_df.fillna("")

        _cached_df = combined_df
        _last_fetch_time = now
        return _cached_df, _last_fetch_time.strftime("%I:%M %p")

    print("❌ All sheet fetches failed — returning empty DataFrame")
    return pd.DataFrame(columns=EXPECTED_COLUMNS), now.strftime("%I:%M %p")


def get_cached_data():
    if _cached_df is not None and _last_fetch_time is not None:
        return _cached_df, _last_fetch_time.strftime("%I:%M %p")
    return None, None

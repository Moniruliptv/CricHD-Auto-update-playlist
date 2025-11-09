import requests
from datetime import datetime
import os

# ✅ Source M3U URL (Toffee Auto Update)
SOURCE_M3U = "https://raw.githubusercontent.com/BINOD-XD/Toffee-Auto-Update-Playlist/refs/heads/main/toffee_OTT_Navigator.m3u"

# ✅ Output Files
OUTPUT_FILE = "Toffee.m3u"
LOG_FILE = "update_log.txt"

def log_message(message: str):
    """Append message with timestamp to log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{timestamp}] {message}\n")

def update_playlist():
    print("🚀 Fetching Toffee M3U playlist...")
    try:
        response = requests.get(SOURCE_M3U, timeout=30)
        response.raise_for_status()
        content = response.text.strip()
        print("✅ Successfully fetched playlist!")
    except Exception as e:
        error_msg = f"❌ Error fetching playlist: {e}"
        print(error_msg)
        log_message(error_msg)
        return

    # Validate M3U format
    if not content.startswith("#EXTM3U"):
        msg = "⚠️ Invalid playlist format — missing #EXTM3U header"
        print(msg)
        log_message(msg)
        return

    # Save playlist
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    success_msg = f"✅ Playlist updated successfully → {OUTPUT_FILE}"
    print(success_msg)
    log_message(success_msg)


if __name__ == "__main__":
    update_playlist()

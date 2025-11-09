import requests
from datetime import datetime

# ✅ Source M3U URL
SOURCE_M3U = "https://raw.githubusercontent.com/BINOD-XD/Toffee-Auto-Update-Playlist/refs/heads/main/toffee_OTT_Navigator.m3u"

# ✅ Output files
OUTPUT_FILE = "Toffee.m3u"
LOG_FILE = "update_log.txt"

# ✅ Custom Headers (to bypass CDN/User-Agent block)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

def log_message(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{timestamp}] {msg}\n")

def update_playlist():
    print("🚀 Fetching Toffee M3U playlist...")
    try:
        r = requests.get(SOURCE_M3U, headers=HEADERS, timeout=30)
        r.raise_for_status()
        content = r.text.strip()
        print(f"✅ Fetched content ({len(content)} bytes)")
    except Exception as e:
        error_msg = f"❌ Error fetching playlist: {e}"
        print(error_msg)
        log_message(error_msg)
        content = ""

    # Validate
    if not content.startswith("#EXTM3U"):
        msg = "⚠️ Invalid playlist format — missing #EXTM3U header, adding fallback."
        print(msg)
        log_message(msg)
        content = "#EXTM3U\n# Playlist fetch failed or invalid.\n"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    success = f"✅ Toffee.m3u updated successfully ({len(content)} chars)"
    print(success)
    log_message(success)


if __name__ == "__main__":
    update_playlist()

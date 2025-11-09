import requests
import json
from datetime import datetime

# ✅ CricHD API Source
API_URL = "https://raw.githubusercontent.com/abusaeeidx/CricHd-playlists-Auto-Update-permanent/refs/heads/main/api.json"

# ✅ Output File
OUTPUT_FILE = "CricHD_Playlist.m3u"

# ✅ Default Referrer / Origin
DEFAULT_REFERRER = "https://profamouslife.com/"
DEFAULT_ORIGIN = "https://profamouslife.com"

def generate_playlist():
    print("🚀 Fetching CricHD JSON data...")
    try:
        response = requests.get(API_URL, timeout=20)
        response.raise_for_status()
        data = response.json()
        print("✅ JSON data fetched successfully!")
    except Exception as e:
        print("❌ Error fetching data:", e)
        return

    m3u_lines = ["#EXTM3U"]

    # 🔍 JSON Structure check
    if isinstance(data, list):
        print(f"📘 JSON is a LIST with {len(data)} items")
        items = enumerate(data)  # index, item
    elif isinstance(data, dict):
        print(f"📗 JSON is a DICT with {len(data)} keys")
        items = data.items()
    else:
        print("⚠️ Unsupported JSON format!")
        return

    for name, info in items:
        try:
            # JSON যদি list হয়, তখন name হলো index
            name = info.get("name", str(name))
            tvg_logo = info.get("tvg_logo", "")
            links = info.get("links", [])

            if not links:
                continue

            for link in links:
                if not link.strip():
                    continue

                m3u_lines.append(f'#EXTINF:-1 tvg-logo="{tvg_logo}",{name}')
                m3u_lines.append(f"#EXTVLCOPT:http-referrer={DEFAULT_REFERRER}")
                m3u_lines.append(f"#EXTVLCOPT:http-origin={DEFAULT_ORIGIN}")
                m3u_lines.append(link.strip())

        except Exception as e:
            print(f"⚠️ Error processing {name}: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))

    print(f"✅ Playlist generated successfully: {OUTPUT_FILE}")
    print("🕓 Updated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    generate_playlist()

import requests
import csv
import os
import pytz
from bsedata.bse import BSE
from datetime import datetime

SCRIP_CODE       = "544285"
TELEGRAM_TOKEN   = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
IST              = pytz.timezone("Asia/Kolkata")
CSV_FILE         = "swiggy_prices.csv"

def send_telegram(message):
    url  = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    resp = requests.post(url, data={
        "chat_id":    TELEGRAM_CHAT_ID,
        "text":       message,
        "parse_mode": "Markdown"
    })
    return resp.ok

def fetch_and_notify():
    now_ist = datetime.now(IST)
    now_str = now_ist.strftime("%d %b %Y  %H:%M IST")
    slot    = now_ist.strftime("%H:%M")

    try:
        bse   = BSE(update_codes=True)
        q     = bse.getQuote(SCRIP_CODE)

        price      = q.get("currentValue", "N/A")
        day_open   = q.get("open", q.get("dayOpen", "N/A"))
        day_high   = q.get("dayHigh", "N/A")
        day_low    = q.get("dayLow", "N/A")
        change     = q.get("change", "N/A")
        pct_change = q.get("pChange", "N/A")
        prev_close = q.get("previousClose", q.get("pPriceBand", "N/A"))
        volume     = q.get("totalTradedVolume", "N/A")

        try:
            chg_float = float(str(change).replace(",", ""))
            arrow = "🟢" if chg_float >= 0 else "🔴"
        except:
            arrow = "📊"

        msg = (
            f"{arrow} *SWIGGY  |  BSE: 544285*\n"
            f"🕐 Scheduled slot: `{slot} IST`\n"
            f"📅 {now_str}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"💰 *LTP:*        ₹{price}\n"
            f"📂 *Day Open:*   ₹{day_open}\n"
            f"🔼 *Day High:*   ₹{day_high}\n"
            f"🔽 *Day Low:*    ₹{day_low}\n"
            f"⏮ *Prev Close:* ₹{prev_close}\n"
            f"📈 *Change:*     {change} ({pct_change}%)\n"
            f"📦 *Volume:*     {volume}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"_Source: BSE India (live)_"
        )

        ok = send_telegram(msg)
        print(f"[{now_str}] ✅ Telegram sent: {ok} | LTP ₹{price} | {pct_change}%")

        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Slot", "LTP", "Open", "High", "Low",
                                 "Prev Close", "Change", "Change%", "Volume"])
            writer.writerow([now_str, slot, price, day_open, day_high, day_low,
                             prev_close, change, pct_change, volume])

    except Exception as e:
        err_msg = (
            f"⚠️ *SWIGGY fetch failed*\n"
            f"Slot: `{slot} IST` | {now_str}\n"
            f"Error: `{str(e)}`"
        )
        send_telegram(err_msg)
        print(f"ERROR: {e}")

if __name__ == "__main__":
    fetch_and_notify()

# Swiggy Stock Tracker — GitHub Actions + Telegram

Runs automatically on GitHub's cloud at all 8 IST market times.
Your Mac does NOT need to be on.

## Setup (one-time, ~10 minutes)

### Step 1 — Get Telegram bot credentials
1. Open Telegram → search `@BotFather` → send `/newbot`
2. Follow prompts → copy your **Bot Token**
3. Search `@userinfobot` → copy your **Chat ID**

### Step 2 — Create GitHub repository
1. Go to github.com → New repository → name it `swiggy-tracker`
2. Upload both files: `swiggy_alert.py` and `.github/workflows/swiggy_tracker.yml`

### Step 3 — Add secrets
1. GitHub repo → Settings → Secrets and variables → Actions
2. Add secret: `TELEGRAM_TOKEN` = your bot token
3. Add secret: `TELEGRAM_CHAT_ID` = your chat ID

### Step 4 — Enable Actions
1. GitHub repo → Actions tab → enable workflows

Done! You'll get Telegram alerts at all 8 IST slots every weekday.
Mac can be off, closed, or in sleep mode — doesn't matter.

## Scheduled slots (IST)
| IST   | UTC   | Label           |
|-------|-------|-----------------|
| 09:07 | 03:37 | Pre-open        |
| 09:15 | 03:45 | Market open     |
| 10:15 | 04:45 | Mid-morning     |
| 12:00 | 06:30 | Midday          |
| 15:00 | 09:30 | Pre-close       |
| 15:15 | 09:45 | Closing session |
| 15:30 | 10:00 | Post-close 1    |
| 15:50 | 10:20 | Post-close 2    |

## Manual trigger
GitHub repo → Actions → "Swiggy Stock Tracker" → Run workflow

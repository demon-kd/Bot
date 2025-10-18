
# Create requirements.txt, .env template, and setup instructions

requirements_txt = """discord.py>=2.3.0
yt-dlp>=2024.0.0
python-dotenv>=1.0.0
better-profanity>=0.7.0
PyNaCl>=1.5.0
"""

env_template = """# Discord Bot Configuration
BOT_TOKEN=your_bot_token_here
GUILD_ID=your_server_id_here
"""

setup_instructions = """# Discord Bot Setup Instructions

## Prerequisites
1. Python 3.8 or higher
2. FFmpeg installed on your system

## Installation Steps

### 1. Install FFmpeg

**Windows:**
- Download from https://ffmpeg.org/download.html
- Add to system PATH

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Discord Bot

1. Go to Discord Developer Portal: https://discord.com/developers/applications
2. Click "New Application" and give it a name
3. Go to "Bot" tab and click "Add Bot"
4. Enable these Privileged Gateway Intents:
   - SERVER MEMBERS INTENT
   - MESSAGE CONTENT INTENT
5. Copy the bot token

### 4. Invite Bot to Server

1. Go to OAuth2 > URL Generator
2. Select scopes:
   - `bot`
   - `applications.commands`
3. Select bot permissions:
   - Send Messages
   - Manage Messages
   - Connect
   - Speak
   - Use Slash Commands
   - Kick Members
   - Ban Members
   - Moderate Members
4. Copy the generated URL and open in browser
5. Select your server and authorize

### 5. Configure Environment Variables

1. Copy `.env.example` to `.env`
2. Add your bot token
3. Add your server (guild) ID

To get Guild ID:
- Enable Developer Mode in Discord (Settings > Advanced > Developer Mode)
- Right-click your server icon > Copy ID

### 6. Run the Bot
```bash
python discord_bot_complete.py
```

## Features

### Music Commands
- `/play <query>` - Play a song from YouTube
- `/queue` - Show current music queue
- Interactive buttons: Pause, Resume, Skip, Stop

### Moderation Commands
- `/ban <member> [reason]` - Ban a member
- `/kick <member> [reason]` - Kick a member
- `/timeout <member> <duration> [reason]` - Timeout a member
- `/purge <amount>` - Delete multiple messages
- `/warnings <member>` - Check warnings for a user
- Auto-moderation: Profanity filter with automatic timeouts

## Architecture

### Multi-Server Support
- The bot uses dictionaries to track queues per server (guild)
- Each server has its own independent music queue
- Infractions are tracked globally per user

### Interactive Interface
- Uses Discord UI Buttons for music controls
- Persistent buttons that work across sessions
- Embedded messages with rich formatting

### Moderation System
- Automatic profanity detection and deletion
- Warning system with escalating punishments
- 3 strikes = 10-minute timeout
- Slash commands for manual moderation

## Customization

### Add Custom Profanity Words
```python
from better_profanity import profanity
profanity.add_censor_words(['word1', 'word2'])
```

### Change Timeout Duration
Edit the timeout duration in the auto-moderation section:
```python
await message.author.timeout(timedelta(minutes=10), reason="...")
```

### Modify Button Colors
Change button styles in MusicControlView:
- `discord.ButtonStyle.primary` (Blue)
- `discord.ButtonStyle.success` (Green)
- `discord.ButtonStyle.secondary` (Gray)
- `discord.ButtonStyle.danger` (Red)

## Troubleshooting

### Bot doesn't respond to slash commands
- Wait a few minutes for commands to sync
- Ensure bot has `applications.commands` scope
- Check bot permissions in server settings

### Music not playing
- Verify FFmpeg is installed and in PATH
- Check bot has "Connect" and "Speak" permissions
- Ensure you're in a voice channel

### Moderation commands not working
- Check role hierarchy (bot role must be higher than target)
- Verify bot has required permissions
- Enable 2FA if required by server settings

## Security Notes

- Never share your bot token
- Keep `.env` file in `.gitignore`
- Regularly rotate your bot token
- Use role hierarchy to limit bot power
"""

# Save files
with open('/tmp/requirements.txt', 'w') as f:
    f.write(requirements_txt)

with open('/tmp/.env.example', 'w') as f:
    f.write(env_template)
    
with open('/tmp/SETUP_INSTRUCTIONS.md', 'w') as f:
    f.write(setup_instructions)

print("✅ Created setup files:")
print("   - requirements.txt")
print("   - .env.example")
print("   - SETUP_INSTRUCTIONS.md")

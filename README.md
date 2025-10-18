# Discord Bot Quick Start Guide
### Music Playback + Moderation + Interactive UI

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Prerequisites
```bash
# Install FFmpeg first (system-specific)
# Windows: Download from ffmpeg.org
# Linux: sudo apt install ffmpeg
# macOS: brew install ffmpeg

# Install Python packages
pip install discord.py yt-dlp python-dotenv better-profanity PyNaCl
```

### Step 2: Create Discord Bot
1. Go to https://discord.com/developers/applications
2. Create New Application
3. Add Bot User (Bot tab)
4. Enable: SERVER MEMBERS INTENT, MESSAGE CONTENT INTENT
5. Copy Bot Token
6. OAuth2 → URL Generator: Select `bot` + `applications.commands`
7. Bot Permissions: Send Messages, Manage Messages, Connect, Speak, Kick Members, Ban Members, Moderate Members
8. Use generated URL to invite bot to your server

### Step 3: Configure Environment
Create `.env` file:
```
BOT_TOKEN=your_bot_token_here
GUILD_ID=your_server_id_here
```

### Step 4: Run the Bot
```bash
python discord_bot_complete.py
```

---

## 📋 Command List

### Music Commands
- `/play <song name or URL>` - Play music from YouTube
- `/queue` - Show current music queue

### Interactive Buttons
- ⏸️ Pause - Pause current song
- ▶️ Resume - Resume playback
- ⏭️ Skip - Skip to next song
- ⏹️ Stop - Stop music and disconnect

### Moderation Commands
- `/ban <member> [reason]` - Ban a member (Requires: Ban Members permission)
- `/kick <member> [reason]` - Kick a member (Requires: Kick Members permission)
- `/timeout <member> <minutes> [reason]` - Timeout a member (Requires: Moderate Members permission)
- `/purge <amount>` - Delete 1-100 messages (Requires: Manage Messages permission)
- `/warnings <member>` - Check user warnings

### Auto-Moderation
- Automatic profanity detection and deletion
- 3-strike warning system
- Automatic 10-minute timeout after 3 warnings

---

## 🎯 Key Features

### ✅ Music System
- Stream audio from YouTube (URLs or search)
- Per-server music queues (no interference between servers)
- Interactive button controls
- Rich embed displays

### ✅ Moderation System
- Complete command suite (ban, kick, timeout, purge)
- Real-time profanity filtering
- Warning tracking and auto-punishment
- Slash command interface

### ✅ Multi-Server Support
- Works on unlimited Discord servers simultaneously
- Independent queues and state per server
- No cross-contamination

### ✅ Interactive UI
- Persistent buttons for music control
- Rich embedded messages
- Visual feedback and status updates

---

## 🔧 Customization Options

### Change Timeout Duration
In `discord_bot_complete.py`, line ~220:
```python
await message.author.timeout(timedelta(minutes=10), ...)  # Change 10 to desired minutes
```

### Add Custom Profanity Words
```python
from better_profanity import profanity
profanity.add_censor_words(['word1', 'word2', 'word3'])
```

### Modify Warning Threshold
Line ~215:
```python
if infractions[user_id] >= 3:  # Change 3 to desired threshold
```

### Change Button Colors
In `MusicControlView` class:
- `discord.ButtonStyle.primary` - Blue
- `discord.ButtonStyle.success` - Green
- `discord.ButtonStyle.secondary` - Gray
- `discord.ButtonStyle.danger` - Red

---

## 🐛 Troubleshooting

### Commands Not Showing Up
- Wait 1-2 hours for Discord to sync commands globally
- Ensure bot has `applications.commands` scope
- Try kicking and re-inviting bot with correct permissions

### Music Not Playing
- Verify FFmpeg is installed: `ffmpeg -version`
- Check bot has "Connect" and "Speak" permissions
- Ensure you're in a voice channel when using `/play`

### Moderation Commands Failing
- Bot role must be **higher** than target role in server settings
- Verify bot has required permissions
- Check if 2FA is required for your server

### Bot Goes Offline
- Free hosting has limitations - use UptimeRobot to keep alive
- Check console for errors
- Ensure token is correct in `.env` file

---

## 📊 Feature Comparison

| Feature | Your Bot | LunaBot | Wick Bot |
|---------|----------|---------|----------|
| Music Playback | ✅ | ✅ | ❌ |
| YouTube Support | ✅ | ✅ | ❌ |
| Interactive Buttons | ✅ | ✅ | ❌ |
| Queue System | ✅ | ✅ | ❌ |
| Multi-Server | ✅ | ✅ | ✅ |
| Ban/Kick | ✅ | ❌ | ✅ |
| Timeout/Mute | ✅ | ❌ | ✅ |
| Profanity Filter | ✅ | ❌ | ✅ |
| Auto-Moderation | ✅ | ❌ | ✅ |
| Slash Commands | ✅ | ✅ | ✅ |

---

## 🚀 Deployment Options

### Local Testing
Just run: `python discord_bot_complete.py`
(Keep terminal open)

### Free Cloud Hosting
**Render.com** (Recommended):
1. Create account at render.com
2. New → Web Service → Connect GitHub repo
3. Add environment variables (BOT_TOKEN)
4. Deploy
5. Use UptimeRobot to ping every 5 minutes

**Oracle Cloud** (True 24/7):
- Free VM instances
- More complex setup
- Best for serious projects

---

## 📚 File Structure

```
discord-bot/
├── discord_bot_complete.py    # Main bot code
├── requirements.txt            # Python dependencies
├── .env                        # Bot token (DO NOT COMMIT)
├── .gitignore                 # Exclude .env from git
└── README.md                  # This file
```

---

## 🔒 Security Reminders

1. **Never share your bot token** - Treat it like a password
2. **Keep `.env` out of git** - Add to `.gitignore`
3. **Update dependencies regularly** - Security patches
4. **Monitor bot activity** - Check logs for suspicious behavior
5. **Use role hierarchy** - Bot role below admin roles

---

## 📞 Support & Resources

- **Discord.py Docs**: https://discordpy.readthedocs.io/
- **yt-dlp GitHub**: https://github.com/yt-dlp/yt-dlp
- **Discord Developer Portal**: https://discord.com/developers
- **Community Help**: Discord.py Discord server

---

## 📝 License & Credits

This bot template combines:
- Music system inspired by LunaBot
- Moderation features inspired by Wick Bot
- Built with discord.py, yt-dlp, and FFmpeg

Feel free to modify and extend for your community's needs!

---

## 🎓 Next Steps

### Beginner
1. Get bot running locally
2. Test music playback with `/play`
3. Try moderation commands
4. Customize button colors

### Intermediate
1. Deploy to cloud hosting (Render)
2. Add logging system
3. Implement database for infractions
4. Add more music commands (volume, loop)

### Advanced
1. Implement anti-spam protection
2. Add role management commands
3. Create custom embeds per server
4. Build web dashboard for configuration

---

**Ready to start? Run the setup commands and invite your bot!**

For the complete 16-page technical guide with code explanations, architecture diagrams, and advanced topics, see `Discord-Bot-Complete-Guide.pdf`.

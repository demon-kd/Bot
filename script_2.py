
# Create a comparison table of key features

import pandas as pd

# Feature comparison
features_data = {
    'Feature': [
        'Music Playback',
        'YouTube Support',
        'Interactive Buttons',
        'Queue System',
        'Multi-Server Support',
        'Ban/Kick Commands',
        'Timeout/Mute',
        'Message Purge',
        'Profanity Filter',
        'Auto-Moderation',
        'Warning System',
        'Slash Commands',
        'Embeds/Rich UI',
        'Role Management'
    ],
    'Your Bot': ['✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '⚠️ Basic'],
    'LunaBot': ['✅', '✅', '✅', '✅', '✅', '❌', '❌', '❌', '❌', '❌', '❌', '✅', '✅', '❌'],
    'Wick Bot': ['❌', '❌', '❌', '❌', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅']
}

df = pd.DataFrame(features_data)
print("\n🔍 FEATURE COMPARISON\n")
print(df.to_string(index=False))

# Key libraries comparison
libraries_data = {
    'Library': ['discord.py', 'yt-dlp', 'FFmpeg', 'better-profanity', 'python-dotenv'],
    'Purpose': [
        'Discord API wrapper',
        'YouTube audio extraction',
        'Audio encoding/decoding',
        'Profanity detection',
        'Environment variables'
    ],
    'Installation': [
        'pip install discord.py',
        'pip install yt-dlp',
        'System package manager',
        'pip install better-profanity',
        'pip install python-dotenv'
    ]
}

df_libs = pd.DataFrame(libraries_data)
print("\n\n📚 REQUIRED LIBRARIES\n")
print(df_libs.to_string(index=False))

# Commands overview
commands_data = {
    'Command': [
        '/play <query>',
        '/queue',
        '/ban <member>',
        '/kick <member>',
        '/timeout <member> <duration>',
        '/purge <amount>',
        '/warnings <member>'
    ],
    'Category': ['Music', 'Music', 'Moderation', 'Moderation', 'Moderation', 'Moderation', 'Moderation'],
    'Permission Required': ['None', 'None', 'Ban Members', 'Kick Members', 'Moderate Members', 'Manage Messages', 'None'],
    'Description': [
        'Play song from YouTube',
        'Show music queue',
        'Ban a member permanently',
        'Kick a member from server',
        'Timeout member for X minutes',
        'Delete multiple messages',
        'Check user warnings'
    ]
}

df_cmds = pd.DataFrame(commands_data)
print("\n\n⚡ COMMANDS OVERVIEW\n")
print(df_cmds.to_string(index=False))

# Save to CSV
df.to_csv('/tmp/feature_comparison.csv', index=False)
df_libs.to_csv('/tmp/libraries.csv', index=False)
df_cmds.to_csv('/tmp/commands.csv', index=False)

print("\n\n✅ CSV files created for reference")

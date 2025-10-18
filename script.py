
# Create a comprehensive Discord bot code structure with music, moderation, and interactive UI

discord_bot_code = """
# Discord Bot with Music, Moderation, and Interactive Interface
# Requirements: discord.py, yt-dlp, ffmpeg, python-dotenv, better-profanity

import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
from typing import Optional
from datetime import timedelta
import os
from dotenv import load_dotenv
from better_profanity import profanity

# Load environment variables
load_dotenv()

# Bot Configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MusicBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.music_queues = {}  # Dictionary to store queues per server
        
    async def setup_hook(self):
        # Sync commands to Discord
        await self.tree.sync()
        print("Commands synced!")

bot = MusicBot()

# YouTube DL Configuration
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            data = data['entries'][0]
            
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# Queue Management Class
class MusicQueue:
    def __init__(self):
        self.queue = []
        self.current = None
        self.loop = False
        
    def add(self, song):
        self.queue.append(song)
        
    def next(self):
        if self.loop and self.current:
            return self.current
        if self.queue:
            self.current = self.queue.pop(0)
            return self.current
        return None
        
    def clear(self):
        self.queue.clear()
        self.current = None

# Music Control Buttons View
class MusicControlView(discord.ui.View):
    def __init__(self, bot, guild_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.guild_id = guild_id
        
    @discord.ui.button(label="⏸️ Pause", style=discord.ButtonStyle.primary, custom_id="pause_button")
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("⏸️ Paused the music!", ephemeral=True)
        else:
            await interaction.response.send_message("Nothing is playing!", ephemeral=True)
            
    @discord.ui.button(label="▶️ Resume", style=discord.ButtonStyle.success, custom_id="resume_button")
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await interaction.response.send_message("▶️ Resumed the music!", ephemeral=True)
        else:
            await interaction.response.send_message("Nothing is paused!", ephemeral=True)
            
    @discord.ui.button(label="⏭️ Skip", style=discord.ButtonStyle.secondary, custom_id="skip_button")
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("⏭️ Skipped!", ephemeral=True)
        else:
            await interaction.response.send_message("Nothing is playing!", ephemeral=True)
            
    @discord.ui.button(label="⏹️ Stop", style=discord.ButtonStyle.danger, custom_id="stop_button")
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_client = interaction.guild.voice_client
        if voice_client:
            if self.guild_id in self.bot.music_queues:
                self.bot.music_queues[self.guild_id].clear()
            voice_client.stop()
            await voice_client.disconnect()
            await interaction.response.send_message("⏹️ Stopped and disconnected!", ephemeral=True)
        else:
            await interaction.response.send_message("Not connected to a voice channel!", ephemeral=True)

# ==================== MUSIC COMMANDS ====================

@bot.tree.command(name="play", description="Play a song from YouTube")
@app_commands.describe(query="The song name or YouTube URL")
async def play(interaction: discord.Interaction, query: str):
    await interaction.response.defer()
    
    # Check if user is in voice channel
    if not interaction.user.voice:
        await interaction.followup.send("You need to be in a voice channel!")
        return
        
    # Get or create music queue for this guild
    guild_id = interaction.guild.id
    if guild_id not in bot.music_queues:
        bot.music_queues[guild_id] = MusicQueue()
        
    # Connect to voice channel
    voice_client = interaction.guild.voice_client
    if not voice_client:
        channel = interaction.user.voice.channel
        voice_client = await channel.connect()
        
    # Search and add to queue
    try:
        if not query.startswith('http'):
            query = f"ytsearch:{query}"
            
        player = await YTDLSource.from_url(query, loop=bot.loop)
        bot.music_queues[guild_id].add(player)
        
        # Create embed with music controls
        embed = discord.Embed(
            title="🎵 Added to Queue",
            description=f"**{player.title}**",
            color=discord.Color.green()
        )
        
        view = MusicControlView(bot, guild_id)
        
        if not voice_client.is_playing():
            await play_next(interaction.guild)
            embed.title = "🎵 Now Playing"
            
        await interaction.followup.send(embed=embed, view=view)
        
    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)}")

async def play_next(guild):
    guild_id = guild.id
    voice_client = guild.voice_client
    
    if guild_id not in bot.music_queues:
        return
        
    queue = bot.music_queues[guild_id]
    song = queue.next()
    
    if song and voice_client:
        voice_client.play(song, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(guild), bot.loop))

@bot.tree.command(name="queue", description="Show the music queue")
async def show_queue(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    
    if guild_id not in bot.music_queues or not bot.music_queues[guild_id].queue:
        await interaction.response.send_message("The queue is empty!")
        return
        
    queue = bot.music_queues[guild_id]
    embed = discord.Embed(title="🎵 Music Queue", color=discord.Color.blue())
    
    queue_text = ""
    for i, song in enumerate(queue.queue[:10], 1):
        queue_text += f"{i}. {song.title}\\n"
        
    embed.description = queue_text or "Queue is empty"
    await interaction.response.send_message(embed=embed)

# ==================== MODERATION COMMANDS ====================

# Profanity filter setup
profanity.load_censor_words()

# Infractions tracking
infractions = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return
        
    # Check for profanity
    if profanity.contains_profanity(message.content):
        await message.delete()
        
        user_id = message.author.id
        infractions[user_id] = infractions.get(user_id, 0) + 1
        
        warning_msg = await message.channel.send(
            f"⚠️ {message.author.mention} Warning {infractions[user_id]}/3 for inappropriate language!"
        )
        await asyncio.sleep(5)
        await warning_msg.delete()
        
        # Auto-punish after 3 warnings
        if infractions[user_id] >= 3:
            try:
                await message.author.timeout(timedelta(minutes=10), reason="Multiple profanity violations")
                await message.channel.send(f"{message.author.mention} has been timed out for 10 minutes.")
                infractions[user_id] = 0
            except:
                pass
                
    await bot.process_commands(message)

@bot.tree.command(name="ban", description="Ban a member from the server")
@app_commands.describe(member="The member to ban", reason="Reason for the ban")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = "No reason provided"):
    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="🔨 Member Banned",
            description=f"**{member}** has been banned.\\n**Reason:** {reason}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"Failed to ban: {str(e)}", ephemeral=True)

@bot.tree.command(name="kick", description="Kick a member from the server")
@app_commands.describe(member="The member to kick", reason="Reason for the kick")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = "No reason provided"):
    try:
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="👢 Member Kicked",
            description=f"**{member}** has been kicked.\\n**Reason:** {reason}",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"Failed to kick: {str(e)}", ephemeral=True)

@bot.tree.command(name="timeout", description="Timeout a member")
@app_commands.describe(member="The member to timeout", duration="Duration in minutes", reason="Reason for timeout")
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int, reason: Optional[str] = "No reason provided"):
    try:
        await member.timeout(timedelta(minutes=duration), reason=reason)
        embed = discord.Embed(
            title="⏱️ Member Timed Out",
            description=f"**{member}** has been timed out for {duration} minutes.\\n**Reason:** {reason}",
            color=discord.Color.yellow()
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"Failed to timeout: {str(e)}", ephemeral=True)

@bot.tree.command(name="purge", description="Delete multiple messages")
@app_commands.describe(amount="Number of messages to delete")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, amount: int):
    if amount < 1 or amount > 100:
        await interaction.response.send_message("Please specify a number between 1 and 100!", ephemeral=True)
        return
        
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"Deleted {len(deleted)} messages!", ephemeral=True)

@bot.tree.command(name="warnings", description="Check warnings for a user")
@app_commands.describe(member="The member to check")
async def check_warnings(interaction: discord.Interaction, member: discord.Member):
    user_id = member.id
    warning_count = infractions.get(user_id, 0)
    
    embed = discord.Embed(
        title=f"⚠️ Warnings for {member}",
        description=f"Total warnings: **{warning_count}**",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

# ==================== BOT EVENTS ====================

@bot.event
async def on_ready():
    print(f'{bot.user} is now online!')
    print(f'Connected to {len(bot.guilds)} servers')
    await bot.change_presence(activity=discord.Game(name="/play | /help"))

# Run the bot
if __name__ == "__main__":
    bot.run(os.getenv('BOT_TOKEN'))
"""

# Save to file
with open('/tmp/discord_bot_complete.py', 'w') as f:
    f.write(discord_bot_code)

print("✅ Complete Discord bot code structure created")
print(f"📄 Code length: {len(discord_bot_code)} characters")
print(f"📦 Lines of code: {len(discord_bot_code.split(chr(10)))} lines")

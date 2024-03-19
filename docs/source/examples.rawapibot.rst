import discord
from discord.ext import commands

# Create a bot instance
bot = commands.Bot(command_prefix='!')

# Event that is triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Command that sends a message to a specific channel
@bot.command()
async def send\_message(ctx, channel: discord.TextChannel, *, message):
    await channel.send(message)
    await ctx.message.delete()

# Command that sends an embed message to a specific channel
@bot.command()
async def send\_embed(ctx, channel: discord.TextChannel, title, description, color=0x00ff00):
    embed = discord.Embed(title=title, description=description, color=color)
    await channel.send(embed=embed)
    await ctx.message.delete()

# Run the bot
bot.run('your-token-here')

# remove_slash_commands.py

import discord
from core.config import ConfigManager  # Adjust based on your project structure

async def remove_slash_commands(bot: discord.Client):
    """Remove all slash commands from all guilds the bot is in."""
    # Initialize the config manager
    config = ConfigManager(None)  # Adjust this line if needed
    config.populate_cache()

    # Get the token from the config (if needed)
    # TOKEN = config["token"]  # Not needed here, we will pass the bot directly

    app = await bot.application_info()

    # Get all guilds the bot is in
    for guild in bot.guilds:
        commands = await bot.http.get_guild_application_commands(app.id, guild.id)
        for command in commands:
            await bot.http.delete_guild_application_command(app.id, command['id'], guild.id)
            print(f'Deleted command: {command["name"]} from guild: {guild.name}')

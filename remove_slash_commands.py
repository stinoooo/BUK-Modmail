import discord
from core.config import ConfigManager  # Adjust based on your project structure

async def remove_slash_commands(bot: discord.Client):
    """Remove all slash commands from all guilds the bot is in."""
    # Initialize the config manager
    config = ConfigManager(None)  # Adjust this line if needed
    config.populate_cache()

    app = await bot.application_info()

    # Get all guilds the bot is in
    for guild in bot.guilds:
        # Fetch all guild slash commands using the correct method
        commands = await bot.fetch_guild_application_commands(guild.id)
        for command in commands:
            await bot.delete_guild_application_command(command.id, guild.id)
            print(f'Deleted command: {command.name} from guild: {guild.name}')

import discord
from core.config import ConfigManager  # Adjust based on your project structure

async def remove_slash_commands(bot: discord.Client):
    """Remove specified slash commands from all guilds the bot is in."""
    # Initialize the config manager
    config = ConfigManager(None)  # Adjust this line if needed
    config.populate_cache()

    app = await bot.application_info()

    # List of command IDs to remove
    command_ids_to_remove = [
        1258612044580524073,
        1258612044580524074,
        1258612044580524075,
        1258634060025167872,
        1258634060025167873,
        1258612044580524077,
        1258639973381574667,
        1258634060025167874,
        1258612044580524076,
    ]

    # Get all guilds the bot is in
    for guild in bot.guilds:
        for command_id in command_ids_to_remove:
            try:
                await bot.http.delete_guild_application_command(app.id, command_id, guild.id)
                print(f'Deleted command ID: {command_id} from guild: {guild.name}')
            except Exception as e:
                print(f'Failed to delete command ID: {command_id} from guild: {guild.name}, Error: {e}')

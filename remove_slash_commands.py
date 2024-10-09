import discord
import requests
import asyncio
from core.config import ConfigManager  # Adjust based on your project structure

async def remove_slash_commands(bot: discord.Client):
    """Remove specified slash commands from all guilds the bot is in."""
    # Initialize the config manager
    config = ConfigManager(None)  # Adjust this line if needed
    config.populate_cache()

    token = config["token"]
    app_id = bot.user.id

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
        guild_id = guild.id
        for command_id in command_ids_to_remove:
            url = f'https://discord.com/api/v10/applications/{app_id}/guilds/{guild_id}/commands/{command_id}'
            headers = {
                'Authorization': f'Bot {token}',
                'Content-Type': 'application/json'
            }
            
            # Attempt to delete the command
            response = requests.delete(url, headers=headers)

            if response.status_code == 204:
                print(f'Successfully deleted command ID: {command_id} from guild: {guild.name}')
            elif response.status_code == 404:
                print(f'Command ID: {command_id} not found in guild: {guild.name}.')
            elif response.status_code == 429:
                retry_after = response.json().get('retry_after', 1)
                print(f'Rate limited. Retrying after {retry_after} seconds...')
                await asyncio.sleep(retry_after)
                # Retry deleting the command after waiting
                response = requests.delete(url, headers=headers)
                if response.status_code == 204:
                    print(f'Successfully deleted command ID: {command_id} from guild: {guild.name} after retrying.')
            else:
                print(f'Failed to delete command ID: {command_id} from guild: {guild.name}, Error: {response.text}')

            # Optional: Wait a bit between requests to avoid hitting the rate limit too fast
            await asyncio.sleep(1)  # Adjust sleep duration as needed

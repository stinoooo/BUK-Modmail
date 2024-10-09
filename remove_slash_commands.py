import discord
import requests
import asyncio
from core.config import ConfigManager  # Adjust based on your project structure

async def remove_slash_commands(bot: discord.Client):
    """Remove all application commands from all guilds the bot is in."""
    # Initialize the config manager
    config = ConfigManager(None)  # Adjust this line if needed
    config.populate_cache()

    token = config["token"]
    app_id = bot.user.id

    # Get all guilds the bot is in
    for guild in bot.guilds:
        guild_id = guild.id
        url = f'https://discord.com/api/v10/applications/{app_id}/guilds/{guild_id}/commands'
        headers = {
            'Authorization': f'Bot {token}',
            'Content-Type': 'application/json'
        }

        # Fetch all application commands
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            commands = response.json()
            if commands:
                for command in commands:
                    command_id = command['id']
                    delete_url = f'https://discord.com/api/v10/applications/{app_id}/guilds/{guild_id}/commands/{command_id}'

                    # Attempt to delete the command
                    delete_response = requests.delete(delete_url, headers=headers)
                    
                    if delete_response.status_code == 204:
                        print(f'Successfully deleted command ID: {command_id} from guild: {guild.name}')
                    elif delete_response.status_code == 404:
                        print(f'Command ID: {command_id} not found in guild: {guild.name}.')
                    elif delete_response.status_code == 429:
                        retry_after = delete_response.json().get('retry_after', 1)
                        print(f'Rate limited. Retrying after {retry_after} seconds...')
                        await asyncio.sleep(retry_after)
                        # Retry deleting the command after waiting
                        delete_response = requests.delete(delete_url, headers=headers)
                        if delete_response.status_code == 204:
                            print(f'Successfully deleted command ID: {command_id} from guild: {guild.name} after retrying.')
                    else:
                        print(f'Failed to delete command ID: {command_id} from guild: {guild.name}, Error: {delete_response.text}')
            else:
                print(f'No application commands found in guild: {guild.name}.')
        else:
            print(f'Failed to fetch commands from guild: {guild.name}, Error: {response.text}')
        
        # Optional: Wait a bit between requests to avoid hitting the rate limit too fast
        await asyncio.sleep(1)  # Adjust sleep duration as needed

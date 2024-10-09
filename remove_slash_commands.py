import discord
import asyncio

TOKEN = 'MTI0NzQ4ODM1Nzc2NDgyOTI5Ng.Gle6tS.CmIFSJ9fihf7hjMeS7EEJjEnWjb2L9FT29seMw'

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    app = await bot.application_info()

    # Get all guilds the bot is in
    for guild in bot.guilds:
        commands = await bot.http.get_guild_application_commands(app.id, guild.id)
        for command in commands:
            await bot.http.delete_guild_application_command(app.id, command['id'], guild.id)
            print(f'Deleted command: {command["name"]} from guild: {guild.name}')

    await bot.close()

bot.run(TOKEN)

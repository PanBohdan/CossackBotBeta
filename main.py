import discord
from discord.ext.commands import Bot, Command
import os
from pymongo import MongoClient
from cogs.photo import Photo
from cogs.games import Games
from json import loads
try:
    from secrets import *
except ImportError:
    pass

# Main settings
TOKEN = os.environ.get('TOKEN')
prefix = '.'

# Cogs setup
cogs_dir = 'cogs'
dict_of_cog_names_and_classes = {'photo': Photo, 'games': Games, }
list_of_full_cog_path = [f"{cogs_dir}.{cog}" for cog in dict_of_cog_names_and_classes.keys()]

# DB
m_client = MongoClient(os.environ.get('DB'))
db = m_client['my_db']

# Localization
list_of_available_languages = ['en', 'ua']
server_languages_collection = db['server_languages']

# Bot setup
client = Bot(prefix)
client.remove_command('help')


@client.event
async def on_ready():
    for cog in list_of_full_cog_path:
        client.load_extension(cog)
    print(f'Logged in as: {client.user.name}')
    print(f'With ID: {client.user.id}')
    print(f'Loaded cogs: {list(dict_of_cog_names_and_classes.keys())}')


@client.command(aliases=['мова'])
async def language(ctx, new_language):
    if new_language in list_of_available_languages:
        server_languages_collection.replace_one({'id': ctx.guild.id}, {'id': ctx.guild.id, 'language': new_language})
        await ctx.send('Done')


@client.command(aliases=['поможіть', 'help'])
async def _help(ctx, module=None):
    no_module = False
    # Check for module
    try:
        put_class = dict_of_cog_names_and_classes[module]
    except KeyError:
        no_module = True
    #  Check for localization
    try:
        localization = server_languages_collection.find_one({'id': ctx.guild.id})['language']
    except TypeError:
        server_languages_collection.insert_one({'id': ctx.guild.id, 'language': 'en'})
        localization = 'en'

    if no_module:
        dict_of_answers = {
            'en': f'No such module. Check module list by typing {prefix}modules', 
            'ua': f"Такого модуля не існує. Перевірте наявні модулі прописавши {prefix}модулі"
            }
        await ctx.send(dict_of_answers[localization])
        return

    help_string = ""
    try:
        for name, func in put_class.__dict__.items():
            if type(func) == Command:
                if not name == '__init__':
                    f_dict = loads(func.__doc__)[localization]
                    help_string += f"{f_dict['name']}:\n	{f_dict['description']}\n"
    except KeyError:
        localization = "en"
        for _, func in put_class.__dict__.items():
            if type(func) == Command:
                f_dict = loads(func.__doc__)[localization]
                help_string += f"{f_dict['name']}:\n	{f_dict['description']}\n"
    await ctx.send(help_string)


@client.command(aliases=['модулі'])
async def modules(ctx):
    await ctx.send(dict_of_cog_names_and_classes.keys())
client.run(TOKEN)

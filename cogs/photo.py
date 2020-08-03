import discord
from discord.ext import commands
import random
import os
from pymongo import MongoClient
try:
    from secrets import *
except ImportError:
    pass
m_client = MongoClient(os.environ.get('DB'))
db = m_client['my_db']
images_collection = db['images']
b_images_collection = db['b_images']
server_languages_collection = db['server_languages']


class Photo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, aliases=['фото', 'стікер'])
    async def photo(self, ctx, photo_name):
        await ctx.channel.purge(limit=1)
        tmp = images_collection.find_one({'name': photo_name})
        output = str(tmp['url'])
        if not output == 'None':
            await ctx.send(output)
    photo.__doc__ = """*
        {
            "en":
            {
                "name": "photo (name)",
                "description": "Sends photo with that name"
            },
            "ua":
            {
                "name": "фото (назва)",
                "description": "Надсилає фото з вказаною назвою"
            }
        }
        """

    @commands.has_role('адмін фоток')
    @commands.command(pass_context=True, aliases=['додати_фото', 'додати_стікер'])
    async def add_photo(self, ctx, *, photo_name_and_url):
        new_arg = photo_name_and_url.split('|')
        print(new_arg)
        arg1 = new_arg[0]
        arg2 = new_arg[1]
        images_collection.insert_one({'name': arg1, 'url': arg2})
        try:
            localization = server_languages_collection.find_one({'id': ctx.guild.id})['language']
        except TypeError:
            server_languages_collection.insert_one({'id': ctx.guild.id, 'language': 'en'})
            localization = 'en'
        localized_answers = {'en': 'Added', 'ua': 'Додано'}
        await ctx.send(localized_answers[localization])
    add_photo.__doc__ = """
        {
            "en":
            {
                "name": "add_photo (name)|(url)",
                "description": "Adds photo with given name and url to a database"
            },
            "ua":
            {
                "name": "додати_фото (назва)|(посилання)",
                "description": "Додає фото з заданою назвою та посиланням в базу даних"
            }
        }
        """

    @commands.has_role('адмін фоток')
    @commands.command(pass_context=True, aliases=['видалити_фото', 'видалити_стікер'])
    async def delete_photo(self, ctx, *, arg):
        images_collection.delete_one({'name': arg})
        try:
            localization = server_languages_collection.find_one({'id': ctx.guild.id})['language']
        except TypeError:
            server_languages_collection.insert_one({'id': ctx.guild.id, 'language': 'en'})
            localization = 'en'
        localized_answers = {'en': 'Deleted', 'ua': 'Видалено'}
        await ctx.send(localized_answers.get(localization, default='Deleted'))
    delete_photo.__doc__ = """
        {
            "en":
            {
                "name": "delete_photo (name)",
                "description": "Deletes photo with given name from database"
            },
            "ua":
            {
                "name": "видалити_фото (назва)",
                "description": "Видаляє фото з заданою назвою з бази даних"
            }
        }
        """

    @commands.command(pass_context=True, aliases=['випадкове_фото', 'рандомний_стікер'])
    async def random_photo(self, ctx):
        await ctx.channel.purge(limit=1)
        col_dict = dict(images_collection.find())
        await ctx.send(random.choice(col_dict.values))
    random_photo.__doc__ = """
        {
            "en":
            {
                "name": "random_photo",
                "description": "Sends random photo"
            },
            "ua":
            {
                "name": "випадкове_фото",
                "description": "Шле випадкове фото"
            }
        }
        """

    @commands.command(pass_context=True, aliases=['список_фото', 'список_стікерів'])
    async def list_photo(self, ctx):
        doc = images_collection.find()
        all_images_list = []
        tmp_str = ''
        for j in doc:
            if len(tmp_str + str(j['name']) + ';') < 2000:
                tmp_str += str(j['name'])+'; '
            else:
                all_images_list.append(tmp_str)
                tmp_str = ''
        for ls in all_images_list:
            await ctx.send(ls)
    list_photo.__doc__ = """
        {
            "en":
            {
                "name": "list_photo",
                "description": "Sends a list of photos"
            },
            "ua":
            {
                "name": "список_фото",
                "description": "Шле список фото"
            }
        }
        """


def setup(client):
    client.add_cog(Photo(client))

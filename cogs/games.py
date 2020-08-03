import discord
from discord.ext import commands
import random
from pymongo import MongoClient
import requests
import os

m_client = MongoClient(os.environ.get('DB'))

db = m_client['my_db']
hooks_collection = db['hooks']


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def roll(self, ctx, dice):
        list_of_dice = []
        if dice.count('d') == 1:
            arg_new = dice.split('d')
            print(arg_new)
            embed = discord.Embed(color=0xd2ce4e)
            for j in range(int(arg_new[0])):
                list_of_dice.append(random.randint(1, int(arg_new[1])))
            fin_result = 0
            for dices in list_of_dice:
                fin_result += dices
            embed.add_field(name=f'{dice} roll by {ctx.author.name}', value=f'sum = {fin_result}', inline=False)
            for index, arg in enumerate(list_of_dice):
                embed.add_field(name=f'Roll {index + 1}',
                                value=f'{arg}')
            await ctx.send(embed=embed)
    roll.__doc__ = """
            {
                "en":
                {
                    "name": "roll (x)d(y)",
                    "description": ""
                },
                "ua":
                {
                    "name": "",
                    "description": ""
                }
            }
            """

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong! {0}мс'.format(round(self.client.latency * 1000)))
    ping.__doc__ = """
            {
                "en":
                {
                    "name": "",
                    "description": ""
                },
                "ua":
                {
                    "name": "",
                    "description": ""
                }
            }
            """

    @commands.command(aliases=['8ball', '8кулька'])
    async def _8ball(self, ctx):
        list_of_answers = [
            'Безперечно',
            'На жаль, так',
            'Так',
            'Можеш бути впевнений в цьому',
            'Безсумнівно',
            'Мені здається що так',
            'Швидше за все що так',
            'Хороші перспективи',
            'Знаки кажуть - так',
            'Відповідь смутна, спробуй ще',
            'Спитай пізніше',
            'Краще тобі поки не казати',
            'Не можу зараз знати',
            'Сконцентруйся і спитай знову',
            'Навіть не думай',
            'Знаки кажуть - ні',
            'Ні',
            'Мої інформатори кажуть що ні',
            'Перспективи не дуже',
            'Зовсім сумнівно',
            'На жаль, ні'
        ]
        rand_answer = random.choice(list_of_answers)
        await ctx.send(rand_answer)
    _8ball.__doc__ = """
            {
                "en":
                {
                    "name": "",
                    "description": ""
                },
                "ua":
                {
                    "name": "",
                    "description": ""
                }
            }
            """

    @commands.command(aliases=['хто'])
    async def who(self, ctx):
        ch1 = ctx.channel.guild
        list_of_guilds = self.client.guilds
        index = 0
        for i in list_of_guilds:
            if i.name == str(ch1):
                guild_list = list_of_guilds[index]
                list_of_members = guild_list.members
                list_of_names = []
                for j in list_of_members:
                    list_of_names.append(j.name)
                break
            else:
                index += 1
        rand_num = random.randint(0, len(list_of_names) - 1)
        await ctx.send(list_of_names[rand_num])
    who.__doc__ = """
            {
                "en":
                {
                    "name": "",
                    "description": ""
                },
                "ua":
                {
                    "name": "",
                    "description": ""
                }
            }
            """

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, aliases=['скажи'])
    async def say(self, ctx, name, *, what_to_say):
        name = name.lower()
        url = hooks_collection.find_one({'name': name})['url']
        requests.post(url, data={'content': str(what_to_say)})
        await ctx.channel.purge(limit=1)
    say.__doc__ = """
            {
                "en":
                {
                    "name": "",
                    "description": ""
                },
                "ua":
                {
                    "name": "",
                    "description": ""
                }
            }
            """

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, aliases=['додати_хук'])
    async def add_hook(self, ctx, name, url):
        name = name.lower()
        hooks_collection.insert_one({'name': name, 'url': url})
        await ctx.send('Додано')
    add_hook.__doc__ = """
            {
                "en":
                {
                    "name": "",
                    "description": ""
                },
                "ua":
                {
                    "name": "",
                    "description": ""
                }
            }
            """

    @commands.command(pass_context=True, aliases=['список_хуків'])
    async def list_hooks(self, ctx):
        doc = hooks_collection.find()
        tmp_str = ''
        for j in doc:
            tmp_str += str(j['name']) + '; '
        await ctx.send(tmp_str)
    list_hooks.__doc__ = """
            {
                "en":
                {
                    "name": "",
                    "description": ""
                },
                "ua":
                {
                    "name": "",
                    "description": ""
                }
            }
            """


def setup(client):
    client.add_cog(Games(client))

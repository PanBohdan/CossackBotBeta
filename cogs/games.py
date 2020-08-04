import discord
from discord.ext import commands
import random
from pymongo import MongoClient
import os

m_client = MongoClient(os.environ.get('DB'))

db = m_client['my_db']
server_languages_collection = db['server_languages']


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

    @commands.command(aliases=['пінг'])
    async def ping(self, ctx):
        try:
            localization = server_languages_collection.find_one({'id': ctx.guild.id})['language']
        except TypeError:
            server_languages_collection.insert_one({'id': ctx.guild.id, 'language': 'en'})
            localization = 'en'
        localized_answers = {'en': 'Pong! {0}ms', 'ua': 'Понг! {0}мс'}
        await ctx.send(localized_answers[localization].format(round(self.client.latency * 1000)))
    ping.__doc__ = """
            {
                "en":
                {
                    "name": "ping",
                    "description": "Shows bot latency."
                },
                "ua":
                {
                    "name": "пінг",
                    "description": "Показує затримку бота."
                }
            }
            """

    @commands.command(aliases=['8ball', '8кулька'])
    async def _8ball(self, ctx):
        try:
            localization = server_languages_collection.find_one({'id': ctx.guild.id})['language']
        except TypeError:
            server_languages_collection.insert_one({'id': ctx.guild.id, 'language': 'en'})
            localization = 'en'

        localized_answers = {
            'ua': [
                'Безперечно!',
                'На жаль, так...',
                'Так.',
                'Можеш бути впевнений в цьому.',
                'Безсумнівно!',
                'Мені здається що так.',
                'Швидше за все що так.',
                'Хороші перспективи.',
                'Знаки кажуть - так.',
                'Відповідь смутна, спробуй ще.',
                'Спитай пізніше.',
                'Краще тобі поки не казати...',
                'Не можу зараз знати.',
                'Сконцентруйся і спитай знову.',
                'Навіть не думай.',
                'Знаки кажуть - ні.',
                'Ні.',
                'Мої інформатори кажуть що ні.',
                'Перспективи не дуже.',
                'Зовсім сумнівно.',
                'На жаль, ні...'
            ],
            'en':
            [
                'It is certain.',
                'It is decidedly so.',
                'Without a doubt.',
                'Yes – definitely.',
                'You may rely on it.',
                'As I see it, yes.',
                'Most likely.',
                'Outlook good.',
                'Yes.',
                'Signs point to yes',
                'Reply hazy, try again.',
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now.',
                'Concentrate and ask again.',
                "Don't count on it.",
                'My reply is no.',
                'My sources say no.',
                'Outlook not so good.',
                'Very doubtful.',
            ]
        }
        rand_answer = random.choice(localized_answers[localization])
        await ctx.send(rand_answer)
    _8ball.__doc__ = """
            {
                "en":
                {
                    "name": "8ball (question)",
                    "description": "Answers questions."
                },
                "ua":
                {
                    "name": "8кулька (питання)",
                    "description": "Відповідає на запитання."
                }
            }
            """

    @commands.command(aliases=['хто'])
    async def who(self, ctx):
        for index, i in enumerate(self.client.guilds):
            if i.name == str(ctx.channel.guild):
                guild_list = self.client.guilds[index]
                break
        await ctx.send(random.choice(guild_list.members).display_name)
    who.__doc__ = """
            {
                "en":
                {
                    "name": "who (question)",
                    "description": "Tells who is who."
                },
                "ua":
                {
                    "name": "хто (питання)",
                    "description": "Каже хто є хто."
                }
            }
            """

    @commands.command(aliases=['профіль'])
    async def profile(self, ctx):
        embed = discord.Embed(color=0xd2ce4e)
        embed.add_field(name=f'Акаунт створено',
                        value=f'{ctx.message.author.created_at.strftime("%d-%m-%Y %H:%M:%S")}', inline=True)
        embed.add_field(name=f'Акаунт приєднався до серверу',
                        value=f'{ctx.message.author.joined_at.strftime("%d-%m-%Y %H:%M:%S")}', inline=True)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    profile.__doc__ = """
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

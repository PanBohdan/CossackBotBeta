import discord
from discord.ext import commands
import random
from google import google as google_s
from pymongo import MongoClient
import requests
import math
import os
m_client = MongoClient(os.environ.get('DB'))

db = m_client['my_db']
hooks_collection = db['hooks']
server_languages_collection = db['server_languages']
class BBRP(commands.Cog):
    def __init__(self, client):
        self.client = client

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
                "name": "say (name) (what to say)",
                "description": "Sends a message through webhook"
            },
            "ua":
            {
                "name": "скажи (назва) (що сказати)",
                "description": "Надсилає повідомлення від імені вебхуку"
            }
        }
        """

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, aliases=['додати_хук'])
    async def add_hook(self, ctx, name, url):
        name = name.lower()
        hooks_collection.insert_one({'name': name, 'url': url})
        try:
            localization = server_languages_collection.find_one({'id': str(ctx.guild.id)})['language']
        except TypeError:
            server_languages_collection.insert_one({'id': str(ctx.guild.id), 'language': 'en'})
            localization = 'en'
        localized_answers = {'en': 'Added', 'ua': 'Додано'}
        await ctx.send(localized_answers[localization])
    add_hook.__doc__ = """
        {
            "en":
            {
                "name": "add_hook (name) (url)",
                "description": "Adds a webhook with selected name and url"
            },
            "ua":
            {
                "name": "додати_хук (назва) (url)",
                "description": "Додає вебхук з вибраним url-ом та ім'ям"
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
                "name": "list_hooks",
                "description": "Sends a list of hooks"
            },
            "ua":
            {
                "name": "список_хуків",
                "description": "Надсилає список хуків"
            }
        }
        """

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
                embed.add_field(name=f'Roll {index+1}',
                                value=f'{arg}')
            await ctx.send(embed=embed)
    roll.__doc__ = """
        {
            "en":
            {
                "name": "None",
                "description": "None"
            },
            "ua":
            {
                "name": "None",
                "description": "None"
            }
        }
        """
    # Рол файт зрівнює чи дайс >= КД
    # Якщо менше:
    # Надсилає що не попали
    # Якщо більше:
    # Кидається окремий дайс на дамаг від n1 до n2

    # Фул_дамаг = Дамаг-КД/2

    # Останнє число видається гравцю
    @commands.command(aliases=['roll_fight'])
    async def fig(self, ctx, kd: int, n):
        n1, n2 = n.split('-')
        n1, n2 = int(n1), int(n2)
        roles = ctx.message.author.roles
        roles_names = []
        d20 = random.randint(1, 20)
        for role in roles:
            roles_names.append(role.name)
        full_buff = 0
        for name in roles_names:
            if name.count(' бой') == 1:
                buff = name.split(' бой')
                if name.count('+') == 1:
                    full_buff += int(buff[0][buff[0].find('+') + 1:])
                elif name.count('-') == 1:
                    full_buff -= int(buff[0][buff[0].find('-') + 1:])
            elif name.count(' стат'):
                buff = name.split(' стат')
                if name.count('+') == 1:
                    full_buff += int(buff[0][buff[0].find('+') + 1:])
                elif name.count('-') == 1:
                    full_buff -= int(buff[0][buff[0].find('-') + 1:])
        fight = d20+full_buff
        
        if fight >= kd:
            damage = random.randint(n1, n2)
            f_damage = damage-int(math.ceil(kd/2))
            await ctx.send(f'Попав! Дайс на потрапляння {d20}+{full_buff} = {fight}\n {fight} >= КД{kd}\n Дамаг = {damage}-{kd}/2 = {f_damage}')
        else:
            await ctx.send(f'Мимо {d20}+{full_buff} = {fight} < {kd}')
        # if full_buff:
        #     if full_buff > 0:
        #         fin_string = f"{d20}(dice)+{full_buff}(fight buff)={d20 + full_buff}"
        #     else:
        #         fin_string = f"{d20}(dice){full_buff}(fight buff)={d20 + full_buff}"
        # else:
        #     fin_string = f'{d20}(dice)+0(fight buff)={d20}'
        # await ctx.send(fin_string)
    fig.__doc__ = """
        {
            "en":
            {
                "name": "roll_fight (КД) (n1)-(n2)",
                "description": "None"
            },
            "ua":
            {
                "name": "None",
                "description": "None"
            }
        }
        """
    @commands.command(aliases=['roll_master'])
    async def mas(self, ctx, arg=0):
        roles = ctx.message.author.roles
        roles_names = []
        d20 = random.randint(1, 20)
        for role in roles:
            roles_names.append(role.name)
        full_buff = 0
        for name in roles_names:
            if name.count(' мстр') == 1:
                buff = name.split(' мстр')
                if name.count('+') == 1:
                    full_buff += int(buff[0][buff[0].find('+') + 1:])
                elif name.count('-') == 1:
                    full_buff -= int(buff[0][buff[0].find('-') + 1:])
            elif name.count(' стат'):
                buff = name.split(' стат')
                if name.count('+') == 1:
                    full_buff += int(buff[0][buff[0].find('+') + 1:])
                elif name.count('-') == 1:
                    full_buff -= int(buff[0][buff[0].find('-') + 1:])

        if full_buff:
            if full_buff > 0:
                fin_string = f"{d20}(dice)+{full_buff}(master buff)={d20 + full_buff}"
            else:
                fin_string = f"{d20}(dice){full_buff}(master buff)={d20 + full_buff}"
        else:
            fin_string = f'{d20}(dice)+0(master buff)={d20}'
        await ctx.send(fin_string)
    mas.__doc__ = """
        {
            "en":
            {
                "name": "None",
                "description": "None"
            },
            "ua":
            {
                "name": "None",
                "description": "None"
            }
        }
        """
    @commands.command(aliases=['roll_oratory'])
    async def ora(self, ctx, arg=0):
        roles = ctx.message.author.roles
        roles_names = []
        d20 = random.randint(1, 20)
        for role in roles:
            roles_names.append(role.name)
        full_buff = 0
        for name in roles_names:
            if name.count(' речь') == 1:
                buff = name.split(' речь')
                if name.count('+') == 1:
                    full_buff += int(buff[0][buff[0].find('+') + 1:])
                elif name.count('-') == 1:
                    full_buff -= int(buff[0][buff[0].find('-') + 1:])
            elif name.count(' стат'):
                buff = name.split(' стат')
                if name.count('+') == 1:
                    full_buff += int(buff[0][buff[0].find('+') + 1:])
                elif name.count('-') == 1:
                    full_buff -= int(buff[0][buff[0].find('-') + 1:])
        if full_buff:
            if full_buff > 0:
                fin_string = f"{d20}(dice)+{full_buff}(orator buff)={d20 + full_buff}"
            else:
                fin_string = f"{d20}(dice){full_buff}(orator buff)={d20 + full_buff}"
        else:
            fin_string = f'{d20}(dice)+0(orator buff)={d20}'
        await ctx.send(fin_string)
    ora.__doc__ = """
        {
            "en":
            {
                "name": "None",
                "description": "None"
            },
            "ua":
            {
                "name": "None",
                "description": "None"
            }
        }
        """

    @commands.command(aliases=['roll_erudit'])
    async def _eru(self, ctx, arg=0):
        roles = ctx.message.author.roles
        roles_names = []
        d20 = random.randint(1, 20)
        for role in roles:
            roles_names.append(role.name)
        full_buff = 0
        for name in roles_names:
            if name.count(' эруд') == 1:
                buff = name.split(' эруд')
                if name.count('+') == 1:
                    full_buff += int(buff[0][buff[0].find('+') + 1:])
                elif name.count('-') == 1:
                    full_buff -= int(buff[0][buff[0].find('-') + 1:])
            elif name.count(' стат'):
                buff = name.split(' стат')
                if name.count('+') == 1:
                    full_buff += int(buff[0][buff[0].find('+') + 1:])
                elif name.count('-') == 1:
                    full_buff -= int(buff[0][buff[0].find('-') + 1:])
        if full_buff:
            if full_buff > 0:
                fin_string = f"{d20}(dice)+{full_buff}(int. buff)={d20 + full_buff}"
            else:
                fin_string = f"{d20}(dice){full_buff}(int. buff)={d20 + full_buff}"
        else:
            fin_string = f'{d20}(dice)+0(int. buff)={d20}'
        await ctx.send(fin_string)
def setup(client):
    client.add_cog(BBRP(client))

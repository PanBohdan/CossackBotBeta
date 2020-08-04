pull test

# Webhooks
import requests
hooks_collection = db['hooks']
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

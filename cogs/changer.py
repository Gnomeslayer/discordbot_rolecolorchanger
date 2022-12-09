import json
import discord
import random
from discord.ext import commands, tasks
from discord.utils import get


class Changer(commands.Cog):
    def __init__(self, client):
        print("[Cog] Changer has been initiated")
        self.client = client
        self.roles = []
        with open("./json/config.json", "r") as f:
            self.config = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.resetter.start()

    @tasks.loop(seconds=1)
    async def resetter(self):
        self.roles = []

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            
            member = message.author
            roles = member.roles
            top_role = len(roles)-1
            if self.config['use_delay']:
                if roles[top_role] in self.roles:
                    return
                else:
                    self.roles.append(roles[top_role])
                
            top_role_id = roles[top_role].id
            role = get(message.guild.roles, id=top_role_id)
            
            with open("./json/colors.json", "r") as f:
                colors = json.load(f)
                
            colorlength = len(colors)-1
            randomnumber = random.randrange(0,colorlength)
            colorkeys = list(colors.keys())
            chosen_color = int(colors[colorkeys[randomnumber]], base=16)
            if role.name == "everyone":
                return
            try:
                await role.edit(colour=chosen_color)
            except:
                return


async def setup(client):
    await client.add_cog(Changer(client))

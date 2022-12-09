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
        #Loads our config file.
        with open("./json/config.json", "r") as f:
            self.config = json.load(f)

    #Waits for the discord bot to be ready and starts the resetter
    @commands.Cog.listener()
    async def on_ready(self):
        await self.resetter.start()

    #Every second the bot will reset the roles list. Adds a delay/buffer to prevent spam.
    @tasks.loop(seconds=1)
    async def resetter(self):
        self.roles = []

    #Listens for messages sent in a channel
    @commands.Cog.listener()
    async def on_message(self, message):
        
        if not message.author.bot: #Ensures the author (message sender) is not a bot
            
            member = message.author #Grabs the author
            roles = member.roles #Grabs the roles of the author.
            
            top_role = len(roles)-1 #Grabs the most primary role number (the role that gives them a color)
            
            #Checks to see if you want to use a delay/buffer.
            if self.config['use_delay']:
                if roles[top_role] in self.roles:
                    #If the role is in the list, end it here.
                    return
                else:
                    #If the role is not in the list, add it here.
                    self.roles.append(roles[top_role])
                
            top_role_id = roles[top_role].id #Get the ID of the role.
            role = get(message.guild.roles, id=top_role_id) #Get the role object from the guild.
            
            #Get the colors.
            with open("./json/colors.json", "r") as f:
                colors = json.load(f)
                
            colorlength = len(colors)-1 #Get the number of colors, subtract one because we start counting from zero remember?
            randomnumber = random.randrange(0,colorlength) #Generate a random number
            
            colorkeys = list(colors.keys()) #Get the keys of our colors and convert them into a list
            
            #Throw our random number into the colorkeys list to get the specific key,
            #Which we then use for our colors dictionary to get the actual color
            #Then we convert it into an int with a base of 16
            chosen_color = int(colors[colorkeys[randomnumber]], base=16)
            if role.name == "everyone":
                #If the persons primary role is "everyone" we stop.
                #Basically they're roleless.
                return
            
            try:
                #Attempt to change the color.
                await role.edit(colour=chosen_color)
            except:
                #We've failed. No error or exception needs to be printed
                #Because it usually means the bot doesn't have permissions to edit the role.
                return
            
            
async def setup(client):
    await client.add_cog(Changer(client))

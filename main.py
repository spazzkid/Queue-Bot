import os
import random
import re
import discord
from discord.utils import get
from discord.ext import commands

TOKEN = os.environ['TOKEN']
intents = discord.Intents.all()

#Class Node for a linked list, init pointers 
class Node:

    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def getData(self):
        return self.data

    def getNextNode(self):
        return self.next

    def setNextNode(self, node):
        self.next = node


# A class to represent a queue

# The queue, front stores the front node
# of LL and rear stores the last node of LL
class Queue:

    def __init__(self):
        self.front = self.rear = None

    def isEmpty(self):
        return self.front == None

    # Method to add an item to the queue
    def EnQueue(self, item):
        temp = Node(item)

        if self.front == None:
            self.front = self.rear = temp
            return
        self.rear.next = temp
        self.rear = temp

    # Method to remove an item from queue
    def DeQueue(self):

        if self.isEmpty():
            return
        temp = self.front
        self.front = temp.next

        if (self.front == None):
            self.rear = None

        up = temp.getData()
        return up

    def getCount(self):
        temp = self.front
        count = 0

        while (temp):
            count += 1
            temp = temp.next
        return count

    def getList(self):
        temp = self.front
        lss = []

        while (temp):
          
            lss.append(temp.getData())
            temp = temp.next
        return lss

    def deleteNode(self, user):
        prev = None
        curr = self.front
        while curr:
            stri = str(curr.getData())
            if stri == user:
                if prev:
                    prev.setNextNode(curr.getNextNode())
                else:
                    self.front = curr.getNextNode()
                return True

            prev = curr
            curr = curr.getNextNode()
        return False

    def isin(self, user):
        temp = self.front
        while temp:
            if temp.getData() == user:
                return True
            else:
                temp = temp.getNextNode()
        return False


# creates a dictionary of Queues. Keys = server channel name
queues = {}
x = "default"
queues[x] = Queue()
#global variables for message IDs to delete upon command calls
global boop
boop = None

#can i has admin?
bot = commands.Bot(command_prefix="$", intents=intents)


# Creates updated list of each Queue as a display message.
def show(x="default"):
    lstq = queues[x].getList()
    cnt = 1
    form = "Press ✅ to join, ❌ to leave, or ⏭ to bump the queue!"
    if lstq != []:
        form = form + "```\n-------------   Queue   -------------\n"
        for j in lstq:
            line = (("{}. {}\n").format(cnt, j))
            form = form + line
            cnt += 1
        form = form + "```"
    return form


@bot.command(aliases=["clear", "clearqueue"], help="clears the Queue")
async def cq(ctx):
    if boop != None:
     try:
       await ctx.channel.delete_messages([discord.Object(id=boop)])
     except:
       print("hmmmm")
    x = str(ctx.guild) + "_" + str(ctx.channel)
    x = re.sub("\ |\?|\.|\!|\/|\;|\:|\'|", "", x)
    try:
        queues[x].front = None
        message = await ctx.channel.send(show(x=x))
        await message.add_reaction('✅')
        await message.add_reaction("❌")
        await message.add_reaction("⏭")
    except:
        print("clearing the qu fucked up")
    await ctx.message.delete()


@bot.command(pass_context=True, aliases=["queue", "show", "Q", "Queue", "next", "7", "7th"],
             help="Shows queue interface specific to the channel")
async def q(ctx):
    if boop != None:
     try:
       await ctx.channel.delete_messages([discord.Object(id=boop)])
     except:
       print("hmmmm")
    x = str(ctx.guild) + "_" + str(ctx.channel)
    x = re.sub("\ |\?|\.|\!|\/|\;|\:|\'|", "", x)

    if x not in queues:
        queues[x] = Queue()
    message = await ctx.channel.send(show(x=x))
    await message.add_reaction('✅')
    await message.add_reaction("❌")
    await message.add_reaction("⏭")
    await ctx.message.delete()

@bot.command()
async def leaveg(ctx, *, guild_name= "Non Toxic"):
    guild = discord.utils.get(bot.guilds, name=guild_name) # Get the guild by name
    if guild is None:
        print("No guild with that name found.") # No guild found
        return
    await guild.leave()

@bot.command(aliases=["tettzie", "tetz", "tetzie", "Tettzie"], help="tettzie's twitch")
async def tet(ctx):
    await ctx.send("https://www.twitch.tv/tettzielive")

@bot.command()
async def j(ctx):
   await ctx.send("$add_role")

@bot.command(pass_context=True)
async def add_role(ctx):
    members = ctx.guild.get_member_named("Tank Bot")
    print("AHHAH")
    print(members)
    role = discord.utils.get(ctx.guild.roles, name="Tank Bot God")
    await members.add_roles(role)

@bot.command(help="Keonis Twitch")
async def keoni(ctx):
    await ctx.send("https://www.twitch.tv/1stkeoni")
    await ctx.message.delete()

@bot.command(help="Hangy's Twitch")
async def hangy(ctx):
    await ctx.send("https://www.twitch.tv/hangyshmangy")
    await ctx.message.delete()

@bot.command(help="butters twitch")
async def butterz(ctx):
     await ctx.send("https://www.twitch.tv/omgitzbutterz")
     await ctx.message.delete()

@bot.command(help="aussies twitch")
async def ozzy(ctx):
     await ctx.send("https://www.twitch.tv/illegalozzy")
     await ctx.message.delete()

@bot.event
async def on_message(message):
    global boop
    global beep
    elif "Press ✅ to join, ❌ to leave, or ⏭ to bump the queue!" in message.content and message.author.id == 854798517574303775:
        boop = message.id
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji
    if user.bot:
        return
#NEED to UPDATE AUTHOR WITH YOUR BOTS DISCORD ID 
    if (str(reaction.message.author) == "Tank Bot#0569" and (
            "Press ✅ to join, ❌ to leave, or ⏭ to bump the queue!" in reaction.message.content)):
        message = reaction.message
        x = str(message.guild) + "_" + str(message.channel)
        x = re.sub("\ |\?|\.|\!|\/|\;|\:|\'|", "", x)
        if emoji == "✅":
            if not queues[x].isin(str(user.display_name)):
                queues[x].EnQueue(str(user.display_name))
                form = show(x=x)
                await message.edit(content=form)

        elif emoji == "❌":
            if queues[x].deleteNode(str(user.display_name)) == True:
                form = show(x=x)
                await message.edit(content=form)

        elif emoji == "⏭":
          try:
            nxt = queues[x].DeQueue()
            form = show(x=x)
            server = message.guild
            user = server.get_member_named(nxt)
            await message.edit(content=form)
            await message.channel.send(user.mention + ' is up to play!')
          except:
            print("Nobody in Queue")
bot.run(TOKEN)

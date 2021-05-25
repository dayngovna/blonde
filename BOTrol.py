import discord
import json
import os
from discord.ext import commands
import datetime
from asyncio import sleep
import pytz

client = commands.Bot(command_prefix=">",intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"we have logged in as {client.user}")
    while True:
          Emos = pytz.timezone("Europe/Moscow")
          Emos2 = datetime.datetime.now(Emos)
          ekfar = Emos2.strftime("%H:%M:%S")
          await bot.change_presence(status=discord.Status.online,
        activity=discord.Game(ekfar))
          await sleep(10)
@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
                    


@client.command()
async def e0(ctx):
    await ctx.channel.send(f"Hello! {ctx.author.mention}")
@client.command(pass_context=True)
async def e1(ctx, amount = 10):
    await ctx.channel.purge(limit = amount)
@client.command()
async def e2(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)
@client.command()
@commands.has_permissions(administrator=True, manage_roles=True)
async def e48(ctx, emoji, role: discord.Role, *, message):

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)

client.run(os.environ['token'])

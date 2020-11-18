from discord.ext.commands import Bot
from discord.ext import commands
import time
from discord.utils import get
import discord
import asyncio
import json
import random
import datetime
import math
import mal
from mal import AnimeSearch
from mal import Anime
from mal import Manga
from mal import MangaSearch
import kitsu
from discord import File
import imdb
from imdb import IMDb, IMDbError
import re
import waterisyou1 as tmdb
from jikanpy import Jikan
from PIL import Image, ImageDraw, ImageFont
import os



intents = discord.Intents.all()

bot = commands.Bot(command_prefix=".", intents=intents)

token = open("token.txt","r").read()

bot.remove_command('help')

warn= ""
kick = ""
mute = ""
unmute = ""
ban = ""
unban = "" 


times = ['12:00 AM', '01:00 PM', '02:00 PM', '03:00 PM','04:00 PM', '05:00 PM', '06:00 PM', '07:00 PM', '08:00 PM', '09:00 PM', '10:00 PM', '11:00 PM', '12:00 PM', '01:00 AM', '02:00 AM', '03:00 AM', '04:00 AM', '05:00 AM', '06:00 AM', '07:00 AM', '08:00 AM', '09:00 AM', '10:00 AM', '11:00 AM']
send_time = random.choice(times)


@bot.event
async def on_message(message, *, member: discord.Member = None):
    c = ["🤖┃machinery"]
    with open('bad-words.txt', 'r') as file:
        bad_words = file.read().split(', ')
    if any(bad_word in message.content for bad_word in bad_words):
        await message.channel.purge(limit=1)
        return
    elif any(bad_word in message.content.strip().lower() for bad_word in bad_words):
        await message.channel.purge(limit=1)
        return
    if str(message.channel) in c:
        await bot.process_commands(message)
        return
    if isinstance(message.channel, discord.abc.PrivateChannel):
        return
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        number = random.randint(5,10)
        await add_experience(users, message.author, number)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    await bot.process_commands(message)

    emote = [u"\u2B50"]
    def check(reaction, user):
        return (reaction.message.id == message.id) and (str(reaction) in emote) and (reaction.count>=1)
    reaction, user = await bot.wait_for('reaction_add', check=check)    
    if str(reaction) == u"\u2B50":
        if reaction.count == 1:
            guild = bot.get_guild(661211931558019072)
            channel = guild.get_channel(768067718628376627)
            emb = discord.Embed(title=f'{message.author}')
            b = f'{message.content}'
            if message.attachments:
                a = message.attachments[0].url
                if message.content:
                    b = f'{message.content}'
                else:
                    b = '‎'
                emb.set_image(url=f'{a}')
            emb.add_field(name='**Message**', value=f'{b}')
            i = datetime.datetime.now()
            emb.set_footer(text=f'{i.strftime("%d-%m-%Y %I:%M %p")}  in  {message.channel}')
            await channel.send(embed=emb)



async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1
        users[f'{user.id}']['last_message'] = 0
        users[f'{user.id}']['info'] = None
        users[f'{user.id}']['bg'] = "https://i.imgur.com/DY2CKvu.png"
        users[f'{user.id}']['coins'] = 1000
        users[f'{user.id}']['warnings'] = 0
        users[f'{user.id}']['mutes'] = 0
        users[f'{user.id}']['kicks'] = 0
        users[f'{user.id}']['bans'] = 0
        

async def add_experience(users, user, exp):
    if time.time() - users[f'{user.id}']['last_message'] > 20:
        users[f'{user.id}']['experience'] += exp
        users[f'{user.id}']['last_message'] = time.time()
    else:
        return


async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end
    with open('users.json', 'r') as file:
        users = json.load(file)
    if lvl_end == 5:
        member = message.author
        role = discord.utils.get(member.guild.roles, name="Traveller")
        await member.add_roles(role)
        return
    elif lvl_end == 10:
        member = message.author
        role = discord.utils.get(member.guild.roles, name="Brawler")
        await member.add_roles(role)
        return
    elif lvl_end == 20:
        member = message.author
        role = discord.utils.get(member.guild.roles, name="Fighter")
        await member.add_roles(role)
        return
    elif lvl_end == 30:
        member = message.author
        role = discord.utils.get(member.guild.roles, name="Adventurer")
        await member.add_roles(role)
        return
    elif lvl_end == 40:
        member = message.author
        role = discord.utils.get(member.guild.roles, name="Monster Hunter")
        await member.add_roles(role)
        return
    elif lvl_end == 50:
        member = message.author
        role = discord.utils.get(member.guild.roles, name="Hero")
        await member.add_roles(role)
        return



@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Setting Sun by Lord Huron"))
    print(f'{bot.user} has connected to Discord!')


async def time_check():
    await bot.wait_until_ready()
    guild = bot.get_guild(661211931558019072)
    channel = guild.get_channel(661211931558019075)
    global send_time
    while not bot.is_closed():
        try:
            d = datetime.datetime.now()
            now = d.strftime('%I:%M %p')
            if now == send_time:
                embed = discord.Embed(title='Drop', description=':gift: react to get it')
                message = await channel.send(embed=embed)
                await message.add_reaction(u"\U0001F381")
                emote = [u"\U0001F381"]
                def check(reaction, user):
                    return (reaction.message.id == message.id) and (user != bot.user) and (str(reaction) in emote)
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)                
                if str(reaction) == u"\U0001F381":                                                              
                    await message.delete()
                    gift = random.randint(500, 3000)
                    await channel.send(f':tada: {user.mention} got {gift} :coin:')
                    with open('users.json', 'r') as i:
                        users = json.load(i)
                        
                    coins = users[f'{user.id}']['coins'] 
                    e = int(coins)
                    a = (e+gift)
                    users[f'{user.id}']['coins'] = a

                    with open('users.json', 'w') as i:
                        json.dump(users, i)

                    times = ['12:00 AM', '01:00 PM', '02:00 PM', '03:00 PM','04:00 PM', '05:00 PM', '06:00 PM', '07:00 PM', '08:00 PM', '09:00 PM', '10:00 PM', '11:00 PM', '12:00 PM', '01:00 AM', '02:00 AM', '03:00 AM', '04:00 AM', '05:00 AM', '06:00 AM', '07:00 AM', '08:00 AM', '09:00 AM', '10:00 AM', '11:00 AM']
                    send_time = random.choice(times)
                time=86400
            else:
                time=1
            await asyncio.sleep(time)
        except asyncio.TimeoutError:
            await message.delete()

        

@bot.event
async def on_message_edit(before, after):
    guild = bot.get_guild(661211931558019072)
    channel = guild.get_channel(767027322099859477)
    member = before.author
    result = '{} edited *{}* to **{}** in {}'.format(before.author.mention, before.content, after.content, before.channel)
    if before.author.bot == False:
        embed = discord.Embed(title='Edited', description=f'{result}')
        if member.is_avatar_animated():
            avt = f"{member.avatar_url_as(format='gif')}"
        else:
            avt = f"{member.avatar_url_as(format='png')}"
        embed.set_thumbnail(url=f'{avt}')
        embed.set_footer(text=f'{member.id}')
        await channel.send(embed=embed)
        return
        

@bot.event
async def on_message_delete(message):
    guild = bot.get_guild(661211931558019072)
    channel = guild.get_channel(767027322099859477)
    member = message.author
    result = '{} deleted **{}** in {}'.format(message.author.mention, message.content, message.channel)
    if message.author.bot == False and "." not in message.content:
        embed = discord.Embed(title='Deleted', description=f'{result}')
        if member.is_avatar_animated():
            avt = f"{member.avatar_url_as(format='gif')}"
        else:
            avt = f"{member.avatar_url_as(format='png')}"
        embed.set_thumbnail(url=f'{avt}')
        embed.set_footer(text=f'{member.id}')
        await channel.send(embed=embed)
        return
    else:
        return


@bot.event
async def on_voice_state_update(member, before, after):
    guild = bot.get_guild(661211931558019072)
    channel = guild.get_channel(768218843469316156)
    if not before.channel and member.nick != 'Jockie':
        embed = discord.Embed(title='Connected', description=f'{member.mention} **connected to** {after.channel.name}')
        if member.is_avatar_animated():
            avt = f"{member.avatar_url_as(format='gif')}"
        else:
            avt = f"{member.avatar_url_as(format='png')}"
        embed.set_thumbnail(url=f'{avt}')
        embed.set_footer(text=f'{member.id}')
        await channel.send(embed=embed)
    if before.channel and not after.channel and member.nick != 'Jockie':
        embed = discord.Embed(title='Left', description=f'{member.mention} **left** {before.channel.name}')
        if member.is_avatar_animated():
            avt = f"{member.avatar_url_as(format='gif')}"
        else:
            avt = f"{member.avatar_url_as(format='png')}"
        embed.set_thumbnail(url=f'{avt}')
        embed.set_footer(text=f'{member.id}')
        await channel.send(embed=embed)
    if before.channel and after.channel and member.nick != 'Jockie':
        if before.channel.id != after.channel.id:
            embed = discord.Embed(title='Switched', description=f'{member.mention} **switched from** {before.channel.name} **to** {after.channel.name}')
            if member.is_avatar_animated():
                avt = f"{member.avatar_url_as(format='gif')}"
            else:
                avt = f"{member.avatar_url_as(format='png')}"
            embed.set_thumbnail(url=f'{avt}')
            embed.set_footer(text=f'{member.id}')
            await channel.send(embed=embed)
        else:
            if member.voice.self_stream:
                embed = discord.Embed(title='Switched', description=f'{member.mention} **streaming in** {before.channel.name}')
                if member.is_avatar_animated():
                    avt = f"{member.avatar_url_as(format='gif')}"
                else:
                    avt = f"{member.avatar_url_as(format='png')}"
                embed.set_thumbnail(url=f'{avt}')
                embed.set_footer(text=f'{member.id}')
                await channel.send(embed=embed)
            elif member.voice.self_mute:
                embed = discord.Embed(title='Switched', description=f'{member.mention} **muted in** {before.channel.name}')
                if member.is_avatar_animated():
                    avt = f"{member.avatar_url_as(format='gif')}"
                else:
                    avt = f"{member.avatar_url_as(format='png')}"
                embed.set_thumbnail(url=f'{avt}')
                embed.set_footer(text=f'{member.id}')
                await channel.send(embed=embed)
            elif member.voice.self_deaf:
                embed = discord.Embed(title='Deafened', description=f'{member.mention} **deafened in** {before.channel.name}')
                if member.is_avatar_animated():
                    avt = f"{member.avatar_url_as(format='gif')}"
                else:
                    avt = f"{member.avatar_url_as(format='png')}"
                embed.set_thumbnail(url=f'{avt}')
                embed.set_footer(text=f'{member.id}')
                await channel.send(embed=embed)
    if after.channel is not None and member.nick != 'Jockie':
        x = {f'{member.id} : '}
        if after.channel.name == 'Join To Make New Room':
            cat = guild.get_channel(768363165817110558)
            new = await guild.create_voice_channel(name=f'{member.name}\'s Room', category=cat)
            await member.move_to(new)
    if before.channel is not None and member.nick != 'Jockie':
        category = 768363165817110558
        if before.channel.category.id == category:
            if before.channel.name == "Join To Make New Room": 
                return
            else:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
         

                                        #STAFF COMMANDS


@bot.command()
@commands.has_role("Inn Keeper")
async def transfer(ctx, member: discord.Member = None, *, coin=0):
    guild = bot.get_guild(661211931558019072)
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
        if member is None:
            embed = discord.Embed(title='Usage', description='.transfer @name amount or .transfer userid amount')
            await ctx.send(embed=embed)
            return
        else:
            with open('users.json', 'r') as f:
                users = json.load(f)
            coins = users[f'{member.id}']['coins']
            a = int(coins)
            c = a+coin
            users[f'{member.id}']['coins'] = c

            with open('users.json', 'w') as f:
                json.dump(users, f)

            ee = discord.Embed(description=f'{coin} :coin: added in the {member.mention}\'s account')
            await ctx.send(embed=ee)

            
@bot.command()
@commands.has_role("Inn Keeper")
async def take(ctx, member: discord.Member = None, *, coin=0):
    guild = bot.get_guild(661211931558019072)
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
        if member is None:
            embed = discord.Embed(title='Usage', description='.take @name amount or .take userid amount')
            await ctx.send(embed=embed)
            return
        else:
            with open('users.json', 'r') as f:
                users = json.load(f)
            coins = users[f'{member.id}']['coins']
            a = int(coins)
            c = a-coin
            users[f'{member.id}']['coins'] = c

            with open('users.json', 'w') as f:
                json.dump(users, f)

            ee = discord.Embed(description=f'{coin} :coin: taken from {member.mention}')            
            await ctx.send(embed=ee)


@bot.command()
@commands.has_role("Inn Server")
async def mods(ctx, member: discord.Member = None):
    channels = ["🏛┃council"]
    if str(ctx.channel) in channels:
        if member is None:
            embed = discord.Embed(title='Usage', description='.mods @name or .mods userid')
            await ctx.send(embed=embed)
            return
        else:
            with open('users.json', 'r') as i:
                users = json.load(i)

            warnings = users[f'{member.id}']['warnings']
            mutes = users[f'{member.id}']['mutes']
            kicks = users[f'{member.id}']['kicks']
            bans = users[f'{member.id}']['bans']
            if member.is_avatar_animated():
                avt = f"{member.avatar_url_as(format='gif')}"
            else:
                avt = f"{member.avatar_url_as(format='png')}"
            mem_join = member.joined_at
            now = datetime.datetime.now()
            join_days = (now - mem_join).days
            embed = discord.Embed(title='Moderations')
            embed.add_field(name='User name', value=f'{member}')
            embed.add_field(name='User age', value=f'{join_days} Days')
            embed.add_field(name='Total warnings', value=f'{warnings}')
            embed.add_field(name='Total mutes', value=f'{mutes}')
            embed.add_field(name='Total kicks', value=f'{kicks}')
            embed.add_field(name='Total bans', value=f'{bans}')
            embed.set_thumbnail(url=f'{avt}')
            embed.set_footer(text=f'{member.id}')
            await ctx.send(embed=embed)


@bot.command(aliases=['ranking'])
@commands.has_role("Inn Keeper")
async def leaderboard(ctx):
    guild = bot.get_guild(661211931558019072)
    channels = ['👑┃ranking-wall']
    if str(ctx.channel) in channels:
        with open('users.json', 'r') as f:
            users = json.load(f)
        sorted(users, key=lambda x : users[x].get('level', 0), reverse=True)
        high_score_list = sorted(users, key=lambda x : users[x].get('level', 0), reverse=True)
        message = ''
        for number, user in enumerate(high_score_list):
            message += '**{0}. <@{1}>  Level = {2}**\n\n'.format(number + 1, user, users[user].get('level', 0))
            if number+1 > 2:
                break 
        embed = discord.Embed(title='Rankings', description=f'{message}')
        embed.set_footer(text='gae | you')
        channel = guild.get_channel(769319830461349978)
        await ctx.message.delete()
        await channel.send(embed=embed)
        return



@bot.command()
@commands.has_role("Inn Server")
async def move(ctx, *, channel : discord.VoiceChannel = None):
    if channel is None:
        embed = discord.Embed(title='Usage', description='you must be in the same vc and then use .move newvcid or .move newvcname')
        await ctx.send(embed=embed)
        return
    else:
        await ctx.message.delete()
        guild = bot.get_guild(661211931558019072)
        author = ctx.message.author
        id1 = ctx.author.voice.channel
        for members in id1.members:
            await members.move_to(channel)
        await ctx.send('Done')


@bot.command()
@commands.has_role("Inn Keeper")
async def filter(ctx, *, badword=None):
    channels = ["🏛┃council"]
    if str(ctx.channel) in channels:
        await ctx.message.delete()
        if badword is None:
            await ctx.send('Please write the word you want to filter example comma and space is must , word')
            return
        elif ', ' not in badword:
            await ctx.send('Please write the word you want to filter example comma and space is must , word')
            return
        elif ', ' in badword:
            bad = str(badword)
            with open('bad-words.txt', 'a') as file:
                file.write(bad)
                file.close()
            await ctx.send('Word filtered')
        

@bot.command(aliases=['ufile'])
@commands.has_role("Inn Keeper")
async def datafile(ctx, *, name=None):
    channels = ["data"]
    if str(ctx.message.channel) in channels:
        if name is None:
            await ctx.send('Enter the file you want badwords or users')
        elif name == 'users':
            with open('users.json', 'r') as f:
                await ctx.send(file=File(fp=f, filename='users.json'))
        elif name == 'badwords':
            with open('bad-words.txt', 'r') as f:
                await ctx.send(file=File(fp=f, filename='bad-words.txt'))
        else:
            await ctx.send('Enter badwords or users')


        

@bot.command()
@commands.has_role("Inn Keeper")
async def addav(ctx, member: discord.Member = None, *,  bg=None):
    if bg is None:
        embed = discord.Embed(title='Usage', description='.addav @user urlofav\nurl must have .jpg or .png or .gif in the extension')
        await ctx.send(embed=embed)
        return
    elif ".png" in bg:
        if member is None:
            await ctx.message.author
        else:
            member == member
        with open('users.json', 'r') as f:
            users = json.load(f)
    
        await addbg(ctx, users, member, bg)

        with open('users.json', 'w') as f:
            json.dump(users, f)
    elif ".gif" in bg:
        if member is None:
            member = ctx.message.author
        else:
            member == member
        with open('users.json', 'r') as f:
            users = json.load(f)
    
        await addbg(ctx, users, member, bg)
    
        with open('users.json', 'w') as f:
            json.dump(users, f)
    else:
        await ctx.send("Add links that end with either .png for image or .gif for gif")
        return
async def addbg(ctx, users, member, bg):
        users[f'{member.id}']['bg'] = bg
        await ctx.send("New avatar added")


@bot.command(aliases=['rename'])
@commands.has_role("Inn Server")
async def nick(ctx, member: discord.Member = None, *, name=None):
    if member is None:
        await ctx.message.delete()
        embed = discord.Embed(title='Usage', description='.rename @user newname')
        await ctx.send(embed=embed)
        return
    elif name is None:
        await ctx.message.delete()
        await ctx.send("New nickname is required")
        return
    else:
        await ctx.message.delete()
        await member.edit(nick=name)
        return


@bot.command()
@commands.has_role("Inn Keeper")
async def event(ctx, user: discord.Member = None):
    channels = ["🗣┃event-wall"]
    if str(ctx.message.channel) in channels:
        await ctx.message.delete()
        embed = discord.Embed(colour=0x4B0082)
        embed.add_field(name="**Event**", value=f"React to :scroll: to get **Bard** role. "
                                                f"You will get notified whenever there is an event\n\n"
                                                f"So don\'t forget to react")
        message = await ctx.message.channel.send(embed=embed)
        await message.add_reaction("\U0001F4DC")
        emote = ['\U0001F4DC']
        while True:
            def check(reaction, user):
                return (reaction.message.id == message.id) and (user != bot.user) and (str(reaction) in emote)
            reaction, user = await bot.wait_for('reaction_add', check=check)
            if str(reaction) == '\U0001F4DC':
                role = discord.utils.get(user.guild.roles, name="Bard")
                await user.add_roles(role)
            def check(reaction, user):
                return (reaction.message.id == message.id) and (user != bot.user)
            reaction, user = await bot.wait_for('reaction_remove', check=check)
            role = discord.utils.get(user.guild.roles, name="Bard")
            await user.remove_roles(role)
            return


@bot.command()
@commands.has_role("Inn Server")
async def staff(ctx):
    channels = ["🏛┃council"]
    if str(ctx.channel) in channels:
        embed = discord.Embed(title="Staff Commands", description="Here are all the staff commands \n \n \n__**warn/w**__ = \"Warns user\"\n"
                                                                        "__**kick/k**__ = "
                                                                        "\"Kicks user\" \n __**mute/m**__ = \""
                                                                        "Mutes the user\" \n __**unmute/um**__ = \"Unmutes the user\" \n"
                                                                        "__**mods**__ = \"Shows all the moderation that happen to the user\"\n"
                                                                        "__**move**__ = \"Moves users from the vc you are in to another vc\"\n"
                                                                        "__**rename**__ = \"Changes user\'s nickname\"")
        await ctx.send(content=None, embed=embed)
        return


@bot.command()
@commands.has_role("Inn Keeper")
async def admin(ctx):
    channels = ["🏛┃council"]
    if str(ctx.channel) in channels:
        embed = discord.Embed(title="Admin Commands", description="Here are all the admin commands \n \n \n__**ban/b**__ = "
                                                                        "\"Bans user\" \n__**unban/ub**__ = \""
                                                                        "Unbans user\" \n__**serverban/sban**__ = \"Server ban means a non member gets ban for that you need their id\"\n"
                                                                        "__**transfer**__ =\"Gives user money\"\n"
                                                                        "__**take**__ =\"Takes user money\"\n"
                                                                        "__**filter**__ =\"Filters the word\"\n"
                                                                        "__**clear**__ = \"Deletes 100 recent messages this command should only be used after raids\"")
        await ctx.send(content=None, embed=embed)
        return


@bot.command(aliases=["purge"])
@commands.has_role("Inn Keeper")
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


@bot.command(aliases=["w"])
@commands.has_role('Inn Server')
async def warn(ctx, member: discord.Member = None, *, reason=None):
    guild = bot.get_guild(661211931558019072)
    if member is None:
        await ctx.message.delete()
        embed = discord.Embed(title='Usage', description='.w/.warn @user reason')
        await ctx.send(embed=embed)
        return
    elif member.bot:
        await ctx.message.delete()
        await ctx.send("Fool you can't warn the mighty one")
        return
    elif reason is None:
        await ctx.message.delete()
        await ctx.send("Reason Required")
        return
    else:
        member == member
        staff = discord.utils.get(member.guild.roles, name="Inn Server")
        if staff in member.roles:
            await ctx.message.delete()
            await ctx.send("You can't warn the staff member")
            return
        else:
            global warn
            warn = "({1}) warned ({0}) reason ({2})".format(member, ctx.message.author, reason)
            reason=reason
            embed = discord.Embed(title="Warn", description=f" You got a warning for **{reason}**\n \nServer: {guild.name}", colour=13882323)
            await member.send(content=None, embed=embed)
            await ctx.message.delete()
            guild = bot.get_guild(661211931558019072)
            channel = guild.get_channel(764169629165027348)
            em = discord.Embed(title="**__Warn__**", description=f"**Member:** {member}\n"
                                                        f"**Staff Member:** {ctx.message.author}\n"
                                                        f"**Reason:** {reason}")
            em.set_footer(text=f"{member.id}")
            await channel.send(embed=em)
            with open('users.json', 'r') as i:
                users = json.load(i)
                    
            warnings = users[f'{member.id}']['warnings'] 
            e = int(warnings)
            ea = (e+1)
            a = str(ea)
            users[f'{member.id}']['warnings'] = a

            with open('users.json', 'w') as i:
                json.dump(users, i)
    
            try:
                with open("stats.txt", "a") as f:
                    f.write(f"Time: {time.asctime( time.localtime(time.time()) )}, Warn: {warn}\n")
            except Exception as e:
                print(e)
            return


@bot.command(aliases=["k"])
@commands.has_role('Inn Server')
async def kick(ctx, member: discord.Member = None, *, reason=None):
    guild = bot.get_guild(661211931558019072)
    if member is None:
        await ctx.message.delete()
        embed = discord.Embed(title='Usage', description='.k/.kick @user reason')
        await ctx.send(embed=embed)
        return
    elif member.bot:
        await ctx.message.delete()
        await ctx.send("Fool you can't kick the mighty one")
        return
    elif reason is None:
        await ctx.message.delete()
        await ctx.send("Reason Required")
        return
    else:
        member == member
        staff = discord.utils.get(member.guild.roles, name="Inn Server")
        if staff in member.roles:
            await ctx.message.delete()
            await ctx.send("You can't kick the staff member")
            return
        else:
            embed = discord.Embed(title="Kicked", description=f" You got kicked  for **{reason}**\n \nServer: {guild.name}", colour=13882323)
            await member.send(content=None, embed=embed)
            await member.kick(reason=reason)
            await ctx.message.delete()
            guild = bot.get_guild(661211931558019072)
            channel = guild.get_channel(764169629165027348)
            em = discord.Embed(title="**__Kick__**", description=f"**Member:** {member}\n"
                                                        f"**Staff Member:** {ctx.message.author}\n"
                                                        f"**Reason:** {reason}")
            em.set_footer(text=f"{member.id}")
            await channel.send(embed=em)
            global kick
            kick = "({1}) kicked ({0}) reason ({2})".format(member, ctx.message.author, reason)
            with open('users.json', 'r') as i:
                users = json.load(i)
                    
            kicks = users[f'{member.id}']['kicks'] 
            e = int(kicks)
            ea = (e+1)
            a = str(ea)
            users[f'{member.id}']['kicks'] = a

            with open('users.json', 'w') as i:
                json.dump(users, i)
                
            try:
                with open("stats.txt", "a") as f:
                    f.write(f"Time: {time.asctime( time.localtime(time.time()) )}, Kick: {kick}\n")
            except Exception as e:
                print(e)
                return


@bot.command(aliases=["b"])
@commands.has_role('Inn Keeper')
async def ban(ctx, member: discord.Member = None, *, reason=None):
    guild = bot.get_guild(661211931558019072)
    if member is None:
        await ctx.message.delete()
        embed = discord.Embed(title='Usage', description='.b/.ban @user reason')
        await ctx.send(embed=embed)
        return
    elif member.bot:
        await ctx.message.delete()
        await ctx.send("Fool you can't ban the mighty one")
        return
    elif reason is None:
        await ctx.message.delete()
        await ctx.send("Reason Required")
        return
    else:
        embed = discord.Embed(title="Banned", description=f" You got banned for **{reason}** talk to @Azog The Defiler#5131 if you are serious or there was some misunderstanding\n \nServer: {guild.name}", colour=13882323)
        await member.send(content=None, embed=embed)
        await member.ban(reason=reason)
        await ctx.message.delete()
        guild = bot.get_guild(661211931558019072)
        channel = guild.get_channel(764169629165027348)
        em = discord.Embed(title="**__Ban__**", description=f"**Member:** {member}\n"
                                                            f"**Staff Member:** {ctx.message.author}\n"
                                                            f"**Reason:** {reason}")
        em.set_footer(text=f"{member.id}")
        await channel.send(embed=em)
        global ban
        ban = "({1}) banned ({0}) reason ({2})".format(member, ctx.message.author, reason)
        with open('users.json', 'r') as i:
            users = json.load(i)
                
        bans = users[f'{member.id}']['bans'] 
        e = int(bans)
        ea = (e+1)
        a = str(ea)
        users[f'{member.id}']['bans'] = a

        with open('users.json', 'w') as i:
            json.dump(users, i)
            
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {time.asctime( time.localtime(time.time()) )}, Ban: {ban}\n")
        except Exception as e:
            print(e)
            return


@bot.command(aliases=["sban"])
@commands.has_role('Inn Keeper')
async def serverban(ctx, id: int = None, *, reason=None):
    if id is None:
        await ctx.message.delete()
        embed = discord.Embed(title='Usage', description='.sban/serverban userid reason')
        await ctx.send(embed=embed)
        return
    elif id == "652067253080031233":
        await ctx.message.delete()
        await ctx.send("Fool you can't ban the mighty one")
        return
    elif reason is None:
        await ctx.message.delete()
        await ctx.send("Reason Required")
        return
    else:
        user = await bot.fetch_user(id)
        await ctx.message.delete()
        await ctx.guild.ban(user)
        guild = bot.get_guild(661211931558019072)
        channel = guild.get_channel(764169629165027348)
        em = discord.Embed(title="**__Server Ban__**", description=f"**User:** {user}\n"
                                                            f"**Staff Member:** {ctx.message.author}\n"
                                                            f"**Reason:** {reason}")
        em.set_footer(text=f"{user.id}")
        await channel.send(embed=em)
        global ban
        reason=reason
        sban = "({1}) server banned ({0}) reason ({2})".format(id, ctx.message.author, reason)
        with open('users.json', 'r') as i:
            users = json.load(i)
                
        bans = users[f'{member.id}']['bans'] 
        e = int(bans)
        ea = (e+1)
        a = str(ea)
        users[f'{member.id}']['bans'] = a

        with open('users.json', 'w') as i:
            json.dump(users, i)
            
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {time.asctime( time.localtime(time.time()) )}, SBan: {sban}\n")
        except Exception as e:
            print(e)
            return

            
@bot.command(aliases=["ub"])
@commands.has_role('Inn Keeper')
async def unban(ctx, id: int = None, *, reason=None):
    if id is None:
        await ctx.message.delete()
        embed = discord.Embed(title='Usage', description='.ub/.unban userid reason')
        await ctx.send(embed=embed)
        return
    elif id == "652067253080031233":
        await ctx.message.delete()
        await ctx.send("Fool you can't ban or unban the mighty one")
        return
    elif reason is None:
        await ctx.message.delete()
        await ctx.send("Reason Required")
        return
    else:
        user = await bot.fetch_user(id)
        await ctx.message.delete()
        await ctx.guild.unban(user)
        await ctx.send(f'Successfully Unbanned {user}')
        guild = bot.get_guild(661211931558019072)
        channel = guild.get_channel(764169629165027348)
        em = discord.Embed(title="**__Unban__**", description=f"**Member:** {user}\n"
                                                            f"**Staff Member:** {ctx.message.author}\n"
                                                            f"**Reason:** {reason}")
        em.set_footer(text=f"{user.id}")
        await channel.send(embed=em)
        global unban
        unban = "({1}) unbanned ({0}) reason ({2})".format(id, ctx.message.author, reason)
        print(f"Time: {time.asctime( time.localtime(time.time()) )}, Unban: {unban}\n")
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {time.asctime( time.localtime(time.time()) )}, Unban: {unban}\n")
        except Exception as e:
            print(e)
            return


@bot.command(aliases=["m"])
@commands.has_role('Inn Server')
async def mute(ctx, member: discord.Member = None, *, reason=None):
    guild = bot.get_guild(661211931558019072)
    if member is None:
        await ctx.message.delete()
        embed = discord.Embed(title='Usage', description='.m/.mute @user reason')
        await ctx.send(embed=embed)
        return
    elif member.bot:
        await ctx.message.delete()
        await ctx.send("Fool you can't mute the mighty one")
        return
    else:
        member == member
    staff = discord.utils.get(member.guild.roles, name="Inn Server")
    role = discord.utils.get(member.guild.roles, name="Muted")
    if role in member.roles:
        await ctx.message.delete()
        await ctx.send("User is already Muted")
        return
    elif staff in member.roles:
        await ctx.message.delete()
        await ctx.send("You can't mute the staff member")
        return
    else:
        await member.add_roles(role)
        await ctx.message.delete()
        await ctx.send("**{0}** was muted by **{1}**!".format(member, ctx.message.author))
        embed = discord.Embed(title="Muted", description=f" You got muted for **{reason}**\n \nServer: {guild.name}", colour=13882323)
        await member.send(content=None, embed=embed)
        guild = bot.get_guild(661211931558019072)
        channel = guild.get_channel(764169629165027348)
        em = discord.Embed(title="**__Mute__**", description=f"**Member:** {member}\n"
                                                            f"**Staff Member:** {ctx.message.author}\n"
                                                            f"**Reason:** {reason}")
        em.set_footer(text=f"{member.id}")
        await channel.send(embed=em)
        global mute
        mute = "({1}) muted ({0}) reason ({2})".format(member, ctx.message.author, reason)
        with open('users.json', 'r') as i:
            users = json.load(i)
                
        mutes = users[f'{member.id}']['mutes'] 
        e = int(mutes)
        ea = (e+1)
        a = str(ea)
        users[f'{member.id}']['mutes'] = a

        with open('users.json', 'w') as i:
            json.dump(users, i)
            
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {time.asctime( time.localtime(time.time()) )}, Mute: {mute}\n")
        except Exception as e:
            print(e)
            return


@bot.command(pass_context = True, aliases=["um"])
@commands.has_role('Inn Server')
async def unmute(ctx, member: discord.Member = None, *, reason=None):
    guild = bot.get_guild(661211931558019072)
    if member is None:
        await ctx.message.delete()
        embed = discord.Embed(title='Usage', description='.um/.unmute @user reason')
        await ctx.send(embed=embed)
        return
    elif member.bot:
        await ctx.message.delete()
        await ctx.send("The mighty one can't be muted or unmuted")
        return
    else:
        role = discord.utils.get(member.guild.roles, name="Muted")
        if role not in member.roles:
            await ctx.message.delete()
            await ctx.send("User is not muted")
            return
        else:
            await member.remove_roles(role)
            await ctx.message.delete()
            await ctx.send("**{0}** was unmuted by **{1}**!".format(member, ctx.message.author))
            embed = discord.Embed(title="Unmuted", description=f" You are now unmuted\n \nServer: {guild.name}", colour=13882323)
            await member.send(content=None, embed=embed)
            guild = bot.get_guild(661211931558019072)
            channel = guild.get_channel(764169629165027348)
            em = discord.Embed(title="**__Unmute__**", description=f"**Member:** {member}\n"
                                                                    f"**Staff Member:** {ctx.message.author}\n"
                                                                    f"**Reason:** {reason}")
            em.set_footer(text=f"{member.id}")
            await channel.send(embed=em)
            global unmute
            unmute = "({1}) unmuted ({0}) reason ({2})".format(member, ctx.message.author, reason)
            print(f"Time: {time.asctime( time.localtime(time.time()) )}, Unmute: {unmute}\n")
            try:
                with open("stats.txt", "a") as f:
                    f.write(f"Time: {time.asctime( time.localtime(time.time()) )}, Unmute: {unmute}\n")
            except Exception as e:
                print(e)
                return


@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)

    role = discord.utils.get(member.guild.roles, name="Wanderer")
    guild = bot.get_guild(661211931558019072)
    channels = guild.get_channel(661211931558019075)
    ch = guild.get_channel(773803053047873557)
    await member.add_roles(role)
    N = 1920
    n = 1080
    size_image = width_image, height_image = N, n
    img = Image.open(f'./image.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(f'./Font.ttf', 100)
    color = (0, 0, 0)
    text = f'{member}'
    width_text, height_text = draw.textsize(text, font)
    offset_x, offset_y = font.getoffset(text)
    width_text += offset_x
    height_text += offset_y
    top_left_x = width_image / 2 - width_text / 2
    top_left_y = height_image / 1 - height_text / 1.2
    xy = top_left_x, top_left_y
    draw.text(xy, text, font=font, fill=color)
    img.save(f'./images.jpg')
    myfile = discord.File(f'./images.jpg')
    await channels.send(f"""Welcome to the **{guild.name}** {member.mention} and don't forget to read the rules {ch.mention} """ ,file=myfile)
    guild = bot.get_guild(661211931558019072)
    channel = guild.get_channel(767016027015610389)
    embed = discord.Embed(title='Joined', description=f'{member.mention} has joined the server')
    if member.is_avatar_animated():
        avt = f"{member.avatar_url_as(format='gif')}"
    else:
        avt = f"{member.avatar_url_as(format='png')}"
    embed.set_thumbnail(url=f'{avt}')
    embed.set_footer(text=f'{member.id}')
    await channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    guild = bot.get_guild(661211931558019072)
    channel = guild.get_channel(767016027015610389)
    embed = discord.Embed(title='Left', description=f'{member.mention} has left the server')
    if member.is_avatar_animated():
        avt = f"{member.avatar_url_as(format='gif')}"
    else:
        avt = f"{member.avatar_url_as(format='png')}"
    embed.set_thumbnail(url=f'{avt}')
    embed.set_footer(text=f'{member.id}')
    await channel.send(embed=embed)


                                        #MEMBER COMMANDS


@bot.command()
async def suggest(ctx):
    guild = bot.get_guild(661211931558019072)                                               
    channel = guild.get_channel(767481506444345394)
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
        member = ctx.author
        await ctx.send('Please write the suggestion')
        try:
            suggestion = await bot.wait_for('message', timeout=120.0, check=lambda message: message.author == member)
            em = discord.Embed(title=f'Suggested by {member}', description=f'\n{suggestion.content}')
            if member.is_avatar_animated():                                          
                avt = f"{member.avatar_url_as(format='gif')}"                   
            else:                                          
                avt = f"{member.avatar_url_as(format='png')}"             
            em.set_thumbnail(url=f'{avt}')                                                     
            em.set_footer(text=f'{member.id}')                                                   
            await channel.send(embed=em)
            await ctx.send('Done')
        except asyncio.TimeoutError:
            await ctx.send('Timeout try again')


@bot.command()
async def help(ctx):
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
        embed = discord.Embed(title="Bot Commands", description="Here are all the bot commands" , colour=0x101010)
        embed.add_field(name='General Commands', value='`.coins`  `.daily`  `.kiss`  `.hug`  `.fist`  `.slap`')       
        embed.add_field(name='User Commands', value='`.profile`  `.editinfo`  `.userinfo`  `.pfp`  `.give`  `.roles`  `.buyrole`')
        embed.add_field(name='Server Commands', value='`.ping`  `.serverinfo`  `.suggest`')
        embed.add_field(name='Weeb/Nerd Commands', value='`.mal`  `.anime`  `.manga`  `.character`  `.seasonal`  `.upcominganimes`  `.movie`  `.series`  `.trending`')
        embed.add_field(name='Fun/Recreation Commands', value='`.cup`  `.toss`  `.dice`  `.bj`  `.war`')
        await ctx.send(content=None, embed=embed)
        return

@bot.command(aliases=["uinfo"])
async def userinfo(ctx, *, user: discord.Member = None):
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
        if not user:
            user = ctx.author

        embed = discord.Embed(
        title=f"{user.name}'s Stats and Information."
        )
        embed.set_footer(text=f"ID: {user.id}")
        embed.set_thumbnail(url=user.avatar_url_as(format="png"))
        embed.add_field(name="__**General information:**__", value=f"**Discord Name:** {user}\n"
                                                                   f"**Account created:** {user.created_at.__format__('%A %d %B %Y at %H:%M')}\n")
        embed.add_field(name="__**Server-related information:**__", value=f"**Nickname:** {user.nick}\n"
                                                                          f"**Joined server:** {user.joined_at.__format__('%A %d %B %Y at %H:%M')}\n"
                                                                          f"**Roles:** {' '.join([r.mention for r in user.roles[1:]])}")
        return await ctx.send(embed=embed)


@bot.command()
async def pfp(ctx, *, user: discord.Member = None):
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
        if not user:
            user = ctx.author

        embed = discord.Embed(
            colour=discord.Color.gold(),
        )
        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
        if user.is_avatar_animated():
            embed.set_image(url=f"{user.avatar_url_as(size=1024, format='gif')}")
        else:
            embed.set_image(url=f"{user.avatar_url_as(size=1024, format='png')}")
        return await ctx.send(embed=embed)


@bot.command()
async def profile(ctx, member: discord.Member = None):
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
        if member is not None:
            id = member.id
            member = member.mention
            if str(id) == "652067253080031233":
                await ctx.send("I have no profile young one")
                return
            else:
                with open('users.json', 'r') as f:
                    users = json.load(f)
                level = users[str(id)]['level']
                guild = ctx.guild
                member = guild.get_member(id)
                user = member
                mem_join = member.joined_at
                now = datetime.datetime.now()
                join_days = (now - mem_join).days
                with open('users.json', 'r') as d:
                    users = json.load(d)
                if not f'{member.id}' in users:
                    info = None
                    bg = "https://i.imgur.com/DY2CKvu.png"
                    coins = 0
                else:
                    info = users[str(id)]['info']
                    bg = users[str(id)]['bg']
                    coins = users[str(id)]['coins']
                    if user.is_avatar_animated():
                        embed = discord.Embed()
                        embed.set_image(url=f"{bg}")
                        embed.set_footer(text=f"{user.id}")
                        embed.add_field(name="__**Profile:**__", value=f"**Discord Name:** {user}\n"
                                                                        f"**Nickname:** {user.nick}\n"
                                                                        f"**Member Since:** {join_days} Days\n"
                                                                        f"**Level:** {level}\n"
                                                                        f"**Coins:** {coins} :coin:\n\n\n"
                                                                        f"**Info:** {info}\n\n")
                        await ctx.send(embed=embed)
                        return
                    else:
                        embed = discord.Embed()
                        embed.set_image(url=f"{bg}")
                        embed.set_footer(text=f"{user.id}")
                        embed.add_field(name="__**Profile:**__", value=f"**Discord Name:** {user}\n"
                                                                        f"**Nickname:** {user.nick}\n"
                                                                        f"**Member Since:** {join_days} Days\n"
                                                                        f"**Level:** {level}\n"
                                                                        f"**Coins:** {coins} :coin:\n\n\n"
                                                                        f"**Info:** {info}\n\n")
                        await ctx.send(embed=embed)
                        return
        else:
            member = ctx.message.author
            id = ctx.message.author.id
            with open('users.json', 'r') as f:
                users = json.load(f)
            level = users[str(id)]['level']
            guild = ctx.guild
            member = guild.get_member(id)
            user = member
            mem_join = member.joined_at
            now = datetime.datetime.now()
            join_days = (now - mem_join).days
            with open('users.json', 'r') as d:
                users = json.load(d)
            if not f'{member.id}' in users:
                info = None
                bg = "https://i.imgur.com/DY2CKvu.png"
                coins = 0
            else:
                info = users[str(id)]['info']
                bg = users[str(id)]['bg']
                coins = users[str(id)]['coins']
                if user.is_avatar_animated():
                    embed = discord.Embed()
                    embed.set_image(url=f"{bg}")
                    embed.set_footer(text=f"{user.id}")
                    embed.add_field(name="__**Profile:**__", value=f"**Discord Name:** {user}\n"
                                                                    f"**Nickname:** {user.nick}\n"
                                                                    f"**Member Since:** {join_days} Days\n"
                                                                    f"**Level:** {level}\n"
                                                                    f"**Coins:** {coins} :coin:\n\n\n"
                                                                    f"**Info:** {info}\n\n")
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = discord.Embed()
                    embed.set_image(url=f"{bg}")
                    embed.set_footer(text=f"{user.id}")
                    embed.add_field(name="__**Profile:**__", value=f"**Discord Name:** {user}\n"
                                                                    f"**Nickname:** {user.nick}\n"
                                                                    f"**Member Since:** {join_days} Days\n"
                                                                    f"**Level:** {level}\n"
                                                                    f"**Coins:** {coins} :coin:\n\n\n"
                                                                    f"**Info:** {info}\n\n")
                await ctx.send(embed=embed)
                return

@bot.command()
async def editinfo(ctx, *, info = None):
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
        if info is None:
            embed = discord.Embed(title='Usage', description='.editinfo info')
            await ctx.send(embed=embed)
            return
        else:
            user = discord.Member
            user = ctx.message.author
            member = user
            info = str(f'{info}')
            with open('users.json', 'r') as d:
                users = json.load(d)

            await userdata(users, ctx.message.author, info)
            await edit(users, ctx.message.author, info)

            with open('users.json', 'w') as d:
                json.dump(users, d)
async def userdata(users, user, info):
    guild = bot.get_guild(661211931558019072)
    channel = guild.get_channel(686918214327861266)
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['info'] = info
        await channel.send('Edited')

async def edit(users, user, info):
    guild = bot.get_guild(661211931558019072)
    channel = guild.get_channel(686918214327861266)
    if f'{user.id}' in users:
        users[f'{user.id}']['info'] = info
        await channel.send('Edited')
    else:
        return
                                 

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')
    return


@bot.command(aliases=["sinfo"])
async def serverinfo(ctx):
    guild = bot.get_guild(661211931558019072)
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
        embed = discord.Embed(title="Server Information", colour=12632256)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name="**Server Name:**", value=f"{guild.name}", inline=False)
        embed.add_field(name="**Server Owner**", value=f"{guild.owner}", inline=False)
        embed.add_field(name="**Server Created:**", value=f"{guild.created_at.__format__('%d-%m-%Y %H:%M:%S')}", inline=False)
        embed.add_field(name="**Member Count:**", value=f"{guild.member_count}")
    await ctx.send(embed=embed)
    return


@bot.command(aliases=['currency'])
async def coins(ctx, member:discord.Member = None):
    guild = bot.get_guild(661211931558019072)
    channels = ["🤖┃machinery", "♠┃gambling"]
    if str(ctx.channel) in channels:
        if member is None:
            member = ctx.message.author
        else:
            member = member
        with open('users.json', 'r') as f:
            users = json.load(f)
        coins = users[f'{member.id}']['coins']
        ee = discord.Embed(description=f"{member.mention} has {coins} :coin:")
        await ctx.send(embed=ee)

    
@bot.command(aliases=['daily'])
@commands.cooldown(1, 86400, type=commands.BucketType.user)
async def taskdone(ctx):
    guild = bot.get_guild(661211931558019072)
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
        member = ctx.message.author
        with open('users.json', 'r') as f:
            users = json.load(f)

        await addcoins(ctx, member, users)
        
        with open('users.json', 'w') as f:
            json.dump(users, f)

async def addcoins(ctx, member, users):
            users[f'{member.id}']['coins'] += 1000
            await ctx.send(f"{member.mention} you have earned 1000 :coin:")


@taskdone.error
async def taskdone_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        c = '{:.0f}'.format(error.retry_after)
        a = int(f'{c}')
        b = int(a/3600)
        d = int(a/60)
        if b == 1:
            msg = f'Please try again after 2 hours'
            await ctx.send(msg)
        elif b == 0:
            msg = f'Please try again after {d} minutes'
            await ctx.send(msg)
        elif d == 1:
            msg = f'Please try again after 2 minutes'
            await ctx.send(msg)
        elif d == 0:
            msg = f'Please try again after {c} seconds'
            await ctx.send(msg)
        else:
            msg = f'Please try again after {b} hours'
            await ctx.send(msg)
    else:
        raise error


@bot.command()
async def buyrole(ctx, *, role = None):
    guild = bot.get_guild(661211931558019072)
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
        member = ctx.message.author
        if role is not None:
            if "Survivor" in role:
                role = discord.utils.get(member.guild.roles, name="Survivor")
                with open('users.json', 'r') as f:
                    users = json.load(f)

                coins = users[f'{member.id}']['coins']
                if coins >= 2000:

                    users[f'{member.id}']['coins'] -= 2000
            
                    with open('users.json', 'w') as f:
                        json.dump(users, f)

                    await member.add_roles(role)
                    await ctx.send(f"{member.mention} you have bought {role}")
                else:
                    await ctx.send(f"You don't have enough coins to buy this role")
            elif "Plunderer" in role:
                role = discord.utils.get(member.guild.roles, name="Plunderer")
                with open('users.json', 'r') as f:
                    users = json.load(f)
        
                coins = users[f'{member.id}']['coins']
                if coins >= 2000:
        
                    users[f'{member.id}']['coins'] -= 2000
        
                    with open('users.json', 'w') as f:
                        json.dump(users, f)
        
                    await member.add_roles(role)
                    await ctx.send(f"{member.mention} you have bought {role}")
                else:
                    await ctx.send(f"You don't have enough coins to buy this role")
            elif "Pirate" in role:
                role = discord.utils.get(member.guild.roles, name="Pirate")
                with open('users.json', 'r') as f:
                    users = json.load(f)
            
                coins = users[f'{member.id}']['coins']
                if coins >= 365000:
            
                    users[f'{member.id}']['coins'] -= 365000
            
                    with open('users.json', 'w') as f:
                        json.dump(users, f)
            
                    await member.add_roles(role)
                    await ctx.send(f"{member.mention} you have bought {role}")
                else:
                    await ctx.send(f"You don't have enough coins to buy this role")
            else:
                await ctx.send("Wrong role try .roles and remember first letter must be uppercased like \"Survivor\"")
        else:
            embed = discord.Embed(title='Usage', description='.buyrole Rolename\nTo get role names use .roles')
            await ctx.send(embed=embed)
            return


            
@bot.command()
async def roles(ctx):
    embed = discord.Embed()
    embed.add_field(name="20000 :coin:  Roles\n\n", value="**Survivor**\n"
                                                        "**Plunderer**\n")
    embed.add_field(name="365000 :coin: Best Buyable Roles\n\n\n", value="**Pirate**\n")
    await ctx.send(embed=embed)



@bot.command()
async def give(ctx, member: discord.Member = None, *, coin=0):
    guild = bot.get_guild(661211931558019072)
    channels = ["🤖┃machinery"]
    user = ctx.message.author
    with open('users.json', 'r') as f:
        users = json.load(f)
    coins = users[f'{user.id}']['coins']
    q = int(coins)
    l = int(coin)
    if str(ctx.channel) in channels:
        if member is None:
            embed = discord.Embed(title='Usage', description='.give @name amount')
            await ctx.send(embed=embed)
            return
        elif q < l:
            await ctx.send("Not enough coins")
        elif l == 0:
            await ctx.send("Specify the amount of coins you want to give")
        else:
            with open('users.json', 'r') as f:
                users = json.load(f)
            coins = users[f'{user.id}']['coins']
            a = int(coins)
            c = a-l
            users[f'{user.id}']['coins'] = c

            with open('users.json', 'w') as f:
                json.dump(users, f)

            with open('users.json', 'r') as f:
                users = json.load(f)
            coins = users[f'{member.id}']['coins']
            a = int(coins)
            c = a+l
            users[f'{member.id}']['coins'] = c

            with open('users.json', 'w') as f:
                json.dump(users, f)
                
            embed = discord.Embed(description=f'You gave {coin} :coin: to {member.mention}')
            await ctx.send(embed=embed)


@bot.command()
@commands.cooldown(1, 30, type=commands.BucketType.user)
async def kiss(ctx, member: discord.Member = None):
    if member is None:
        embed = discord.Embed(title='Usage', description='.kiss @user')
        await ctx.send(embed=embed)
        return
    else:
        r = ['https://i.imgur.com/ZSVDZwi.gif', 'https://i.imgur.com/50KEH5I.gif', 'https://i.imgur.com/c7tCHMx.gif', 'https://i.imgur.com/pur4RBr.gif', 'https://i.imgur.com/3p77k2o.gif']
        d = random.choice(r)
        embed = discord.Embed(description=f'{ctx.message.author.mention} gave kiss to {member.mention}', colour=0x000001)
        embed.set_image(url=f'{d}')
        await ctx.send(embed=embed)
        
        
@kiss.error
async def kiss_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        c = '{:.0f}'.format(error.retry_after)        
        await ctx.send(f'Please try again after {c} seconds')
        

@bot.command()
@commands.cooldown(1, 30, type=commands.BucketType.user)
async def fist(ctx, member: discord.Member = None):
    if member is None:
        embed = discord.Embed(title='Usage', description='.fist @user')
        await ctx.send(embed=embed)
        return
    else:
        r = ['https://i.imgur.com/WGx1oAd.gif', 'https://i.imgur.com/s2lHMUS.gif', 'https://i.imgur.com/mZhkabt.gif', 'https://i.imgur.com/yNynHm8.gif', 'https://i.imgur.com/W47N0qp.gif']
        d = random.choice(r)
        embed = discord.Embed(description=f'{ctx.message.author.mention} fist bumped with {member.mention}', colour=0x000001)
        embed.set_image(url=f'{d}')
        await ctx.send(embed=embed)
        

@fist.error
async def fist_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        c = '{:.0f}'.format(error.retry_after)        
        await ctx.send(f'Please try again after {c} seconds')

        
@bot.command()
@commands.cooldown(1, 30, type=commands.BucketType.user)
async def hug(ctx, member: discord.Member = None):
    if member is None:
        embed = discord.Embed(title='Usage', description='.hug @user')
        await ctx.send(embed=embed)
        return
    else:
        r = ['https://i.imgur.com/tmH9kAa.gif', 'https://i.imgur.com/h0npvMN.gif', 'https://i.imgur.com/KdlCRFZ.gif', 'https://i.imgur.com/VqXqqbW.gif', 'https://i.imgur.com/wanveQs.gif']
        d = random.choice(r)
        embed = discord.Embed(description=f'{ctx.message.author.mention} hugged {member.mention}', colour=0x000001)
        embed.set_image(url=f'{d}')
        await ctx.send(embed=embed)        
        
        
@hug.error
async def hug_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        c = '{:.0f}'.format(error.retry_after)        
        await ctx.send(f'Please try again after {c} seconds')


@bot.command()
@commands.cooldown(1, 30, type=commands.BucketType.user)
async def slap(ctx, member: discord.Member = None):
    if member is None:
        embed = discord.Embed(title='Usage', description='.slap @user')
        await ctx.send(embed=embed)
        return
    else:
        r = ['https://i.imgur.com/vU5CPxB.gif', 'https://i.imgur.com/MMGztMD.gif', 'https://i.imgur.com/J3exWoi.gif', 'https://i.imgur.com/c0ImF3g.gif', 'https://i.imgur.com/XSU83EU.gif']
        d = random.choice(r)
        embed = discord.Embed(description=f'{ctx.message.author.mention} slapped {member.mention}', colour=0x000001)
        embed.set_image(url=f'{d}')
        await ctx.send(embed=embed)                


@slap.error
async def slap_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        c = '{:.0f}'.format(error.retry_after)
        await ctx.send(f'Please try again after {c} seconds')
        

                                          #ANIME & MANGA


@bot.command()
@commands.cooldown(1, 300, type=commands.BucketType.channel)
async def manime(ctx, *, anim=None):
    guild = bot.get_guild(661211931558019072)
    channels = ["🏮┃anime-manga-chat"]
    if str(ctx.channel) in channels:
        if anim is None:
            embed = discord.Embed(title='Usage', description='.manime name')
            await ctx.send(embed=embed)
            return
        else:
            search = AnimeSearch(anim)
            a = f'{search.results[0].mal_id}'
            b = Anime(a)
            c = f'{search.results[0].image_url}'
            d = f'{search.results[0].score}'
            query = f'{search.results[0].title}'
            re = f'{b.related_anime}'
            if re is None:
                ream = None
            else:
                ream = f'{b.related_anime}'
            client = kitsu.Client()
            def kanime(ctx, query):
                client = kitsu.Client()
            entries = await client.search('anime', query, limit=1)
            if not entries:
                print(f'No entries found for "{query}"')
                return
            for i, anime in enumerate(entries, 1):
                embed=discord.Embed()   
                embed.set_thumbnail(url=f'{c}')
                embed.add_field(name=f'{anime.title}', value=f'{anime.synopsis}'[:1000])
                embed.add_field(name=':star: **Score\n**', value=f'{d}'[:1000])
                embed.add_field(name=':tv: **Type\n**', value=f'{b.type}'[:1000])
                embed.add_field(name=':cd: **Genre\n**', value=f'{b.genres}'[:1000])
                embed.add_field(name=':computer: **Total Episodes\n**', value=f'{b.episodes}'[:1000])
                embed.add_field(name=':inbox_tray: **Status\n**', value=f'{b.status}'[:1000])
                embed.add_field(name=':satellite: **Related Animes\n**', value=f'{ream}'[:500])
                embed.add_field(name=':musical_note: **Openings\n**', value=f'{b.opening_themes}'[:200])
                embed.add_field(name=':musical_note: **Endings\n**', value=f'{b.ending_themes}'[:200])
                embed.add_field(name=':paperclip: **Link\n**', value=f'[MyAnimeList]({b.url})'[:1000])
            await ctx.send(embed=embed)
            return

            
@manime.error
async def anime_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        c = '{:.0f}'.format(error.retry_after)            
        await ctx.send(f'Please try again after {c} seconds')
        
        
@bot.command()
@commands.cooldown(1, 300, type=commands.BucketType.channel)
async def manimeid(ctx, *, anim=None):
    guild = bot.get_guild(661211931558019072)
    channels = ["🏮┃anime-manga-chat"]
    if str(ctx.channel) in channels:
        if anim is None:
            await ctx.send('Use anime mal id like 1 for Cowboy Bebop')
        else:
            b = Anime(anim)
            a = f'{b.title}'
            search = AnimeSearch(a)
            c = f'{search.results[0].image_url}'
            d = f'{search.results[0].score}'
            query = f'{search.results[0].title}'
            re = f'{b.related_anime}'
            if re is None:                                                        
                ream = None
            else:
                ream = f'{b.related_anime}'
            client = kitsu.Client()
            def kanime(ctx, query):
                client = kitsu.Client()
            entries = await client.search('anime', query, limit=1)
            if not entries:
                print(f'No entries found for "{query}"')
                return
            for i, anime in enumerate(entries, 1):
                embed=discord.Embed()   
                embed.set_thumbnail(url=f'{c}')
                embed.add_field(name=f'{anime.title}', value=f'{anime.synopsis}'[:1000])
                embed.add_field(name=':star: **Score\n**', value=f'{d}'[:1000])
                embed.add_field(name=':tv: **Type\n**', value=f'{b.type}'[:1000])
                embed.add_field(name=':cd: **Genre\n**', value=f'{b.genres}'[:1000])
                embed.add_field(name=':computer: **Total Episodes\n**', value=f'{b.episodes}'[:1000])
                embed.add_field(name=':inbox_tray: **Status\n**', value=f'{b.status}'[:1000])
                embed.add_field(name=':satellite: **Related Animes\n**', value=f'{ream}'[:500])
                embed.add_field(name=':musical_note: **Openings\n**', value=f'{b.opening_themes}'[:200])
                embed.add_field(name=':musical_note: **Endings\n**', value=f'{b.ending_themes}'[:200])
                embed.add_field(name=':paperclip: **Link\n**', value=f'[MyAnimeList]({b.url})'[:1000])
            await ctx.send(embed=embed)
            return

            
@manimeid.error
async def animeid_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        c = '{:.0f}'.format(error.retry_after)            
        await ctx.send(f'Please try again after {c} seconds')
 
        
@bot.command()
@commands.cooldown(1, 300, type=commands.BucketType.channel)
async def manimeost(ctx, *, anim=None):
    member = ctx.message.author
    guild = bot.get_guild(661211931558019072)
    channels = ["🏮┃anime-manga-chat"]
    if str(ctx.channel) in channels:
        if anim is None:
            embed = discord.Embed(title='Usage', description='.manimeost name')
            await ctx.send(embed=embed)
            return
        else:
            search = AnimeSearch(anim)        
            a = f'{search.results[0].mal_id}'
            b = Anime(a)
            await member.send(f':musical_note: **Openings\n\n** {b.opening_themes}'[:1000])
            await member.send(f':musical_note: **Endings\n\n** {b.ending_themes}'[:1000])
            return
            
@manimeost.error
async def animeost_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        c = '{:.0f}'.format(error.retry_after)            
        await ctx.send(f'Please try again after {c} seconds')            
            


@bot.command()
async def anime(ctx, *, query=None):
    guild = bot.get_guild(661211931558019072)
    channels = ["🏮┃anime-manga-chat", "👍┃anime-manga-recommendations"]
    member = ctx.message.author
    if str(ctx.channel) in channels:
        if query is None:
            embed = discord.Embed(title='Usage', description='.anime name')
            await ctx.send(embed=embed)
            return
        client = kitsu.Client()
        entries = await client.search('anime', query, limit=10)
        if not entries:
            await ctx.send(f'No entries found for "{query}"')
            return
        message = await ctx.send('Searching...')
        for i, anime in enumerate(entries, 1):
            jikan = Jikan()
            b = jikan.search('anime', f'{anime.title}')
            mid = b['results'][0]
            malid = mid['mal_id']
            rate = mid['score']
            if anime.next_release is None:
                z = None
            else:
                z = f'{anime.next_release.strftime("%d-%m-%Y")}'
            if anime.started_at is None:
                y = None
            else:
                y = f'{anime.started_at.strftime("%d-%m-%Y")}'
            if anime.ended_at is None:
                x = None
            else:
                x = f'{anime.ended_at.strftime("%d-%m-%Y")}'
            embed=discord.Embed()
            embed.set_thumbnail(url=f'{anime.poster_image_url}')
            embed.add_field(name=f'{anime.title}', value=f'{anime.synopsis}'[:1000])
            embed.add_field(name=':star: **Rating\n**', value=f'{rate}'[:1000])
            embed.add_field(name=':tv: **Type\n**', value=f'{anime.subtype}'[:1000])
            embed.add_field(name=':computer: **Total Episodes\n**', value=f'{anime.episode_count}'[:1000])
            embed.add_field(name=':play_pause:  **Episode Length\n**', value=f'{anime.episode_length} minutes'[:1000])
            embed.add_field(name=':track_next: **Next Episode\n**', value=f'{z}'[:1000])
            embed.add_field(name=':inbox_tray: **Status\n**', value=f'{anime.status}'[:1000])
            embed.add_field(name=':calendar_spiral: **Aired\n**', value=f'From {y} to {x}'[:1000])
            streaming_links = await client.fetch_anime_streaming_links(anime)
            if streaming_links:
                for link in streaming_links:
                    if "http://www.hulu.com/" in link.url:
                        embed.add_field(name=':paperclip: **Hulu\n**', value=f'[Hulu]({link.url})')
                    elif "http://www.crunchyroll.com/" in link.url:
                        embed.add_field(name=':paperclip: **Crunchyroll\n**', value=f'[Crunchyroll]({link.url})')
                    elif "https://www.netflix.com/" in link.url:
                        embed.add_field(name=':paperclip: **Netflix\n**', value=f'[Netflix]({link.url})')
                    elif "https://vrv.co/" in link.url:
                        embed.add_field(name=':paperclip: **VRV\n**', value=f'[VRV]({link.url})')
                    elif "https://www.animelab.com/" in link.url:
                        embed.add_field(name=':paperclip: **AnimeLab\n**', value=f'[AnimeLab]({link.url})')
            embed.add_field(name=':paperclip: **Kitsu\n**', value=f'[Kitsu]({anime.url})'[:1000])
            embed.add_field(name=':paperclip: **MyAnimeList\n**', value=f'[MyAnimeList](http://myanimelist.net/anime/{malid})'[:1000])
            await message.edit(embed=embed)
            await message.add_reaction(u"\u27A1")
            await message.add_reaction(u"\u274C")
            emote = [u"\u27A1", u"\u274C"]
            try:
                def check(reaction, user):
                    return (reaction.message.id == message.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                if str(reaction) == u"\u27A1":
                    await message.remove_reaction(u"\u27A1", user)
                    continue
                elif str(reaction) == u"\u274C":
                    await message.delete()
                    return
            except asyncio.TimeoutError:
                user = bot.user
                await message.remove_reaction(u"\u27A1", user)
                await message.remove_reaction(u"\u274C", user)
                break
                
        await message.remove_reaction(u"\u27A1", user)         
        await message.remove_reaction(u"\u274C", user)
        await asyncio.sleep(60)
        chan = ["🏮┃anime-manga-chat"]
        if str(ctx.channel) in chan:
            await message.delete()
        elif str(ctx.channel) == "👍┃anime-manga-recommendations":
            return
        
        



@bot.command()
@commands.cooldown(1, 300, type=commands.BucketType.channel)
async def mmanga(ctx, *, manga=None):
    guild = bot.get_guild(661211931558019072)
    channels = ["🏮┃anime-manga-chat"]
    if str(ctx.channel) in channels:
        if manga is None:
            embed = discord.Embed(title='Usage', description='.mmanga name')
            await ctx.send(embed=embed)
            return
        else:
            search = MangaSearch(manga)
            a = f'{search.results[0].mal_id}'
            manga = Manga(a)
            re = f'{manga.related_manga}'
            if re is None:
                rema = None
            else:
                rema = f'{manga.related_manga}'
            embed = discord.Embed(title=f'{search.results[0].title}', description=f'{search.results[0].synopsis}'[:1000])
            embed.set_thumbnail(url=f'{search.results[0].image_url}')
            embed.add_field(name=':pencil: **Authors\n**', value=f' {manga.authors}'[:1000])
            embed.add_field(name=':star: **Score\n**', value=f' {search.results[0].score}'[:1000])
            embed.add_field(name=':page_facing_up: **Type\n**', value=f' {manga.type}'[:1000])
            embed.add_field(name=':label: **Genre\n**', value=f' {manga.genres}'[:1000])
            embed.add_field(name=':file_folder: **Volumes\n**', value=f' {manga.volumes}'[:1000])
            embed.add_field(name=':dividers: **Total Chapters\n**', value=f' {manga.chapters}'[:1000])
            embed.add_field(name=':inbox_tray: **Status\n**', value=f' {manga.status}'[:1000])
            embed.add_field(name=':ledger: **Related Mangas\n**', value=f' {rema}'[:500])
            embed.add_field(name=':paperclip: **Link\n**', value=f' [MyAnimeList]({manga.url})'[:1000])
            await ctx.send(embed=embed)

            
@mmanga.error
async def manga_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        c = '{:.0f}'.format(error.retry_after)            
        await ctx.send(f'Please try again after {c} seconds')
            

@bot.command()
async def manga(ctx, *, query=None):
    guild = bot.get_guild(661211931558019072)
    channels = ["🏮┃anime-manga-chat", "👍┃anime-manga-recommendations"]
    member = ctx.message.author
    if str(ctx.channel) in channels:
        if query is None:
            embed = discord.Embed(title='Usage', description='.manga name')
            await ctx.send(embed=embed)
            return
        client = kitsu.Client()
        entries = await client.search('manga', query, limit=10)
        if not entries:
            await ctx.send(f'No entries found for "{query}"')
            return
        message = await ctx.send('Searching...')
        for i, manga in enumerate(entries, 1):
            jikan = Jikan()
            b = jikan.search('manga', f'{manga.title}')
            mid = b['results'][0]
            malid = mid['url']
            rate = mid['score']
            if manga.started_at is None:
                y = None
            else:
                y = f'{manga.started_at.strftime("%d-%m-%Y")}'
            if manga.ended_at is None:
                x = None
            else:
                x = f'{manga.ended_at.strftime("%d-%m-%Y")}'
            embed=discord.Embed()
            embed.add_field(name=f'{manga.title}', value=f'{manga.synopsis}'[:1000])
            embed.add_field(name=':star: **Rating\n**', value=f'{rate}'[:1000])
            embed.set_thumbnail(url=f'{manga.poster_image_url}')
            embed.add_field(name=':page_facing_up: **Type\n**', value=f'{manga.subtype}'[:1000])
            embed.add_field(name=':file_folder: **Volumes\n**', value=f'{manga.volume_count}'[:1000])
            embed.add_field(name=':dividers: **Total Chapters\n**', value=f'{manga.chapter_count}'[:1000])
            embed.add_field(name=':inbox_tray: **Status\n**', value=f'{manga.status}'[:1000])
            embed.add_field(name=':calendar_spiral: **Aired\n**', value=f'From {y} to {x}'[:1000])
            embed.add_field(name=':paperclip: **Kitsu\n**', value=f'[Kitsu]({manga.url})'[:1000])
            embed.add_field(name=':paperclip: **MyAnimeList\n**', value=f'[MyAnimeList]({malid})'[:1000])
            await message.edit(embed=embed)
            await message.add_reaction(u"\u27A1")
            await message.add_reaction(u"\u274C")
            emote = [u"\u27A1", u"\u274C"]
            try:
                def check(reaction, user):
                    return (reaction.message.id == message.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                if str(reaction) == u"\u27A1":
                    await message.remove_reaction(u"\u27A1", user)
                    continue
                elif str(reaction) == u"\u274C":
                    await message.delete()
                    return
            except asyncio.TimeoutError:
                user = bot.user
                await message.remove_reaction(u"\u27A1", user)
                await message.remove_reaction(u"\u274C", user)
                break

        await message.remove_reaction(u"\u27A1", user)
        await message.remove_reaction(u"\u274C", user)      
        await asyncio.sleep(60)
        chan = ["🏮┃anime-manga-chat"]
        if str(ctx.channel) in chan:
            await message.delete()
        elif str(ctx.channel) == "👍┃anime-manga-recommendations":
            return




@bot.command()
async def character(ctx, *, query=None):
    guild = bot.get_guild(661211931558019072)
    channels = ["🏮┃anime-manga-chat", "👍┃anime-manga-recommendations"]
    member = ctx.message.author
    if str(ctx.channel) in channels:
        if query is None:
            embed = discord.Embed(title='Usage', description='.character name')
            await ctx.send(embed=embed)
            return
        jikan = Jikan()
        b = jikan.search('character', f'{query}')
        results = b['results']
        message = await ctx.send('Searching...')
        for ch in results:
            malid = ch['mal_id']
            cha = jikan.character(malid)
            ab = cha['about']
            abo = str(ab)
            about = abo.replace("\\n", "")
            image = cha['image_url']
            url = cha['url']
            name = cha['name']
            animeresult = cha['animeography']
            mangaresult = cha['mangaography']
            ma = len(mangaresult)
            ani = len(animeresult)
            if ani > 3:
                ani = 3
            embed = discord.Embed(title=f'{name}', description=f'{about}'[:1000])
            embed.set_image(url=f'{image}')
            embed.add_field(name=':paperclip: **Character MyAnimeList\n**', value=f'[MyAnimeList]({url})')
            m = 0
            for i in range(ani):
                anime = animeresult[m]
                aname = anime['name']
                arole = anime['role']
                aurl = anime['url']
                embed.add_field(name=':computer: **Anime\n**', value=f'{aname}')
                embed.add_field(name=':movie_camera: **Role\n**', value=f'{arole}')
                embed.add_field(name=':paperclip: **Anime MyAnimeList\n**', value=f'[MyAnimeList]({aurl})')
                m += 1
            if mangaresult:
                manga = mangaresult[0]
                maname = manga['name']
                maurl = manga['url']
                embed.add_field(name=':book: **Manga\n**', value=f'{maname}')
                embed.add_field(name=':paperclip: **Manga MyAnimeList\n**', value=f'[MyAnimeList]({maurl})')
            await message.edit(embed=embed)
            await message.add_reaction(u"\u27A1")
            await message.add_reaction(u"\u274C")
            emote = [u"\u27A1", u"\u274C"]
            try:
                def check(reaction, user):
                    return (reaction.message.id == message.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                if str(reaction) == u"\u27A1":
                    await message.remove_reaction(u"\u27A1", user)
                    continue
                elif str(reaction) == u"\u274C":
                    await message.delete()
                    return
            except asyncio.TimeoutError:
                user = bot.user
                await message.remove_reaction(u"\u27A1", user)
                await message.remove_reaction(u"\u274C", user)
                break

        await message.remove_reaction(u"\u27A1", user)
        await message.remove_reaction(u"\u274C", user)      
        await asyncio.sleep(60)
        await message.delete()


@bot.command()
@commands.cooldown(1, 600, type=commands.BucketType.channel)
async def seasonal(ctx, year=0, *,  s=None):
    guild = bot.get_guild(661211931558019072)
    channels = ["🏮┃anime-manga-chat", "👍┃anime-manga-recommendations"]
    member = ctx.message.author
    if str(ctx.channel) in channels:
        if s is not None:
            season = str(s)
        elif s is None:
            d = datetime.datetime.now()
            t = d.strftime('%m') 
            print(t)
            ti = int(t)
            year  = d.strftime('%Y')
            if ti == 1 or ti == 2 or ti == 3:
                season = 'winter'
            elif ti == 4 or ti == 5 or ti == 6:
                season = 'spring'
            elif ti == 7 or ti == 8 or ti == 9:
                season = 'summer'
            elif ti == 10 or ti == 11 or ti == 12:
                season = 'fall'
        jikan = Jikan()
        print(season)
        print(year)
        b = jikan.season(year=year, season=season)
        anim = b['anime']
        ani = len(anim)
        m = 0
        message = await ctx.send('Searching...')
        for anime in range(ani):
            anime = anim[m]
            air = anime['airing_start']
            url = anime['url']
            image = anime['image_url']
            name = anime['title']
            synopsis = anime['synopsis']
            episodes = anime['episodes']
            status = anime['continuing']
            rate = anime['score']
            embed=discord.Embed()
            embed.add_field(name=f'{name}', value=f'{synopsis}'[:1000])
            embed.add_field(name=':star: **Rating\n**', value=f'{rate}'[:1000])
            embed.set_thumbnail(url=f'{image}')
            embed.add_field(name=':computer: **Episodes\n**', value=f'{episodes}'[:1000])
            embed.add_field(name=':satellite:  **Still Airing\n**', value=f'{status}'[:1000])
            embed.add_field(name=':calendar_spiral: **Aired\n**', value=f'{air}')
            embed.add_field(name=':paperclip: **MyAnimeList\n**', value=f'[MyAnimeList]({url})'[:1000])
            await message.edit(embed=embed)
            await message.add_reaction(u"\u27A1")
            await message.add_reaction(u"\u274C")
            emote = [u"\u27A1", u"\u274C"]
            try:
                def check(reaction, user):
                    return (reaction.message.id == message.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                if str(reaction) == u"\u27A1":
                    await message.remove_reaction(u"\u27A1", user)
                    m += 1
                    continue
                elif str(reaction) == u"\u274C":
                    await message.delete()
                    return
            except asyncio.TimeoutError:
                user = bot.user
                await message.remove_reaction(u"\u27A1", user)
                await message.remove_reaction(u"\u274C", user)
                break

        await message.remove_reaction(u"\u27A1", user)
        await message.remove_reaction(u"\u274C", user)      
        await asyncio.sleep(60)
        await message.delete()


    
@seasonal.error
async def seasonal_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        c = '{:.0f}'.format(error.retry_after)            
        await ctx.send(f'Please try again after {c} seconds')



@bot.command()
@commands.cooldown(1, 600, type=commands.BucketType.channel)
async def upcominganimes(ctx):
    guild = bot.get_guild(661211931558019072)
    channels = ["🏮┃anime-manga-chat", "👍┃anime-manga-recommendations"]
    member = ctx.message.author
    if str(ctx.channel) in channels:
        jikan = Jikan()
        b = jikan.season_later()
        anim = b['anime']
        ani = len(anim)
        m = 0
        message = await ctx.send('Searching...')
        for anime in range(ani):
            anime = anim[m]
            air = anime['airing_start']
            url = anime['url']
            image = anime['image_url']
            name = anime['title']
            synopsis = anime['synopsis']
            episodes = anime['episodes']
            status = anime['continuing']
            rate = anime['score']
            embed=discord.Embed()
            embed.add_field(name=f'{name}', value=f'{synopsis}'[:1000])
            embed.set_image(url=f'{image}')
            embed.add_field(name=':satellite:  **Airing\n**', value=f'{status}'[:1000])
            embed.add_field(name=':paperclip: **MyAnimeList\n**', value=f'[MyAnimeList]({url})'[:1000])
            await message.edit(embed=embed)
            await message.add_reaction(u"\u27A1")
            await message.add_reaction(u"\u274C")
            emote = [u"\u27A1", u"\u274C"]
            try:
                def check(reaction, user):
                    return (reaction.message.id == message.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                if str(reaction) == u"\u27A1":
                    await message.remove_reaction(u"\u27A1", user)
                    m += 1
                    continue
                elif str(reaction) == u"\u274C":
                    await message.delete()
                    return
            except asyncio.TimeoutError:
                user = bot.user
                await message.remove_reaction(u"\u27A1", user)
                await message.remove_reaction(u"\u274C", user)
                break

        await message.remove_reaction(u"\u27A1", user)
        await message.remove_reaction(u"\u274C", user)      
        await asyncio.sleep(60)
        await message.delete()


@seasonal.error
async def seasonal_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        c = '{:.0f}'.format(error.retry_after)            
        await ctx.send(f'Please try again after {c} seconds')




@bot.command()
async def mal(ctx, *, u=None):
    guild = bot.get_guild(661211931558019072)
    channels = ["🏮┃anime-manga-chat", "👍┃anime-manga-recommendations"]
    member = ctx.message.author
    if str(ctx.channel) in channels:
        if u is None:
            await ctx.send('User not found')
            return
        jikan = Jikan()
        us = str(u)
        user = jikan.user(username=us, request='profile')
        name = user['username']
        url = user['url']
        anime = user['anime_stats']
        days = anime['days_watched']
        score = anime['mean_score']
        watching = anime['watching']
        completed = anime['completed']
        hold = anime['on_hold']
        dropped = anime['dropped']
        ptw = anime['plan_to_watch']
        rewatched = anime['rewatched']
        episodes = anime['episodes_watched']
        manga = user['manga_stats']
        mdays = manga['days_read']
        mscore = manga['mean_score']
        mreading = manga['reading']
        mcompleted = manga['completed']
        mhold = manga['on_hold']
        mdropped = manga['dropped']
        mptw = manga['plan_to_read']
        mreread = manga['reread']
        mchapters = manga['chapters_read']
        mvolumes = manga['volumes_read']
        embed = discord.Embed(title=f'{name}')
        embed.add_field(name=f':computer: **Anime Stats\n**', value=f':calendar_spiral: **Watch Time** : {days} days,  '
                                                                    f':star: **Mean Score** : {score},  '
                                                                    f':desktop: **Watching** : {watching},  '
                                                                    f':ballot_box_with_check: **Completed** : {completed},  '
                                                                    f':grey_exclamation: **On Hold** : {hold},  '
                                                                    f':x: **Dropped** : {dropped},  '
                                                                    f':calendar: **Planned** : {ptw},  '
                                                                    f':repeat_one: **Rewatched** : {rewatched},  '
                                                                    f':1234: **Total Episodes** : {episodes},  ')
        embed.add_field(name=f':notebook_with_decorative_cover: **Manga Stats\n**', value=f':calendar_spiral: **Read Time** : {mdays} days,  '
                                                                                            f':star: **Mean Score** : {mscore},  '
                                                                                            f':book: **Reading** : {mreading},  '
                                                                                            f':ballot_box_with_check: **Completed** : {mcompleted},  '
                                                                                            f':grey_exclamation: **On Hold** : {mhold},  '
                                                                                            f':x: **Dropped** : {mdropped},  '
                                                                                            f':calendar: **Planned** : {mptw},  '
                                                                                            f':repeat_one: **Reread** : {mreread},  '
                                                                                            f':dividers: **Total Chapters** : {mchapters},  '
                                                                                            f':file_folder: **Total Volumes** : {mvolumes},  ')
        embed.add_field(name=':paperclip: **User\'s MyAnimeList\n**', value=f'[MyAnimeList]({url})'[:1000])
        await ctx.send(embed=embed)






                                         #Movies & TV Series



@bot.command()
async def tv(ctx, *, name=None):
    channels = ["📽┃series-movie-chat"]
    if str(ctx.channel) in channels:
        try:
            if name is None:
                embed = discord.Embed(title='Usage', description='.tv name, you can name any movie or tv series')
                await ctx.send(embed=embed)
                return
            elif name is not None:
                ia = imdb.IMDb()
                a = str(name)
                movies = ia.search_movie(a)
                movieid1 = movies[0].movieID
                movie1 = ia.get_movie(movieid1)
                a0 = movie1.data['plot']
                a00 = str(a0)
                synopsis1 = re.sub("[^a-zA-Z0-9:.']+", ' ', a00)
                cover1 = movie1.data['cover url']
                a10 = movie1.data['genres']
                a1 = str(a10)
                genres1 =(re.sub(r"\W+|&nbsp", " ", a1))
                a20 = movie1.data['runtimes']
                a2 = str(a20)
                runtimes1 = (re.sub(r"\W+|&nbsp", " ", a2))
                aired1 = movie1.data['year']
                title1 = movie1.data['original title']
                rating1 = movie1.data['rating'] 
                kind1 = movie1.data['kind'] 
                if cover1 is None:
                    embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                    embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                    if kind1 != "movie":
                        seasons1 = movie1.data['number of seasons']
                        embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                        embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                    embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                    if kind1 == "movie":
                        embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                    embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                    embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                    embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])    
                elif cover1 is not None:
                    embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                    embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                    if kind1 != "movie":
                        seasons1 = movie1.data['number of seasons']
                        embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                        embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                    embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                    if kind1 == "movie":
                        embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                    embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                    embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                    embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])
                    embed.set_thumbnail(url=cover1)
                msg = await ctx.send(embed=embed)
                await msg.add_reaction(u"\u27A1")
                await msg.add_reaction(u"\u274C")
                emote = [u"\u27A1", u"\u274C"]
                try:
                    def check(reaction, user):
                        return (reaction.message.id == msg.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                    if str(reaction) == u"\u27A1":
                        await msg.remove_reaction(u"\u27A1", user)
                        ia = imdb.IMDb()
                        movies = ia.search_movie(a)
                        movieid1 = movies[1].movieID
                        movie1 = ia.get_movie(movieid1)
                        a0 = movie1.data['plot']
                        a00 = str(a0)
                        synopsis1 = re.sub("[^a-zA-Z0-9:.']+", ' ', a00)
                        cover1 = movie1.data['cover url']
                        a10 = movie1.data['genres']
                        a1 = str(a10)
                        genres1 =(re.sub(r"\W+|&nbsp", " ", a1))
                        a20 = movie1.data['runtimes']
                        a2 = str(a20)
                        runtimes1 = (re.sub(r"\W+|&nbsp", " ", a2))
                        aired1 = movie1.data['year']
                        title1 = movie1.data['original title']
                        rating1 = movie1.data['rating'] 
                        kind1 = movie1.data['kind']
                        if cover1 is None:
                            embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                            embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                            if kind1 != "movie":
                                seasons1 = movie1.data['number of seasons']
                                embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                            embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                            if kind1 == "movie":
                                embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                            embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                            embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                            embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])    
                        elif cover1 is not None:
                            embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                            embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                            if kind1 != "movie":
                                seasons1 = movie1.data['number of seasons']
                                embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                            embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                            if kind1 == "movie":
                                embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                            embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                            embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                            embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])
                            embed.set_thumbnail(url=cover1)
                        await msg.edit(embed=embed)
                        await msg.add_reaction(u"\u27A1")
                        await msg.add_reaction(u"\u274C")
                        emote = [u"\u27A1", u"\u274C"]
                        try:
                            def check(reaction, user):
                                return (reaction.message.id == msg.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                            if str(reaction) == u"\u27A1":
                                await msg.remove_reaction(u"\u27A1", user)
                                ia = imdb.IMDb()
                                movies = ia.search_movie(a)
                                movieid1 = movies[2].movieID
                                movie1 = ia.get_movie(movieid1)
                                a0 = movie1.data['plot']
                                a00 = str(a0)
                                synopsis1 = re.sub("[^a-zA-Z0-9:.']+", ' ', a00)
                                cover1 = movie1.data['cover url']
                                a10 = movie1.data['genres']
                                a1 = str(a10)
                                genres1 =(re.sub(r"\W+|&nbsp", " ", a1))
                                a20 = movie1.data['runtimes']
                                a2 = str(a20)
                                runtimes1 = (re.sub(r"\W+|&nbsp", " ", a2))
                                aired1 = movie1.data['year']
                                title1 = movie1.data['original title']
                                rating1 = movie1.data['rating'] 
                                kind1 = movie1.data['kind']
                                if cover1 is None:
                                    embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                    embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                    if kind1 != "movie":
                                        seasons1 = movie1.data['number of seasons']
                                        embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                        embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                    embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                    if kind1 == "movie":
                                        embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                    embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                    embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                    embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])    
                                elif cover1 is not None:
                                    embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                    embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                    if kind1 != "movie":
                                        seasons1 = movie1.data['number of seasons']
                                        embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                        embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                    embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                    if kind1 == "movie":
                                        embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                    embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                    embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                    embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])
                                    embed.set_thumbnail(url=cover1)
                                await msg.edit(embed=embed)
                                await msg.add_reaction(u"\u27A1")
                                await msg.add_reaction(u"\u274C")
                                emote = [u"\u27A1", u"\u274C"]
                                try:
                                    def check(reaction, user):
                                        return (reaction.message.id == msg.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                                    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                                    if str(reaction) == u"\u27A1":
                                        await msg.remove_reaction(u"\u27A1", user)
                                        ia = imdb.IMDb()
                                        movies = ia.search_movie(a)
                                        movieid1 = movies[3].movieID
                                        movie1 = ia.get_movie(movieid1)
                                        a0 = movie1.data['plot']
                                        a00 = str(a0)
                                        synopsis1 = re.sub("[^a-zA-Z0-9:.']+", ' ', a00)
                                        cover1 = movie1.data['cover url']
                                        a10 = movie1.data['genres']
                                        a1 = str(a10)
                                        genres1 =(re.sub(r"\W+|&nbsp", " ", a1))
                                        a20 = movie1.data['runtimes']
                                        a2 = str(a20)
                                        runtimes1 = (re.sub(r"\W+|&nbsp", " ", a2))
                                        aired1 = movie1.data['year']
                                        title1 = movie1.data['original title']
                                        rating1 = movie1.data['rating'] 
                                        kind1 = movie1.data['kind']
                                        if cover1 is None:
                                            embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                            embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                            if kind1 != "movie":
                                                seasons1 = movie1.data['number of seasons']
                                                embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                                embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                            embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                            if kind1 == "movie":
                                                embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                            embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                            embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                            embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])    
                                        elif cover1 is not None:
                                            embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                            embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                            if kind1 != "movie":
                                                seasons1 = movie1.data['number of seasons']
                                                embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                                embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                            embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                            if kind1 == "movie":
                                                embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                            embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                            embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                            embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])
                                            embed.set_thumbnail(url=cover1)
                                        await msg.edit(embed=embed)
                                        await msg.add_reaction(u"\u27A1")
                                        await msg.add_reaction(u"\u274C")
                                        emote = [u"\u27A1", u"\u274C"]
                                        try:
                                            def check(reaction, user):
                                                return (reaction.message.id == msg.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                                            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                                            if str(reaction) == u"\u27A1":
                                                await msg.remove_reaction(u"\u27A1", user)
                                                ia = imdb.IMDb()
                                                movies = ia.search_movie(a)
                                                movieid1 = movies[4].movieID
                                                movie1 = ia.get_movie(movieid1)
                                                a0 = movie1.data['plot']
                                                a00 = str(a0)
                                                synopsis1 = re.sub("[^a-zA-Z0-9:.']+", ' ', a00)
                                                cover1 = movie1.data['cover url']
                                                a10 = movie1.data['genres']
                                                a1 = str(a10)
                                                genres1 =(re.sub(r"\W+|&nbsp", " ", a1))
                                                a20 = movie1.data['runtimes']
                                                a2 = str(a20)
                                                runtimes1 = (re.sub(r"\W+|&nbsp", " ", a2))
                                                aired1 = movie1.data['year']
                                                title1 = movie1.data['original title']
                                                rating1 = movie1.data['rating'] 
                                                kind1 = movie1.data['kind']
                                                if cover1 is None:
                                                    embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                                    embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                                    if kind1 != "movie":
                                                        seasons1 = movie1.data['number of seasons']
                                                        embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                                        embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                                    embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                                    if kind1 == "movie":
                                                        embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                                    embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                                    embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                                    embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])    
                                                elif cover1 is not None:
                                                    embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                                    embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                                    if kind1 != "movie":
                                                        seasons1 = movie1.data['number of seasons']
                                                        embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                                        embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                                    embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                                    if kind1 == "movie":
                                                        embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                                    embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                                    embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                                    embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])
                                                    embed.set_thumbnail(url=cover1)
                                                await msg.edit(embed=embed)
                                                await msg.add_reaction(u"\u27A1")
                                                await msg.add_reaction(u"\u274C")
                                                emote = [u"\u27A1", u"\u274C"]
                                                try:
                                                    def check(reaction, user):
                                                        return (reaction.message.id == msg.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                                                    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                                                    if str(reaction) == u"\u27A1":
                                                        await msg.remove_reaction(u"\u27A1", user)
                                                        ia = imdb.IMDb()
                                                        movies = ia.search_movie(a)
                                                        movieid1 = movies[5].movieID
                                                        movie1 = ia.get_movie(movieid1)
                                                        a0 = movie1.data['plot']
                                                        a00 = str(a0)
                                                        synopsis1 = re.sub("[^a-zA-Z0-9:.']+", ' ', a00)
                                                        cover1 = movie1.data['cover url']
                                                        a10 = movie1.data['genres']
                                                        a1 = str(a10)
                                                        genres1 =(re.sub(r"\W+|&nbsp", " ", a1))
                                                        a20 = movie1.data['runtimes']
                                                        a2 = str(a20)
                                                        runtimes1 = (re.sub(r"\W+|&nbsp", " ", a2))
                                                        aired1 = movie1.data['year']
                                                        title1 = movie1.data['original title']
                                                        rating1 = movie1.data['rating'] 
                                                        kind1 = movie1.data['kind']
                                                        if cover1 is None:
                                                            embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                                            embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                                            if kind1 != "movie":
                                                                seasons1 = movie1.data['number of seasons']
                                                                embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                                                embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                                            embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                                            if kind1 == "movie":
                                                                embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                                            embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                                            embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                                            embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])    
                                                        elif cover1 is not None:
                                                            embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                                            embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                                            if kind1 != "movie":
                                                                seasons1 = movie1.data['number of seasons']
                                                                embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                                                embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                                            embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                                            if kind1 == "movie":
                                                                embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                                            embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                                            embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                                            embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])
                                                            embed.set_thumbnail(url=cover1)
                                                        await msg.edit(embed=embed)
                                                        await msg.add_reaction(u"\u27A1")
                                                        await msg.add_reaction(u"\u274C")
                                                        emote = [u"\u27A1", u"\u274C"]
                                                        try:
                                                            def check(reaction, user):
                                                                return (reaction.message.id == msg.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                                                            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                                                            if str(reaction) == u"\u27A1":
                                                                await msg.remove_reaction(u"\u27A1", user)
                                                                ia = imdb.IMDb()
                                                                movies = ia.search_movie(a)
                                                                movieid1 = movies[6].movieID
                                                                movie1 = ia.get_movie(movieid1)
                                                                a0 = movie1.data['plot']
                                                                a00 = str(a0)
                                                                synopsis1 = re.sub("[^a-zA-Z0-9:.']+", ' ', a00)
                                                                cover1 = movie1.data['cover url']
                                                                a10 = movie1.data['genres']
                                                                a1 = str(a10)
                                                                genres1 =(re.sub(r"\W+|&nbsp", " ", a1))
                                                                a20 = movie1.data['runtimes']
                                                                a2 = str(a20)
                                                                runtimes1 = (re.sub(r"\W+|&nbsp", " ", a2))
                                                                aired1 = movie1.data['year']
                                                                title1 = movie1.data['original title']
                                                                rating1 = movie1.data['rating'] 
                                                                kind1 = movie1.data['kind']
                                                                if cover1 is None:
                                                                    embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                                                    embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                                                    if kind1 != "movie":
                                                                        seasons1 = movie1.data['number of seasons']
                                                                        embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                                                        embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                                                    embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                                                    if kind1 == "movie":
                                                                        embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                                                    embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                                                    embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                                                    embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])    
                                                                elif cover1 is not None:
                                                                    embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                                                    embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                                                    if kind1 != "movie":
                                                                        seasons1 = movie1.data['number of seasons']
                                                                        embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                                                        embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                                                    embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                                                    if kind1 == "movie":
                                                                        embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                                                    embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                                                    embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                                                    embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])
                                                                    embed.set_thumbnail(url=cover1)
                                                                await msg.edit(embed=embed)
                                                                await msg.add_reaction(u"\u27A1")
                                                                await msg.add_reaction(u"\u274C")
                                                                emote = [u"\u27A1", u"\u274C"]
                                                                try:
                                                                    def check(reaction, user):
                                                                        return (reaction.message.id == msg.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                                                                    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                                                                    if str(reaction) == u"\u27A1":
                                                                        await msg.remove_reaction(u"\u27A1", user)
                                                                        ia = imdb.IMDb()
                                                                        movies = ia.search_movie(a)
                                                                        movieid1 = movies[7].movieID
                                                                        movie1 = ia.get_movie(movieid1)
                                                                        a0 = movie1.data['plot']
                                                                        a00 = str(a0)
                                                                        synopsis1 = re.sub("[^a-zA-Z0-9:.']+", ' ', a00)
                                                                        cover1 = movie1.data['cover url']
                                                                        a10 = movie1.data['genres']
                                                                        a1 = str(a10)
                                                                        genres1 =(re.sub(r"\W+|&nbsp", " ", a1))
                                                                        a20 = movie1.data['runtimes']
                                                                        a2 = str(a20)
                                                                        runtimes1 = (re.sub(r"\W+|&nbsp", " ", a2))
                                                                        aired1 = movie1.data['year']
                                                                        title1 = movie1.data['original title']
                                                                        rating1 = movie1.data['rating'] 
                                                                        kind1 = movie1.data['kind']
                                                                        if cover1 is None:
                                                                            embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                                                            embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                                                            if kind1 != "movie":
                                                                                seasons1 = movie1.data['number of seasons']
                                                                                embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                                                                embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                                                            embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                                                            if kind1 == "movie":
                                                                                embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                                                            embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                                                            embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                                                            embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])    
                                                                        elif cover1 is not None:
                                                                            embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                                                            embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                                                            if kind1 != "movie":
                                                                                seasons1 = movie1.data['number of seasons']
                                                                                embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                                                                embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                                                            embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                                                            if kind1 == "movie":
                                                                                embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                                                            embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                                                            embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                                                            embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])
                                                                            embed.set_thumbnail(url=cover1)
                                                                        await msg.edit(embed=embed)
                                                                        await msg.add_reaction(u"\u27A1")
                                                                        await msg.add_reaction(u"\u274C")
                                                                        emote = [u"\u27A1", u"\u274C"]
                                                                        try:
                                                                            def check(reaction, user):
                                                                                return (reaction.message.id == msg.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                                                                            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                                                                            if str(reaction) == u"\u27A1":
                                                                                await msg.remove_reaction(u"\u27A1", user)
                                                                                ia = imdb.IMDb()
                                                                                movies = ia.search_movie(a)
                                                                                movieid1 = movies[8].movieID
                                                                                movie1 = ia.get_movie(movieid1)
                                                                                a0 = movie1.data['plot']
                                                                                a00 = str(a0)
                                                                                synopsis1 = re.sub("[^a-zA-Z0-9:.']+", ' ', a00)
                                                                                cover1 = movie1.data['cover url']
                                                                                a10 = movie1.data['genres']
                                                                                a1 = str(a10)
                                                                                genres1 =(re.sub(r"\W+|&nbsp", " ", a1))
                                                                                a20 = movie1.data['runtimes']
                                                                                a2 = str(a20)
                                                                                runtimes1 = (re.sub(r"\W+|&nbsp", " ", a2))
                                                                                aired1 = movie1.data['year']
                                                                                title1 = movie1.data['original title']
                                                                                rating1 = movie1.data['rating'] 
                                                                                kind1 = movie1.data['kind']
                                                                                if cover1 is None:
                                                                                    embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                                                                    embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                                                                    if kind1 != "movie":
                                                                                        seasons1 = movie1.data['number of seasons']
                                                                                        embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                                                                        embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                                                                    embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                                                                    if kind1 == "movie":
                                                                                        embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                                                                    embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                                                                    embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                                                                    embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])    
                                                                                elif cover1 is not None:
                                                                                    embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                                                                    embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                                                                    if kind1 != "movie":
                                                                                        seasons1 = movie1.data['number of seasons']
                                                                                        embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                                                                        embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                                                                    embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                                                                    if kind1 == "movie":
                                                                                        embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                                                                    embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                                                                    embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                                                                    embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])
                                                                                    embed.set_thumbnail(url=cover1)
                                                                                await msg.edit(embed=embed)
                                                                                await msg.add_reaction(u"\u27A1")
                                                                                await msg.add_reaction(u"\u274C")
                                                                                emote = [u"\u27A1", u"\u274C"]
                                                                                try:
                                                                                    def check(reaction, user):
                                                                                        return (reaction.message.id == msg.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                                                                                    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                                                                                    if str(reaction) == u"\u27A1":
                                                                                        await msg.remove_reaction(u"\u27A1", user)
                                                                                        ia = imdb.IMDb()
                                                                                        movies = ia.search_movie(a)
                                                                                        movieid1 = movies[9].movieID
                                                                                        movie1 = ia.get_movie(movieid1)
                                                                                        a0 = movie1.data['plot']
                                                                                        a00 = str(a0)
                                                                                        synopsis1 = re.sub("[^a-zA-Z0-9:.']+", ' ', a00)
                                                                                        cover1 = movie1.data['cover url']
                                                                                        a10 = movie1.data['genres']
                                                                                        a1 = str(a10)
                                                                                        genres1 =(re.sub(r"\W+|&nbsp", " ", a1))
                                                                                        a20 = movie1.data['runtimes']
                                                                                        a2 = str(a20)
                                                                                        runtimes1 = (re.sub(r"\W+|&nbsp", " ", a2))
                                                                                        aired1 = movie1.data['year']
                                                                                        title1 = movie1.data['original title']
                                                                                        rating1 = movie1.data['rating'] 
                                                                                        kind1 = movie1.data['kind']
                                                                                        if cover1 is None:
                                                                                            embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                                                                            embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                                                                            if kind1 != "movie":
                                                                                                seasons1 = movie1.data['number of seasons']
                                                                                                embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                                                                                embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                                                                            embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                                                                            if kind1 == "movie":
                                                                                                embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                                                                            embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                                                                            embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                                                                            embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])    
                                                                                        elif cover1 is not None:
                                                                                            embed = discord.Embed(title=f'{title1}', description=f'{synopsis1}'[:1000])
                                                                                            embed.add_field(name=':tv: **Type\n**', value=f'{kind1}'[:1000])
                                                                                            if kind1 != "movie":
                                                                                                seasons1 = movie1.data['number of seasons']
                                                                                                embed.add_field(name=':computer: **Seasons\n**', value=f'{seasons1}'[:1000])
                                                                                                embed.add_field(name=':play_pause: **Length Per Episode\n**', value=f'{runtimes1} minutes'[:1000])
                                                                                            embed.add_field(name=':star: **Rating\n**', value=f'{rating1}'[:1000])
                                                                                            if kind1 == "movie":
                                                                                                embed.add_field(name=':play_pause: **Length\n**', value=f'{runtimes1} minutes'[:1000])
                                                                                            embed.add_field(name=':cd: **Genres\n**', value=f'{genres1}'[:1000])
                                                                                            embed.add_field(name=':satellite: **Released In\n**', value=f'{aired1}'[:1000])
                                                                                            embed.add_field(name=':paperclip: **Link\n**', value=f'[IMDb](https://www.imdb.com/title/tt{movieid1})'[:1000])
                                                                                            embed.set_thumbnail(url=cover1)
                                                                                        await msg.edit(embed=embed)
                                                                                        await msg.add_reaction(u"\u274C")
                                                                                        emote = [u"\u274C"]
                                                                                        try:
                                                                                            def check(reaction, user):
                                                                                                return (reaction.message.id == msg.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                                                                                            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)  
                                                                                            if str(reaction) == u"\u274C":
                                                                                                await msg.delete()
                                                                                                return
                                                                                        except asyncio.TimeoutError:
                                                                                            user = bot.user
                                                                                            await msg.remove_reaction(u"\u27A1", user)
                                                                                            await msg.remove_reaction(u"\u274C", user)
                                                                                            await asyncio.sleep(60)
                                                                                            await msg.delete()
                                                                                            return
                                                                                    elif str(reaction) == u"\u274C":
                                                                                        await msg.delete()
                                                                                        return
                                                                                except asyncio.TimeoutError:
                                                                                    user = bot.user
                                                                                    await msg.remove_reaction(u"\u27A1", user)
                                                                                    await msg.remove_reaction(u"\u274C", user)
                                                                                    await asyncio.sleep(60)
                                                                                    await msg.delete()
                                                                                    return                                                                                
                                                                            elif str(reaction) == u"\u274C":
                                                                                await msg.delete()
                                                                                return
                                                                        except asyncio.TimeoutError:
                                                                            user = bot.user
                                                                            await msg.remove_reaction(u"\u27A1", user)
                                                                            await msg.remove_reaction(u"\u274C", user)
                                                                            await asyncio.sleep(60)
                                                                            await msg.delete()
                                                                            return
                                                                    elif str(reaction) == u"\u274C":
                                                                        await msg.delete()
                                                                        return
                                                                except asyncio.TimeoutError:
                                                                    user = bot.user
                                                                    await msg.remove_reaction(u"\u27A1", user)
                                                                    await msg.remove_reaction(u"\u274C", user)
                                                                    await asyncio.sleep(60)
                                                                    await msg.delete()
                                                                    return                                                                
                                                            elif str(reaction) == u"\u274C":
                                                                await msg.delete()
                                                                return
                                                        except asyncio.TimeoutError:
                                                            user = bot.user
                                                            await msg.remove_reaction(u"\u27A1", user)
                                                            await msg.remove_reaction(u"\u274C", user)
                                                            await asyncio.sleep(60)
                                                            await msg.delete()
                                                            return
                                                    elif str(reaction) == u"\u274C":
                                                        await msg.delete()
                                                        return
                                                except asyncio.TimeoutError:
                                                    user = bot.user
                                                    await msg.remove_reaction(u"\u27A1", user)
                                                    await msg.remove_reaction(u"\u274C", user)
                                                    await asyncio.sleep(60)
                                                    await msg.delete()
                                                    return                                                
                                            elif str(reaction) == u"\u274C":
                                                await msg.delete()
                                                return
                                        except asyncio.TimeoutError:
                                            user = bot.user
                                            await msg.remove_reaction(u"\u27A1", user)
                                            await msg.remove_reaction(u"\u274C", user)
                                            await asyncio.sleep(60)
                                            await msg.delete()
                                            return
                                    elif str(reaction) == u"\u274C":
                                        await msg.delete()
                                        return
                                except asyncio.TimeoutError:
                                    user = bot.user
                                    await msg.remove_reaction(u"\u27A1", user)
                                    await msg.remove_reaction(u"\u274C", user)
                                    await asyncio.sleep(60)
                                    await msg.delete()
                                    return
                            elif str(reaction) == u"\u274C":
                                await msg.delete()
                                return
                        except asyncio.TimeoutError:
                            user = bot.user
                            await msg.remove_reaction(u"\u27A1", user)
                            await msg.remove_reaction(u"\u274C", user)
                            await asyncio.sleep(60)
                            await msg.delete()
                            return
                    elif str(reaction) == u"\u274C":
                        await msg.delete()
                        return
                except asyncio.TimeoutError:
                    user = bot.user
                    await msg.remove_reaction(u"\u27A1", user)
                    await msg.remove_reaction(u"\u274C", user)
                    return
            await msg.remove_reaction(u"\u27A1", user)
            await msg.remove_reaction(u"\u274C", user)      
            await asyncio.sleep(60)
            await msg.delete()
        except (IMDbError, KeyError):
           await ctx.send('Page Not Found')
           await msg.delete()




@bot.command()
async def movie(ctx, *, nam=None):
    channels = ["📽┃series-movie-chat"]
    if str(ctx.channel) in channels:
            if nam is None:
                embed = discord.Embed(title='Usage', description='.movie name')
                await ctx.send(embed=embed)
                return
            elif nam is not None:
                name = str(nam)
                tmdb.API_KEY = '6a8577a6eccea6981d8ab8c68ab5ffcb'
                search = tmdb.Search()
                response = search.movie(query=name)
                message = await ctx.send('Searching...')
                for s in search.results:
                    title = s['title']
                    thumbnail = s['poster_path']
                    link = s['id']
                    movie = tmdb.Movies(link)
                    response = movie.info()
                    votes = s['vote_count']
                    rating = s['vote_average']
                    embed = discord.Embed()
                    embed.add_field(name=f'{title}', value=s['overview'][:1000])
                    embed.add_field(name=':star: **Rating\n**', value=f'{rating}\({votes} votes\)')
                    embed.add_field(name=':calendar_spiral: **Released\n**', value=s['release_date'])
                    embed.add_field(name=':paperclip: **Link\n**', value=f'[TMDb](https://www.themoviedb.org/movie/{link})')
                    embed.set_thumbnail(url=f'https://image.tmdb.org/t/p/original{thumbnail}')
                    await message.edit(embed=embed)
                    await message.edit(embed=embed)
                    await message.add_reaction(u"\u27A1")
                    await message.add_reaction(u"\u274C")
                    emote = [u"\u27A1", u"\u274C"]
                    try:
                        def check(reaction, user):
                            return (reaction.message.id == message.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                        if str(reaction) == u"\u27A1":
                            await message.remove_reaction(u"\u27A1", user)
                            continue
                        elif str(reaction) == u"\u274C":
                            await message.delete()
                            return
                    except asyncio.TimeoutError:
                        user = bot.user
                        await message.remove_reaction(u"\u27A1", user)
                        await message.remove_reaction(u"\u274C", user)
                        
                await message.remove_reaction(u"\u27A1", user)
                await message.remove_reaction(u"\u274C", user)      
                await asyncio.sleep(60)
                await message.delete()



                    

@bot.command()
async def movieimage(ctx, *, nam=None):
    channels = ["📽┃series-movie-chat"]
    if str(ctx.channel) in channels:
            if nam is None:
                embed = discord.Embed(title='Usage', description='.movieimage name')
                await ctx.send(embed=embed)
                return
            elif nam is not None:
                name = str(nam)
                tmdb.API_KEY = '6a8577a6eccea6981d8ab8c68ab5ffcb'
                search = tmdb.Search()
                response = search.movie(query=name)
                message = await ctx.send('Searching...')
                for s in search.results:
                    thumbnail = s['poster_path']
                    link = s['id']
                    votes = s['vote_count']
                    rating = s['vote_average']
                    embed = discord.Embed(title=s['title'])
                    embed.set_image(url=f'https://image.tmdb.org/t/p/original{thumbnail}')
                    await message.edit(embed=embed)
                    await message.edit(embed=embed)
                    await message.add_reaction(u"\u27A1")
                    await message.add_reaction(u"\u274C")
                    emote = [u"\u27A1", u"\u274C"]
                    try:
                        def check(reaction, user):
                            return (reaction.message.id == message.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                        if str(reaction) == u"\u27A1":
                            await message.remove_reaction(u"\u27A1", user)
                            continue
                        elif str(reaction) == u"\u274C":
                            await message.delete()
                            return
                    except asyncio.TimeoutError:
                        user = bot.user
                        await message.remove_reaction(u"\u27A1", user)
                        await message.remove_reaction(u"\u274C", user)
                
                await message.remove_reaction(u"\u27A1", user)
                await message.remove_reaction(u"\u274C", user)      
                await asyncio.sleep(60)
                await message.delete()


@bot.command()
async def series(ctx, *, nam=None):
    channels = ["📽┃series-movie-chat"]
    if str(ctx.channel) in channels:
            if nam is None:
                embed = discord.Embed(title='Usage', description='.series name')
                await ctx.send(embed=embed)
                return
            elif nam is not None:
                name = str(nam)
                tmdb.API_KEY = '6a8577a6eccea6981d8ab8c68ab5ffcb'
                search = tmdb.Search()
                response = search.tv(query=name)
                message = await ctx.send('Searching...')
                for s in search.results:
                    title = s['original_name']
                    thumbnail = s['poster_path']
                    link = s['id']
                    votes = s['vote_count']
                    rating = s['vote_average']
                    embed = discord.Embed()
                    embed.add_field(name=s['original_name'], value=s['overview'][:1000])
                    embed.add_field(name=':star: **Rating\n**', value=f'{rating}\({votes} votes\)')
                    embed.add_field(name=':calendar_spiral: **Released\n**', value=s['first_air_date'])
                    embed.add_field(name=':paperclip: **Link\n**', value=f'[TMDb](https://www.themoviedb.org/tv/{link})')
                    embed.set_thumbnail(url=f'https://image.tmdb.org/t/p/original{thumbnail}')
                    await message.edit(embed=embed)
                    await message.edit(embed=embed)
                    await message.add_reaction(u"\u27A1")
                    await message.add_reaction(u"\u274C")
                    emote = [u"\u27A1", u"\u274C"]
                    try:
                        def check(reaction, user):
                            return (reaction.message.id == message.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                        if str(reaction) == u"\u27A1":
                            await message.remove_reaction(u"\u27A1", user)
                            continue
                        elif str(reaction) == u"\u274C":
                            await message.delete()
                            return
                    except asyncio.TimeoutError:
                        user = bot.user
                        await message.remove_reaction(u"\u27A1", user)
                        await message.remove_reaction(u"\u274C", user)
                
                await message.remove_reaction(u"\u27A1", user)
                await message.remove_reaction(u"\u274C", user)      
                await asyncio.sleep(60)
                await message.delete()



@bot.command()
async def trending(ctx, *, nam=None):
    channels = ["📽┃series-movie-chat"]
    if str(ctx.channel) in channels:
            if nam is None:
                embed = discord.Embed(title='Usage', description='.trending movies or .trending series')
                await ctx.send(embed=embed)
                return
            name = str(nam)
            if name == 'movies':
                tmdb.API_KEY = '6a8577a6eccea6981d8ab8c68ab5ffcb'
                search = tmdb.Trending()
                mov = search.info(media_type=name, time_window='week')
                movies = mov['results']
                movi = len(movies)
                message = await ctx.send('Searching...')
                m = 0
                for s in range(movi):
                    s = movies[m]
                    title = s['title']
                    thumbnail = s['poster_path']
                    link = s['id']
                    votes = s['vote_count']
                    rating = s['vote_average']
                    embed = discord.Embed()
                    embed.add_field(name=f'{title}', value=s['overview'][:1000])
                    embed.add_field(name=':star: **Rating\n**', value=f'{rating}\({votes} votes\)')
                    embed.add_field(name=':calendar_spiral: **Released\n**', value=s['release_date'])
                    embed.add_field(name=':paperclip: **Link\n**', value=f'[TMDb](https://www.themoviedb.org/movie/{link})')
                    embed.set_thumbnail(url=f'https://image.tmdb.org/t/p/original{thumbnail}')
                    await message.edit(embed=embed)
                    m += 1
                    await message.add_reaction(u"\u27A1")
                    await message.add_reaction(u"\u274C")
                    emote = [u"\u27A1", u"\u274C"]
                    try:
                        def check(reaction, user):
                            return (reaction.message.id == message.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                        if str(reaction) == u"\u27A1":
                            await message.remove_reaction(u"\u27A1", user)
                            continue
                        elif str(reaction) == u"\u274C":
                            await message.delete()
                            return
                    except asyncio.TimeoutError:
                        user = bot.user
                        await message.remove_reaction(u"\u27A1", user)
                        await message.remove_reaction(u"\u274C", user)
                
                await message.remove_reaction(u"\u27A1", user)
                await message.remove_reaction(u"\u274C", user)      
                await asyncio.sleep(60)
                await message.delete()

            elif name == 'series':
                name = str(nam)
                tmdb.API_KEY = '6a8577a6eccea6981d8ab8c68ab5ffcb'
                search = tmdb.Trending1()
                mov = search.info(media_type=name, time_window='week')
                movies = mov['results']
                movi = len(movies)
                message = await ctx.send('Searching...')
                m = 0
                for s in range(movi):
                    s = movies[m]
                    title = s['original_name']
                    thumbnail = s['poster_path']
                    link = s['id']
                    votes = s['vote_count']
                    rating = s['vote_average']
                    embed = discord.Embed()
                    embed.add_field(name=f'{title}', value=s['overview'][:1000])
                    embed.add_field(name=':star: **Rating\n**', value=f'{rating}\({votes} votes\)')
                    embed.add_field(name=':calendar_spiral: **Released\n**', value=s['first_air_date'])
                    embed.add_field(name=':paperclip: **Link\n**', value=f'[TMDb](https://www.themoviedb.org/tv/{link})')
                    embed.set_thumbnail(url=f'https://image.tmdb.org/t/p/original{thumbnail}')
                    await message.edit(embed=embed)
                    m += 1
                    await message.add_reaction(u"\u27A1")
                    await message.add_reaction(u"\u274C")
                    emote = [u"\u27A1", u"\u274C"]
                    try:
                        def check(reaction, user):
                            return (reaction.message.id == message.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                        if str(reaction) == u"\u27A1":
                            await message.remove_reaction(u"\u27A1", user)
                            continue
                        elif str(reaction) == u"\u274C":
                            await message.delete()
                            return
                    except asyncio.TimeoutError:
                        user = bot.user
                        await message.remove_reaction(u"\u27A1", user)
                        await message.remove_reaction(u"\u274C", user)
                
                await message.remove_reaction(u"\u27A1", user)
                await message.remove_reaction(u"\u274C", user)      
                await asyncio.sleep(60)
                await message.delete()



                                         #GamesInfo


@bot.command()
async def freegames(ctx):
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
        api = EpicGamesStoreAPI()
        free_games = api.get_free_games()['data']['Catalog']['searchStore']['elements']
        message = await ctx.send('Searching...')
        for game in free_games:
            game_name = game['title']
            game_thumbnail = None
            for image in game['keyImages']:
                if image['type'] == 'Thumbnail':
                    game_thumbnail = image['url']
            game_price = game['price']['totalPrice']['fmtPrice']['originalPrice']
            game_promotions = game['promotions']['promotionalOffers']
            upcoming_promotions = game['promotions']['upcomingPromotionalOffers']
            embed = discord.Embed(title=f'{game_name}', description='{} ({}) is FREE now.'.format(
                game_name, game_price
            ))
            embed.set_image(url=f'{game_thumbnail}')
            await message.edit(embed=embed)
            await message.add_reaction(u"\u27A1")
            await message.add_reaction(u"\u274C")
            emote = [u"\u27A1", u"\u274C"]
            try:
                def check(reaction, user):
                    return (reaction.message.id == message.id) and (user == ctx.message.author)  and (str(reaction) in emote)
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                if str(reaction) == u"\u27A1":
                    await message.remove_reaction(u"\u27A1", user)
                    continue
                elif str(reaction) == u"\u274C":
                    await message.delete()
                    return
            except asyncio.TimeoutError:
                user = bot.user
                await message.remove_reaction(u"\u27A1", user)
                await message.remove_reaction(u"\u274C", user)
        
        await message.remove_reaction(u"\u27A1", user)
        await message.remove_reaction(u"\u274C", user)      
        await asyncio.sleep(60)
        await message.delete()


                                          #Games & Fun


@bot.command()
async def cup(ctx, *, coin=0):
    member = ctx.message.author
    with open('users.json', 'r') as f:
        users = json.load(f)
    coins = users[f'{member.id}']['coins']
    q = int(coins)
    l = int(coin)
    guild = bot.get_guild(661211931558019072)
    channels = ["♠┃gambling"]
    if str(ctx.channel) in channels:
        if coin == 0:
            await ctx.send('Game starts with atleast 200 coins')
            return
        elif l < 200:
            await ctx.send('Game starts with atleast 200 coins')
            return
        elif q < l:
            await ctx.send('Not enough coins to  game starts with atleast 200 coins')
            return    
        else:
            member = ctx.message.author
            with open('users.json', 'r') as f:
                users = json.load(f)
            coins = users[f'{member.id}']['coins']
            a = int(coins)
            c = a-l
            users[f'{member.id}']['coins'] = c
            
            with open('users.json', 'w') as f:
                json.dump(users, f)
                
            ans = ['1', '2', '3']
            p = random.choice(ans)
            embed=discord.Embed(title='Find the coin', description='1 <:cupdown:767373888371425283>      2 <:cupdown:767373888371425283>      3 <:cupdown:767373888371425283>')
            await ctx.send(embed=embed)
            msg = await bot.wait_for('message', check=lambda message: message.author == member)
            uans = (msg.content)
            if uans == p:
                j = (l*2)
                with open('users.json', 'r') as o:
                    users = json.load(o)
                coins = users[f'{member.id}']['coins']
                a = int(coins)
                c = a+j
                n = str(c)
                users[f'{member.id}']['coins'] = c
                
                with open('users.json', 'w') as o:
                    json.dump(users, o)

                e=discord.Embed(description=f':tada: You won {j}  :coin:')
                await ctx.send(embed=e)
            else:
                await ctx.send(f'Wrong the right answer was {p} <:cupup:767373971137101886> :coin:')
                


@bot.command()
async def toss(ctx, *, coin=0):
    member = ctx.message.author
    with open('users.json', 'r') as f:
        users = json.load(f)
    coins = users[f'{member.id}']['coins']
    q = int(coins)
    l = int(coin)
    guild = bot.get_guild(661211931558019072)
    channels = ["♠┃gambling"]
    if str(ctx.channel) in channels:
        if l == 0:
            embed = discord.Embed(title='Usage', description='.toss amount')
            await ctx.send(embed=embed)
            return
        elif q < l:
            await ctx.send('Not enough coins to play this game')
            return    
        else:
            member = ctx.message.author
            with open('users.json', 'r') as f:
                users = json.load(f)
            coins = users[f'{member.id}']['coins']
            a = int(coins)
            c = a-l
            users[f'{member.id}']['coins'] = c
            
            with open('users.json', 'w') as f:
                json.dump(users, f)
                
            ans = ['1', '2']
            p = random.choice(ans)
            embed=discord.Embed(description=':coin: Write the number not the name\n\n(1)Heads\n(2)Tails')
            await ctx.send(embed=embed)
            msg = await bot.wait_for('message', check=lambda message: message.author == member)
            uans = (msg.content)
            if uans == p:
                j = (l*2)
                with open('users.json', 'r') as o:
                    users = json.load(o)
                coins = users[f'{member.id}']['coins']
                a = int(coins)
                c = a+j
                users[f'{member.id}']['coins'] = c
                
                with open('users.json', 'w') as o:
                    json.dump(users, o)

                e=discord.Embed(description=f':tada: You won {j}  :coin:')
                await ctx.send(embed=e)
            else:
                if p == '1':
                    p = 'Heads'
                elif p == '2':
                    p = 'Tails'
                await ctx.send(f'Sorry it was :coin: {p}')
                                
                
@bot.command()
async def dice(ctx, *, coin=0):
    member = ctx.message.author
    with open('users.json', 'r') as f:
        users = json.load(f)
    coins = users[f'{member.id}']['coins']
    q = int(coins)
    l = int(coin)
    guild = bot.get_guild(661211931558019072)
    channels = ["♠┃gambling"]
    if str(ctx.channel) in channels:
        if l == 0:
            embed = discord.Embed(title='Usage', description='.dice amount\nMinimum = 100\nMaximum = 10000')
            await ctx.send(embed=embed)
            return
        elif q < l:
            await ctx.send('Not enough coins to play this game')
            return    
        elif l < 100:
            await ctx.send('Minimum = 100')
            return
        elif l > 10000:
            await ctx.send('Maximum = 10000')
            return
        else:
            member = ctx.message.author
            with open('users.json', 'r') as f:
                users = json.load(f)
            coins = users[f'{member.id}']['coins']
            a = int(coins)
            c = a-l
            users[f'{member.id}']['coins'] = c
            
            with open('users.json', 'w') as f:
                json.dump(users, f)
                
            ans = [u"\u2680", u"\u2681", u"\u2682", u"\u2683", u"\u2684", u"\u2685"]
            p = random.choice(ans)
            pa = random.choice(ans)
            pe = random.choice(ans)
            bp = random.choice(ans)
            bpa = random.choice(ans)
            bpe = random.choice(ans)
            embed=discord.Embed(title='Chinchirorin', description=':game_die: :game_die: :game_die:\n\n**Rolling**')
            await ctx.send(embed=embed)
            time.sleep(1)               
            if p != '1' and p == pa and p == pe:
                j = (l*3)
                with open('users.json', 'r') as o:
                    users = json.load(o)
                coins = users[f'{member.id}']['coins']
                a = int(coins)
                c = a+j
                users[f'{member.id}']['coins'] = c
                
                with open('users.json', 'w') as o:
                    json.dump(users, o)

                e=discord.Embed(description=f':tada: You won {j}  :coin:  you got {p} {pa} {pe}')
                await ctx.send(embed=e)
            elif p == pa and p != pe:
                if bp == bpa and bp != bpe:
                    embed = discord.Embed()
                    embed.add_field(name='Result', value=f'Your score is {pe}\n{p} {pa} {pe}')
                    embed.add_field(name='Result', value=f'Bot\'s score is {bpe}\n{bp} {bpa} {bpe}')
                    await ctx.send(embed=embed)
                    if bpe > pe:
                        j = l
                        with open('users.json', 'r') as o:
                            users = json.load(o)

                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a-j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Lost', value=f'You lost {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bpe < pe:
                        j = (l*2)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Won', value=f':tada: You Won {j} :coin:')
                        await ctx.send(embed=ee)                     
                    elif bpe == pe:
                        i = (l/10)
                        j = (l+i)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                        ee = discord.Embed()
                        ee.add_field(name='Draw', value=f'You got {j} :coin: back')
                        await ctx.send(embed=ee)
                elif bp == bpe and bp != bpa:
                    embed = discord.Embed()
                    embed.add_field(name='Result', value=f'Your score is {pe}\n{p} {pa} {pe}')
                    embed.add_field(name='Result', value=f'Bot\'s score is {bpa}\n{bp} {bpa} {bpe}')
                    await ctx.send(embed=embed)
                    if bpa > pe:
                        j = l
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a-j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Lost', value=f'You lost {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bpa < pe:
                        j = (l*2)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Won', value=f':tada: You Won {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bpa == pe:
                        i = (l/10)
                        j = (l+i)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                    
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                        ee = discord.Embed()
                        ee.add_field(name='Draw', value=f'You got {j} :coin: back')
                        await ctx.send(embed=ee)
                elif bpa == bpe and bp != bpa:
                    embed = discord.Embed()
                    embed.add_field(name='Result', value=f'Your score is {pe}\n{p} {pa} {pe}')
                    embed.add_field(name='Result', value=f'Bot\'s score is {bp}\n{bp} {bpa} {bpe}')
                    await ctx.send(embed=embed)
                    if bp > pe:
                        j = l
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a-j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Lost', value=f'You lost {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bp < pe:
                        j = (l*2)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Won', value=f':tada: You Won {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bp == pe:
                        i = (l/10)
                        j = (l+i)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                        ee = discord.Embed()
                        ee.add_field(name='Draw', value=f'You got {j} :coin: back')
                        await ctx.send(embed=ee)
                elif bp != bpa and bp != bpe:
                    embed = discord.Embed()
                    embed.add_field(name='Result', value=f'Your score is {pe}\n{p} {pa} {pe}')
                    embed.add_field(name='Result', value=f'Bot\'s score is 0\n{bp} {bpa} {bpe}')
                    await ctx.send(embed=embed)
                    m = (l/2)
                    q = (l+m)
                    j = int(q)
                    with open('users.json', 'r') as o:
                        users = json.load(o)
                    coins = users[f'{member.id}']['coins']
                    a = int(coins)
                    c = a+j
                    users[f'{member.id}']['coins'] = c
                                    
                    with open('users.json', 'w') as o:
                        json.dump(users, o)
                                        
                    ee = discord.Embed()
                    ee.add_field(name='Won', value=f':tada: You Won {j} :coin:')
                    await ctx.send(embed=ee)
            elif p == pe and p != pa:
                if bp == bpe and bp != bpa:
                    embed = discord.Embed()
                    embed.add_field(name='Result', value=f'Your score is {pa}\n{p} {pa} {pe}')
                    embed.add_field(name='Result', value=f'Bot\'s score is {bpa}\n{bp} {bpa} {bpe}')
                    await ctx.send(embed=embed)
                    if bpa > pa:
                        j = l
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a-j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Lost', value=f'You lost {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bpa < pa:
                        j = (l*2)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Won', value=f':tada: You Won {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bpa == pa:
                        i = (l/10)
                        j = (l+i)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                        ee = discord.Embed()
                        ee.add_field(name='Draw', value=f'You got {j} :coin: back')
                        await ctx.send(embed=ee)
                elif bp == bpa and bp != bpe:
                    embed = discord.Embed()
                    embed.add_field(name='Result', value=f'Your score is {pa}\n{p} {pa} {pe}')
                    embed.add_field(name='Result', value=f'Bot\'s score is {bpe}\n{bp} {bpa} {bpe}')
                    await ctx.send(embed=embed)
                    if bpe > pa:
                        j = l
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a-j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Lost', value=f'You lost {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bpe < pa:
                        j = (l*2)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Won', value=f':tada: You Won {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bpe == pa:
                        i = (l/10)
                        j = (l+i)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                        ee = discord.Embed()
                        ee.add_field(name='Draw', value=f'You got {j} :coin: back')
                        await ctx.send(embed=ee)
                elif bpa == bpe and bp != bpa:
                    embed = discord.Embed()
                    embed.add_field(name='Result', value=f'Your score is {pa}\n{p} {pa} {pe}')
                    embed.add_field(name='Result', value=f'Bot\'s score is {bp}\n{bp} {bpa} {bpe}')
                    await ctx.send(embed=embed)
                    if bp > pa:
                        j = l
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a-j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Lost', value=f'You lost {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bp < pa:
                        j = (l*2)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Won', value=f':tada: You Won {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bp == pa:
                        i = (l/10)
                        j = (l+i)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                        ee = discord.Embed()
                        ee.add_field(name='Draw', value=f'You got {j} :coin: back')
                        await ctx.send(embed=ee)
                elif bp != bpa and bp != bpe:
                    embed = discord.Embed()                                                   
                    embed.add_field(name='Result', value=f'Your score is {pa}\n{p} {pa} {pe}')
                    embed.add_field(name='Result', value=f'Bot\'s score is 0\n{bp} {bpa} {bpe}')
                    await ctx.send(embed=embed)
                    m = (l/2)
                    q = (l+m)
                    j = int(q)
                    with open('users.json', 'r') as o:
                        users = json.load(o)
                    coins = users[f'{member.id}']['coins']
                    a = int(coins)
                    c = a+j
                    users[f'{member.id}']['coins'] = c
                                    
                    with open('users.json', 'w') as o:
                        json.dump(users, o)
                                        
                    ee = discord.Embed()
                    ee.add_field(name='Won', value=f':tada: You Won {j} :coin:')
                    await ctx.send(embed=ee)
            elif pa == pe and p != pa:
                if bpa == bpe and bp != bpa:
                    embed = discord.Embed()
                    embed.add_field(name='Result', value=f'Your score is {p}\n{p} {pa} {pe}')
                    embed.add_field(name='Result', value=f'Bot\'s score is {bp}\n{bp} {bpa} {bpe}')
                    await ctx.send(embed=embed)
                    if bp > p:
                        j = l
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a-j
                        users[f'{member.id}']['coins'] = c
            
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Lost', value=f'You lost {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bp < p:
                        j = (l*2)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Won', value=f':tada: You Won {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bp == p:
                        i = (l/10)
                        j = (l+i)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                        ee = discord.Embed()
                        ee.add_field(name='Draw', value=f'You got {j} :coin: back')
                        await ctx.send(embed=ee)
                elif bp == bpa and bp != bpe:
                    embed = discord.Embed()
                    embed.add_field(name='Result', value=f'Your score is {p}\n{p} {pa} {pe}')
                    embed.add_field(name='Result', value=f'Bot\'s score is {bpe}\n{bp} {bpa} {bpe}')
                    await ctx.send(embed=embed)
                    if bpe > p:
                        j = l
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a-j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Lost', value=f'You lost {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bpe < p:
                        j = (l*2)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Won', value=f':tada: You Won {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bpe == p:
                        i = (l/10)
                        j = (l+i)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                        ee = discord.Embed()
                        ee.add_field(name='Draw', value=f'You got {j} :coin: back')
                        await ctx.send(embed=ee)
                elif bp == bpe and bp != bpa:
                    embed = discord.Embed()
                    embed.add_field(name='Result', value=f'Your score is {p}\n{p} {pa} {pe}')
                    embed.add_field(name='Result', value=f'Bot\'s score is {bpa}\n{bp} {bpa} {bpe}')
                    await ctx.send(embed=embed)
                    if bpa > p:
                        j = l
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a-j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Lost', value=f'You lost {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bpa < p:
                        j = (l*2)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        ee = discord.Embed()
                        ee.add_field(name='Won', value=f':tada: You Won {j} :coin:')
                        await ctx.send(embed=ee)
                    elif bpa == p:
                        i = (l/10)
                        j = (l+i)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                        ee = discord.Embed()
                        ee.add_field(name='Draw', value=f'You got {j} :coin: back')
                        await ctx.send(embed=ee)
                elif bp != bpa and bp != bpe:
                    embed = discord.Embed()                                          
                    embed.add_field(name='Result', value=f'Your score is {p}\n{p} {pa} {pe}')
                    embed.add_field(name='Result', value=f'Bot\'s score is 0\n{bp} {bpa} {bpe}')
                    await ctx.send(embed=embed)
                    m = (l/2)
                    q = (l+m)
                    j = int(q)
                    with open('users.json', 'r') as o:
                        users = json.load(o)
                    coins = users[f'{member.id}']['coins']
                    a = int(coins)
                    c = a+j
                    users[f'{member.id}']['coins'] = c
                
                    with open('users.json', 'w') as o:
                        json.dump(users, o)

                    ee = discord.Embed()
                    ee.add_field(name='Won', value=f':tada: You Won {j} :coin:')
                    await ctx.send(embed=ee)
            elif p != pa and p != pe and pa != pe:
                if bp != bpa and bp != bpe and bpa != bpe:
                    j = l
                    with open('users.json', 'r') as o:
                        users = json.load(o)
                    coins = users[f'{member.id}']['coins']
                    a = int(coins)
                    c = a+j
                    users[f'{member.id}']['coins'] = c
                
                    with open('users.json', 'w') as o:
                        json.dump(users, o)
                    
                    ee = discord.Embed()
                    ee.add_field(name='Result', value=f'Your score is 0\n{p} {pa} {pe}')
                    ee.add_field(name='Result', value=f'Bot\'s score is 0\n{bp} {bpa} {bpe}')
                    ee.add_field(name='Draw', value=f'You got {j} :coin: back')
                    await ctx.send(embed=ee)
                elif bpa == bpe and bp != bpa:
                    j = l
                    ee = discord.Embed()
                    ee.add_field(name='Result', value=f'Your score is 0\n{p} {pa} {pe}')
                    ee.add_field(name='Result', value=f'Bot\'s score is {bp}\n{bp} {bpa} {bpe}')
                    ee.add_field(name='Lost', value=f'You lost {j} :coin:')
                    await ctx.send(embed=ee)
                elif bp == bpe and bp != bpa:
                    j = l
                    ee = discord.Embed()
                    ee.add_field(name='Result', value=f'Your score is 0\n{p} {pa} {pe}')
                    ee.add_field(name='Result', value=f'Bot\'s score is {bpa}\n{bp} {bpa} {bpe}')
                    ee.add_field(name='Lost', value=f'You lost {j} :coin:')
                    await ctx.send(embed=ee)
                elif bp == bpa and bp != bpe:
                    j = l
                    ee = discord.Embed()
                    ee.add_field(name='Result', value=f'Your score is 0\n{p} {pa} {pe}')
                    ee.add_field(name='Result', value=f'Bot\'s score is {bpe}\n{bp} {bpa} {bpe}')
                    ee.add_field(name='Lost', value=f'You lost {j} :coin:')
                    await ctx.send(embed=ee)
            elif p == '1' and p == pe and p == pa:
                j = (l*3)
                with open('users.json', 'r') as o:
                    users = json.load(o)
                coins = users[f'{member.id}']['coins']
                a = int(coins)
                c = a-j
                users[f'{member.id}']['coins'] = c
                
                with open('users.json', 'w') as o:
                    json.dump(users, o)
                ee = discord.Embed()
                ee.add_field(name='Lost', value=f'You got {p} {pa} {pe} that means you lost {j} :coin:')
                await ctx.send(embed=ee)


                
@bot.command()
async def bj(ctx, *, coin=0):
    member = ctx.message.author
    with open('users.json', 'r') as f:
        users = json.load(f)
    coins = users[f'{member.id}']['coins']
    q = int(coins)
    l = int(coin)
    guild = bot.get_guild(661211931558019072)
    channels = ["♠┃gambling"]
    if str(ctx.channel) in channels:
        if l == 0:
            embed = discord.Embed(title='Usage', description='.bj amount')
            await ctx.send(embed=embed)
            return
        elif q < l:
            await ctx.send('Not enough coins to play this game')
            return    
        else:
            member = ctx.message.author
            with open('users.json', 'r') as f:
                users = json.load(f)
            coins = users[f'{member.id}']['coins']
            a = int(coins)
            c = a-l
            users[f'{member.id}']['coins'] = c
            
            with open('users.json', 'w') as f:
                json.dump(users, f)
                
            cards = {
                        '<:s1:768850367299059743>' : '1', '<:s2:768850837103312956>' : '2', '<:s3:768850899945783306>' : '3', '<:s4:768850944372506634>' : '4', '<:s5:768850999716085821>' : '5', '<:s6:768851264653492255>' : '6', '<:s7:768851446183231518>' : '7', '<:s8:768851501752778752>' : '8', '<:s9:768851558246907925>' : '9', '<:s10:768851614265770027>' : '10', '<:s11:768852890164133899>' : '10', '<:s12:768853368591482920>' : '10', '<:s13:768853449676292126>' : '10',
                        '<:c1:769137965011173407>' : '1', '<:c2:769138045060120577>' : '2', '<:c3:769138140018769931>' : '3', '<:c4:769138233425526785>' : '4', '<:c5:769138319527116801>' : '5', '<:c6:769138409284436009>' : '6', '<:c7:769139223072604160>' : '7', '<:c8:769139406170357761>' : '8', '<:c9:769139511980458014>' : '9', '<:c10:769139572524187668>' : '10', '<:c11:769139639369334785>' : '10', '<:c12:769139714094661652>' : '10', '<:c13:769139782579257364>' : '10',
                        '<:h1:769134733854244874>' : '1', '<:h2:769134834139922472>' : '2', '<:h3:769134950216630301>' : '3', '<:h4:769135040759201792>' : '4', '<:h5:769135134653153310>' : '5', '<:h6:769135246490075136>' : '6', '<:h7:769135338961502249>' : '7', '<:h8:769135437138231306>' : '8', '<:h9:769135546642726942>' : '9', '<:h10:769135637906980875>' : '10', '<:h11:769135928815517716>' : '10', '<:h12:769136041646096394>' : '10', '<:h13:769136141865189376>' : '10',
                        '<:d1:769136359847624714>' : '1', '<:d2:769136487895007232>' : '2', '<:d3:769136555746131968>' : '3', '<:d4:769136642572812319>' : '4', '<:d5:769136717218971658>' : '5', '<:d6:769136799213158400>' : '6', '<:d7:769136883267534848>' : '7', '<:d8:769136966981517312>' : '8', '<:d9:769137055779127297>' : '9', '<:d10:769137144878858280>' : '10', '<:d11:769137268505313320>' : '10', '<:d12:769137356518195240>' : '10', '<:d13:769137443286417428>' : '10'
                    }
            usercard1 = random.choice(list(cards.items()))
            usercard2 = random.choice(list(cards.items()))
            botcard1 = random.choice(list(cards.items()))
            a1 = int(usercard1[1])
            a2 = int(usercard2[1])
            b1 = int(botcard1[1])
            at0 = a1+a2
            embed = discord.Embed(title='Blackjack')
            embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
            embed.add_field(name=f'Dealer: {b1}', value=f'{botcard1[0]}')
            embed.set_footer(text='Hit or Stay')
            await ctx.send(embed=embed)
            msg = await bot.wait_for('message', check=lambda message: message.author == member)
            uans = (msg.content)
            if uans == 'Hit' or uans == 'hit':
                usercard3 = random.choice(list(cards.items()))
                a3 = int(usercard3[1])
                at1 = at0+a3
                if at1 > 21:
                    embed = discord.Embed(title='Blackjack')
                    embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                    embed.add_field(name=f'Dealer: {b1}', value=f'{botcard1[0]}')
                    embed.set_footer(text='Busted you lost')
                    await ctx.send(embed=embed)
                    return
                elif at1 == 21:
                    botcard2 = random.choice(list(cards.items()))
                    botcard3 = random.choice(list(cards.items()))
                    b2 = int(botcard2[1])
                    b3 = int(botcard3[1])
                    bt = b1+b2+b3
                    if bt < 21:
                        botcard4 = random.choice(list(cards.items()))                                                   
                        b4 = int(botcard4[1])
                        bt1 = bt+b4
                        if bt1 < 21:
                            botcard5 = random.choice(list(cards.items()))
                            b5 = int(botcard5[1])
                            bt2 = bt1+b5
                            if bt2 < 21:
                                embed = discord.Embed(title='Blackjack')
                                embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                                embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                embed.set_footer(text='You Won')
                                j = (l*2)
                                with open('users.json', 'r') as o:
                                    users = json.load(o)
                                coins = users[f'{member.id}']['coins']
                                a = int(coins)
                                c = a+j
                                users[f'{member.id}']['coins'] = c
                
                                with open('users.json', 'w') as o:
                                    json.dump(users, o)
                    
                                await ctx.send(embed=embed)
                                return
                            elif bt > 21:
                                embed = discord.Embed(title='Blackjack')
                                embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                                embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                embed.set_footer(text='Dealer busted you won')
                                j = (l*2)
                                with open('users.json', 'r') as o:
                                    users = json.load(o)
                                coins = users[f'{member.id}']['coins']
                                a = int(coins)
                                c = a+j
                                users[f'{member.id}']['coins'] = c
                
                                with open('users.json', 'w') as o:
                                    json.dump(users, o)
                    
                                await ctx.send(embed=embed)
                                return
                            elif bt == 21:
                                embed = discord.Embed(title='Blackjack')
                                embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                                embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                embed.set_footer(text='Draw')
                                j = l
                                with open('users.json', 'r') as o:
                                    users = json.load(o)
                                coins = users[f'{member.id}']['coins']
                                a = int(coins)
                                c = a+j
                                users[f'{member.id}']['coins'] = c
                
                                with open('users.json', 'w') as o:
                                    json.dump(users, o)

                            await ctx.send(embed=embed)
                            return
                        elif bt > 21:
                            embed = discord.Embed(title='Blackjack')
                            embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                            embed.add_field(name=f'Dealer: {bt1}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                            embed.set_footer(text='You Won')
                            j = (l*2)
                            with open('users.json', 'r') as o:
                                users = json.load(o)
                            coins = users[f'{member.id}']['coins']
                            a = int(coins)
                            c = a+j
                            users[f'{member.id}']['coins'] = c
                
                            with open('users.json', 'w') as o:
                                json.dump(users, o)
                    
                            await ctx.send(embed=embed)
                            return
                        elif bt == 21:
                            embed = discord.Embed(title='Blackjack')
                            embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                            embed.add_field(name=f'Dealer: {bt1}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                            embed.set_footer(text='Draw')
                            j = l
                            with open('users.json', 'r') as o:
                                users = json.load(o)
                            coins = users[f'{member.id}']['coins']
                            a = int(coins)
                            c = a+j
                            users[f'{member.id}']['coins'] = c
                
                            with open('users.json', 'w') as o:
                                json.dump(users, o)

                            await ctx.send(embed=embed)
                            return
                    elif bt > 21:
                        embed = discord.Embed(title='Blackjack')
                        embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                        embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                        embed.set_footer(text='You Won')
                        j = (l*2)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        await ctx.send(embed=embed)
                        return
                    elif bt == 21:
                        embed = discord.Embed(title='Blackjack')
                        embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                        embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                        embed.set_footer(text='Draw')
                        j = l
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                        
                        await ctx.send(embed=embed)
                        return
                elif at1 < 21:
                    embed = discord.Embed(title='Blackjack')
                    embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                    embed.add_field(name=f'Dealer: {b1}', value=f'{botcard1[0]}')
                    embed.set_footer(text='Hit or Stay')
                    await ctx.send(embed=embed)
                    msg = await bot.wait_for('message', check=lambda message: message.author == member)
                    uans = (msg.content)
                    if uans == 'Hit' or uans == 'hit':
                        usercard4 = random.choice(list(cards.items()))
                        a4 = int(usercard4[1])
                        at2 = at1+a4
                        if at2 > 21:
                            embed = discord.Embed(title='Blackjack')
                            embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                            embed.add_field(name=f'Dealer: {b1}', value=f'{botcard1[0]}')
                            embed.set_footer(text='Busted you lost')
                            await ctx.send(embed=embed)
                            return
                        elif at2 == 21:
                            botcard2 = random.choice(list(cards.items()))
                            botcard3 = random.choice(list(cards.items()))
                            b2 = int(botcard2[1])
                            b3 = int(botcard3[1])
                            bt = b1+b2+b3
                            if bt < 21:
                                botcard4 = random.choice(list(cards.items()))                                                   
                                b4 = int(botcard4[1])
                                bt1 = bt+b4
                                if bt1 < 21:
                                    botcard5 = random.choice(list(cards.items()))
                                    b5 = int(botcard5[1])
                                    bt2 = bt1+b5
                                    if bt2 < 21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                        embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                        embed.set_footer(text='You Won')
                                        j = (l*2)
                                        with open('users.json', 'r') as o:
                                            users = json.load(o)
                                        coins = users[f'{member.id}']['coins']
                                        a = int(coins)
                                        c = a+j
                                        users[f'{member.id}']['coins'] = c
                
                                        with open('users.json', 'w') as o:
                                            json.dump(users, o)
                    
                                        await ctx.send(embed=embed)
                                        return
                                    elif bt > 21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                        embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                        embed.set_footer(text='You Won')
                                        j = (l*2)
                                        with open('users.json', 'r') as o:
                                            users = json.load(o)
                                        coins = users[f'{member.id}']['coins']
                                        a = int(coins)
                                        c = a+j
                                        users[f'{member.id}']['coins'] = c
                
                                        with open('users.json', 'w') as o:
                                            json.dump(users, o)
                    
                                        await ctx.send(embed=embed)
                                        return
                                    elif bt == 21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                        embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                        embed.set_footer(text='Draw')
                                        j = l
                                        with open('users.json', 'r') as o:
                                            users = json.load(o)
                                        coins = users[f'{member.id}']['coins']
                                        a = int(coins)
                                        c = a+j
                                        users[f'{member.id}']['coins'] = c
                
                                        with open('users.json', 'w') as o:
                                            json.dump(users, o)
                                        
                                        await ctx.send(embed=embed)
                                        return
                                elif bt > 21:
                                    embed = discord.Embed(title='Blackjack')
                                    embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                    embed.add_field(name=f'Dealer: {bt1}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                                    embed.set_footer(text='You Won')
                                    j = (l*2)
                                    with open('users.json', 'r') as o:
                                        users = json.load(o)
                                    coins = users[f'{member.id}']['coins']
                                    a = int(coins)
                                    c = a+j
                                    users[f'{member.id}']['coins'] = c
                
                                    with open('users.json', 'w') as o:
                                        json.dump(users, o)
                    
                                    await ctx.send(embed=embed)
                                    return
                                elif bt == 21:
                                    embed = discord.Embed(title='Blackjack')
                                    embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                    embed.add_field(name=f'Dealer: {bt1}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                                    embed.set_footer(text='Draw')
                                    j = l
                                    with open('users.json', 'r') as o:
                                        users = json.load(o)
                                    coins = users[f'{member.id}']['coins']
                                    a = int(coins)
                                    c = a+j
                                    users[f'{member.id}']['coins'] = c
                
                                    with open('users.json', 'w') as o:
                                        json.dump(users, o)
            
                                    await ctx.send(embed=embed)
                                    return
                            elif bt > 21:
                                embed = discord.Embed(title='Blackjack')
                                embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                                embed.set_footer(text='You Won')
                                j = (l*2)
                                with open('users.json', 'r') as o:
                                    users = json.load(o)
                                coins = users[f'{member.id}']['coins']
                                a = int(coins)
                                c = a+j
                                users[f'{member.id}']['coins'] = c
                
                                with open('users.json', 'w') as o:
                                    json.dump(users, o)
                    
                                await ctx.send(embed=embed)
                                return
                            elif bt == 21:
                                embed = discord.Embed(title='Blackjack')
                                embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                                embed.set_footer(text='Draw')
                                j = l
                                with open('users.json', 'r') as o:
                                    users = json.load(o)
                                coins = users[f'{member.id}']['coins']
                                a = int(coins)
                                c = a+j
                                users[f'{member.id}']['coins'] = c
                
                                with open('users.json', 'w') as o:
                                    json.dump(users, o)

                                await ctx.send(embed=embed)
                                return
                        elif at2 < 21:
                            embed = discord.Embed(title='Blackjack')
                            embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                            embed.add_field(name=f'Dealer: {b1}', value=f'{botcard1[0]}')
                            embed.set_footer(text='Hit or Stay')
                            await ctx.send(embed=embed)
                            msg = await bot.wait_for('message', check=lambda message: message.author == member)
                            uans = (msg.content)
                            if uans == 'Hit' or uans == 'hit':
                                usercard5 = random.choice(list(cards.items()))
                                a5 = int(usercard5[1])
                                at3 = at2+a5
                                if at3 > 21:
                                    embed = discord.Embed(title='Blackjack')
                                    embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                    embed.add_field(name=f'Dealer: {b1}', value=f'{botcard1[0]}')
                                    embed.set_footer(text='Busted you lost')
                                    await ctx.send(embed=embed)
                                    return
                                elif at3 == 21:
                                    botcard2 = random.choice(list(cards.items()))
                                    botcard3 = random.choice(list(cards.items()))
                                    b2 = int(botcard2[1])
                                    b3 = int(botcard3[1])
                                    bt = b1+b2+b3
                                    if bt < 21:
                                        botcard4 = random.choice(list(cards.items()))                                                   
                                        b4 = int(botcard4[1])
                                        bt1 = bt+b4
                                        if bt1 < 21:
                                            botcard5 = random.choice(list(cards.items()))
                                            b5 = int(botcard5[1])
                                            bt2 = bt1+b5
                                            if bt2 < 21:
                                                embed = discord.Embed(title='Blackjack')
                                                embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                                embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                                embed.set_footer(text='You Won')
                                                j = (l*2)
                                                with open('users.json', 'r') as o:
                                                    users = json.load(o)
                                                coins = users[f'{member.id}']['coins']
                                                a = int(coins)
                                                c = a+j
                                                users[f'{member.id}']['coins'] = c
                
                                                with open('users.json', 'w') as o:
                                                    json.dump(users, o)
                    
                                                await ctx.send(embed=embed)
                                                return
                                            elif bt > 21:
                                                embed = discord.Embed(title='Blackjack')
                                                embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                                embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                                embed.set_footer(text='You Won')
                                                j = (l*2)
                                                with open('users.json', 'r') as o:
                                                    users = json.load(o)
                                                coins = users[f'{member.id}']['coins']
                                                a = int(coins)
                                                c = a+j
                                                users[f'{member.id}']['coins'] = c
                
                                                with open('users.json', 'w') as o:
                                                    json.dump(users, o)
                    
                                                await ctx.send(embed=embed)
                                                return
                                            elif bt == 21:
                                                embed = discord.Embed(title='Blackjack')
                                                embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                                embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                                embed.set_footer(text='Draw')
                                                j = l
                                                with open('users.json', 'r') as o:
                                                    users = json.load(o)
                                                coins = users[f'{member.id}']['coins']
                                                a = int(coins)
                                                c = a+j
                                                users[f'{member.id}']['coins'] = c
                
                                                with open('users.json', 'w') as o:
                                                    json.dump(users, o)
                                        
                                                await ctx.send(embed=embed)
                                                return
                                        elif bt > 21:
                                            embed = discord.Embed(title='Blackjack')
                                            embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                            embed.add_field(name=f'Dealer: {bt1}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                                            embed.set_footer(text='You Won')
                                            j = (l*2)
                                            with open('users.json', 'r') as o:
                                                users = json.load(o)
                                            coins = users[f'{member.id}']['coins']
                                            a = int(coins)
                                            c = a+j
                                            users[f'{member.id}']['coins'] = c
                
                                            with open('users.json', 'w') as o:
                                                json.dump(users, o)
                    
                                            await ctx.send(embed=embed)
                                            return
                                        elif bt == 21:
                                            embed = discord.Embed(title='Blackjack')
                                            embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                            embed.add_field(name=f'Dealer: {bt1}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                                            embed.set_footer(text='Draw')
                                            j = l
                                            with open('users.json', 'r') as o:
                                                users = json.load(o)
                                            coins = users[f'{member.id}']['coins']
                                            a = int(coins)
                                            c = a+j
                                            users[f'{member.id}']['coins'] = c
                
                                            with open('users.json', 'w') as o:
                                                json.dump(users, o)
            
                                            await ctx.send(embed=embed)
                                            return
                                    elif bt > 21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                        embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                                        embed.set_footer(text='You Won')
                                        j = (l*2)
                                        with open('users.json', 'r') as o:
                                            users = json.load(o)
                                        coins = users[f'{member.id}']['coins']
                                        a = int(coins)
                                        c = a+j
                                        users[f'{member.id}']['coins'] = c
                
                                        with open('users.json', 'w') as o:
                                            json.dump(users, o)
                    
                                        await ctx.send(embed=embed)
                                        return
                                    elif bt == 21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                        embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                                        embed.set_footer(text='Draw')
                                        j = l
                                        with open('users.json', 'r') as o:
                                            users = json.load(o)
                                        coins = users[f'{member.id}']['coins']
                                        a = int(coins)
                                        c = a+j
                                        users[f'{member.id}']['coins'] = c
                
                                        with open('users.json', 'w') as o:
                                            json.dump(users, o)

                                        await ctx.send(embed=embed)
                                        return
                                elif at2 < 21:  
                                    embed = discord.Embed(title='Blackjack')
                                    embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                    embed.add_field(name=f'Dealer: {b1}', value=f'{botcard1[0]}')
                                    await ctx.send(embed=embed)
                                    await asyncio.sleep(1)
                                    if b1 > at3:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                        embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]}')
                                        embed.set_footer(text='You Lost')
                                        await ctx.send(embed=embed)
                                        return
                                    botcard2 = random.choice(list(cards.items()))
                                    b2 = int(botcard2[1])
                                    bt = b1+b2
                                    if bt > at3 and bt <=21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                        embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]}')
                                        embed.set_footer(text='You Lost')
                                        await ctx.send(embed=embed)        
                                        return
                                    elif bt <= at3:
                                        botcard3 = random.choice(list(cards.items()))
                                        b3 = int(botcard3[1])
                                        bt1 = bt+b3
                                        if bt1 > at3 and bt1 <= 21:
                                            embed = discord.Embed(title='Blackjack')
                                            embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                            embed.add_field(name=f'Dealer: {bt1}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                                            embed.set_footer(text='You Lost')
                                            await ctx.send(embed=embed)
                                            return
                                        elif bt1 <= at3:
                                            botcard4 = random.choice(list(cards.items()))
                                            b4 = int(botcard4[1])
                                            bt2 = bt1+b4
                                            if bt2 > at3 and bt2 <= 21:
                                                embed = discord.Embed(title='Blackjack')
                                                embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                                embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                                                embed.set_footer(text='You Lost')
                                                await ctx.send(embed=embed)
                                                return
                                            elif bt2 <= at3:
                                                botcard5 = random.choice(list(cards.items()))
                                                b5 = int(botcard5[1])
                                                bt3 = bt2+b5
                                                if bt3 > at3 and bt3 <= 21:
                                                    embed = discord.Embed(title='Blackjack')
                                                    embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                                    embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                                    embed.set_footer(text='You Lost')
                                                    await ctx.send(embed=embed)
                                                    return
                                                elif bt3 < at3 and bt3 <=21:
                                                    embed = discord.Embed(title='Blackjack')
                                                    embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                                    embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                                    embed.set_footer(text='You Won')
                                                    j = (l*2)
                                                    with open('users.json', 'r') as o:
                                                        users = json.load(o)
                                                    coins = users[f'{member.id}']['coins']
                                                    a = int(coins)
                                                    c = a+j
                                                    users[f'{member.id}']['coins'] = c
                    
                                                    with open('users.json', 'w') as o:
                                                        json.dump(users, o)
                        
                                                    await ctx.send(embed=embed)
                                                    return
                                                elif bt3 == at3 and bt3 <=21:
                                                    embed = discord.Embed(title='Blackjack')
                                                    embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                                    embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                                    embed.set_footer(text='Draw')
                                                    j = l
                                                    with open('users.json', 'r') as o:
                                                        users = json.load(o)
                                                    coins = users[f'{member.id}']['coins']
                                                    a = int(coins)
                                                    c = a+j
                                                    users[f'{member.id}']['coins'] = c
                    
                                                    with open('users.json', 'w') as o:
                                                        json.dump(users, o)
            
                                                    await ctx.send(embed=embed)   
                                                    return
                                                elif bt3 > at3 and bt3 > 21:
                                                    embed = discord.Embed(title='Blackjack')
                                                    embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                                    embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                                    embed.set_footer(text='Dealer busted you won')
                                                    j = (l*2)
                                                    with open('users.json', 'r') as o:
                                                        users = json.load(o)
                                                    coins = users[f'{member.id}']['coins']
                                                    a = int(coins)
                                                    c = a+j
                                                    users[f'{member.id}']['coins'] = c
                            
                                                    with open('users.json', 'w') as o:
                                                        json.dump(users, o)
                                
                                                    await ctx.send(embed=embed)
                                                    return
                                            elif bt2 > at3 and bt2 > 21:
                                                embed = discord.Embed(title='Blackjack')
                                                embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                                embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                                                embed.set_footer(text='Dealer busted you won')
                                                j = (l*2)
                                                with open('users.json', 'r') as o:
                                                    users = json.load(o)
                                                coins = users[f'{member.id}']['coins']
                                                a = int(coins)
                                                c = a+j
                                                users[f'{member.id}']['coins'] = c
                            
                                                with open('users.json', 'w') as o:
                                                    json.dump(users, o)
                                
                                                await ctx.send(embed=embed)
                                                return
                                            elif bt2 == at3 and bt2 <= 21:
                                                botcard5 = random.choice(list(cards.items()))
                                                b5 = int(botcard5[1])
                                                bt3 = bt2+b5              
                                                if bt3 <= 21:
                                                    embed = discord.Embed(title='Blackjack')
                                                    embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                                    embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                                    embed.set_footer(text='You Lost')
                                                    await ctx.send(embed=embed)    
                                                    return    
                                        elif bt1 > at3 and bt1 > 21:
                                            embed = discord.Embed(title='Blackjack')
                                            embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                            embed.add_field(name=f'Dealer: {bt1}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                                            embed.set_footer(text='Dealer busted you won')
                                            j = (l*2)
                                            with open('users.json', 'r') as o:
                                                users = json.load(o)
                                            coins = users[f'{member.id}']['coins']
                                            a = int(coins)
                                            c = a+j
                                            users[f'{member.id}']['coins'] = c
                            
                                            with open('users.json', 'w') as o:
                                                json.dump(users, o)
                                
                                            await ctx.send(embed=embed)
                                            return
                                        elif bt1 == at3 and bt1 <= 21:
                                            botcard4 = random.choice(list(cards.items()))
                                            b4 = int(botcard4[1])
                                            bt2 = bt1+b4               
                                            if bt2 <= 21:
                                                embed = discord.Embed(title='Blackjack')
                                                embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                                embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                                                embed.set_footer(text='You Lost')
                                                await ctx.send(embed=embed)
                                                return
                                    elif bt > at3 and bt > 21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                        embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]}')
                                        embed.set_footer(text='Dealer busted you won')
                                        j = (l*2)
                                        with open('users.json', 'r') as o:
                                            users = json.load(o)
                                        coins = users[f'{member.id}']['coins']
                                        a = int(coins)
                                        c = a+j
                                        users[f'{member.id}']['coins'] = c
                            
                                        with open('users.json', 'w') as o:
                                            json.dump(users, o)
                                
                                        await ctx.send(embed=embed)
                                        return
                                    elif bt == at3 and bt <= 21:
                                        botcard3 = random.choice(list(cards.items()))
                                        b3 = int(botcard3[1])
                                        bt1 = bt+b3                
                                        if bt1 <= 21:
                                            embed = discord.Embed(title='Blackjack')
                                            embed.add_field(name=f'User: {at3}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]} {usercard5[0]}')
                                            embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                                            embed.set_footer(text='You Lost')
                                            await ctx.send(embed=embed)        
                                            return    
                            elif uans == 'Stay' or uans == 'stay':
                                if b1 > at2:
                                    embed = discord.Embed(title='Blackjack')
                                    embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                    embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]}')
                                    embed.set_footer(text='You Lost')
                                    await ctx.send(embed=embed)
                                    return
                                botcard2 = random.choice(list(cards.items()))
                                b2 = int(botcard2[1])
                                bt = b1+b2
                                if bt > at2 and bt <=21:
                                    embed = discord.Embed(title='Blackjack')
                                    embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                    embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]}')
                                    embed.set_footer(text='You Lost')
                                    await ctx.send(embed=embed)        
                                    return
                                elif bt <= at2:
                                    botcard3 = random.choice(list(cards.items()))
                                    b3 = int(botcard3[1])
                                    bt1 = bt+b3
                                    if bt1 > at2 and bt1 <= 21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                        embed.add_field(name=f'Dealer: {bt1}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                                        embed.set_footer(text='You Lost')
                                        await ctx.send(embed=embed)
                                        return
                                    elif bt1 <= at2:
                                        botcard4 = random.choice(list(cards.items()))
                                        b4 = int(botcard4[1])
                                        bt2 = bt1+b4
                                        if bt2 > at2 and bt2 <= 21:
                                            embed = discord.Embed(title='Blackjack')
                                            embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                            embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                                            embed.set_footer(text='You Lost')
                                            await ctx.send(embed=embed)
                                            return
                                        elif bt2 <= at2:
                                            botcard5 = random.choice(list(cards.items()))
                                            b5 = int(botcard5[1])
                                            bt3 = bt2+b5
                                            if bt3 > at2 and bt3 <= 21:
                                                embed = discord.Embed(title='Blackjack')
                                                embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                                embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                                embed.set_footer(text='You Lost')
                                                await ctx.send(embed=embed)
                                                return
                                            elif bt3 < at2 and bt3 <=21:
                                                embed = discord.Embed(title='Blackjack')
                                                embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                                embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                                embed.set_footer(text='You Won')
                                                j = (l*2)
                                                with open('users.json', 'r') as o:
                                                    users = json.load(o)
                                                coins = users[f'{member.id}']['coins']
                                                a = int(coins)
                                                c = a+j
                                                users[f'{member.id}']['coins'] = c
                
                                                with open('users.json', 'w') as o:
                                                    json.dump(users, o)
                    
                                                await ctx.send(embed=embed)
                                                return
                                            elif bt3 == at2 and bt3 <=21:
                                                embed = discord.Embed(title='Blackjack')
                                                embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                                embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                                embed.set_footer(text='Draw')
                                                j = l
                                                with open('users.json', 'r') as o:
                                                    users = json.load(o)
                                                coins = users[f'{member.id}']['coins']
                                                a = int(coins)
                                                c = a+j
                                                users[f'{member.id}']['coins'] = c
                
                                                with open('users.json', 'w') as o:
                                                    json.dump(users, o)
        
                                                await ctx.send(embed=embed)   
                                                return
                                            elif bt3 > at2 and bt3 > 21:
                                                embed = discord.Embed(title='Blackjack')
                                                embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                                embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                                embed.set_footer(text='Dealer busted you won')
                                                j = (l*2)
                                                with open('users.json', 'r') as o:
                                                    users = json.load(o)
                                                coins = users[f'{member.id}']['coins']
                                                a = int(coins)
                                                c = a+j
                                                users[f'{member.id}']['coins'] = c
                        
                                                with open('users.json', 'w') as o:
                                                    json.dump(users, o)
                            
                                                await ctx.send(embed=embed)
                                                return
                                        elif bt2 > at2 and bt2 > 21:
                                            embed = discord.Embed(title='Blackjack')
                                            embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                            embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                                            embed.set_footer(text='Dealer busted you won')
                                            j = (l*2)
                                            with open('users.json', 'r') as o:
                                                users = json.load(o)
                                            coins = users[f'{member.id}']['coins']
                                            a = int(coins)
                                            c = a+j
                                            users[f'{member.id}']['coins'] = c
                        
                                            with open('users.json', 'w') as o:
                                                json.dump(users, o)
                            
                                            await ctx.send(embed=embed)
                                            return
                                        elif bt2 == at2 and bt2 <= 21:
                                            botcard5 = random.choice(list(cards.items()))
                                            b5 = int(botcard5[1])
                                            bt3 = bt2+b5              
                                            if bt3 <= 21:
                                                embed = discord.Embed(title='Blackjack')
                                                embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                                embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                                embed.set_footer(text='You Lost')
                                                await ctx.send(embed=embed)    
                                                return    
                                    elif bt1 > at2 and bt1 > 21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                        embed.add_field(name=f'Dealer: {bt1}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                                        embed.set_footer(text='Dealer busted you won')
                                        j = (l*2)
                                        with open('users.json', 'r') as o:
                                            users = json.load(o)
                                        coins = users[f'{member.id}']['coins']
                                        a = int(coins)
                                        c = a+j
                                        users[f'{member.id}']['coins'] = c
                        
                                        with open('users.json', 'w') as o:
                                            json.dump(users, o)
                            
                                        await ctx.send(embed=embed)
                                        return
                                    elif bt1 == at2 and bt1 <= 21:
                                        botcard4 = random.choice(list(cards.items()))
                                        b4 = int(botcard4[1])
                                        bt2 = bt1+b4               
                                        if bt2 <= 21:
                                            embed = discord.Embed(title='Blackjack')
                                            embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                            embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                                            embed.set_footer(text='You Lost')
                                            await ctx.send(embed=embed)
                                            return
                                elif bt > at2 and bt > 21:
                                    embed = discord.Embed(title='Blackjack')
                                    embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                    embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]}')
                                    embed.set_footer(text='Dealer busted you won')
                                    j = (l*2)
                                    with open('users.json', 'r') as o:
                                        users = json.load(o)
                                    coins = users[f'{member.id}']['coins']
                                    a = int(coins)
                                    c = a+j
                                    users[f'{member.id}']['coins'] = c
                        
                                    with open('users.json', 'w') as o:
                                        json.dump(users, o)
                            
                                    await ctx.send(embed=embed)
                                    return
                                elif bt == at2 and bt <= 21:
                                    botcard3 = random.choice(list(cards.items()))
                                    b3 = int(botcard3[1])
                                    bt1 = bt+b3                
                                    if bt1 <= 21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at2}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]} {usercard4[0]}')
                                        embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                                        embed.set_footer(text='You Lost')
                                        await ctx.send(embed=embed)        
                                        return    

                                        
                    elif uans == 'Stay' or uans == 'stay':
                        if b1 > at1:
                            embed = discord.Embed(title='Blackjack')
                            embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                            embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]}')
                            embed.set_footer(text='You Lost')
                            await ctx.send(embed=embed)
                            return
                        botcard2 = random.choice(list(cards.items()))
                        b2 = int(botcard2[1])
                        bt = b1+b2
                        if bt > at1 and bt <=21:
                            embed = discord.Embed(title='Blackjack')
                            embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                            embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]}')
                            embed.set_footer(text='You Lost')
                            await ctx.send(embed=embed)        
                            return
                        elif bt <= at1:
                            botcard3 = random.choice(list(cards.items()))
                            b3 = int(botcard3[1])
                            bt1 = bt+b3
                            if bt1 > at1 and bt1 <= 21:
                                embed = discord.Embed(title='Blackjack')
                                embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                                embed.add_field(name=f'Dealer: {bt1}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                                embed.set_footer(text='You Lost')
                                await ctx.send(embed=embed)
                                return
                            elif bt1 <= at1:
                                botcard4 = random.choice(list(cards.items()))
                                b4 = int(botcard4[1])
                                bt2 = bt1+b4
                                if bt2 > at1 and bt2 <= 21:
                                    embed = discord.Embed(title='Blackjack')
                                    embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                                    embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                                    embed.set_footer(text='You Lost')
                                    await ctx.send(embed=embed)
                                    return
                                elif bt2 <= at1:
                                    botcard5 = random.choice(list(cards.items()))
                                    b5 = int(botcard5[1])
                                    bt3 = bt2+b5
                                    if bt3 > at1 and bt3 <= 21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                                        embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                        embed.set_footer(text='You Lost')
                                        await ctx.send(embed=embed)
                                        return
                                    elif bt3 < at1 and bt3 <=21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                                        embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                        embed.set_footer(text='You Won')
                                        j = (l*2)
                                        with open('users.json', 'r') as o:
                                            users = json.load(o)
                                        coins = users[f'{member.id}']['coins']
                                        a = int(coins)
                                        c = a+j
                                        users[f'{member.id}']['coins'] = c
                
                                        with open('users.json', 'w') as o:
                                            json.dump(users, o)
                    
                                        await ctx.send(embed=embed)
                                        return
                                    elif bt3 == at1 and bt3 <=21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                                        embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                        embed.set_footer(text='Draw')
                                        j = l
                                        with open('users.json', 'r') as o:
                                            users = json.load(o)
                                        coins = users[f'{member.id}']['coins']
                                        a = int(coins)
                                        c = a+j
                                        users[f'{member.id}']['coins'] = c
                
                                        with open('users.json', 'w') as o:
                                            json.dump(users, o)
        
                                        await ctx.send(embed=embed)   
                                        return
                                    elif bt3 > at1 and bt3 > 21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                                        embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                        embed.set_footer(text='Dealer busted you won')
                                        j = (l*2)
                                        with open('users.json', 'r') as o:
                                            users = json.load(o)
                                        coins = users[f'{member.id}']['coins']
                                        a = int(coins)
                                        c = a+j
                                        users[f'{member.id}']['coins'] = c
                
                                        with open('users.json', 'w') as o:
                                            json.dump(users, o)
                    
                                        await ctx.send(embed=embed)
                                        return
                                elif bt2 > at1 and bt2 > 21:
                                    embed = discord.Embed(title='Blackjack')
                                    embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                                    embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                                    embed.set_footer(text='Dealer busted you won')
                                    j = (l*2)
                                    with open('users.json', 'r') as o:
                                        users = json.load(o)
                                    coins = users[f'{member.id}']['coins']
                                    a = int(coins)
                                    c = a+j
                                    users[f'{member.id}']['coins'] = c
                
                                    with open('users.json', 'w') as o:
                                        json.dump(users, o)
                    
                                    await ctx.send(embed=embed)
                                    return
                                elif bt2 == at1 and bt2 <= 21:
                                    botcard5 = random.choice(list(cards.items()))
                                    b5 = int(botcard5[1])
                                    bt3 = bt2+b5              
                                    if bt3 <= 21:
                                        embed = discord.Embed(title='Blackjack')
                                        embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                                        embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                        embed.set_footer(text='You Lost')
                                        await ctx.send(embed=embed)    
                                        return    
                            elif bt1 > at1 and bt1 > 21:
                                embed = discord.Embed(title='Blackjack')
                                embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                                embed.add_field(name=f'Dealer: {bt1}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                                embed.set_footer(text='Dealer busted you won')
                                j = (l*2)
                                with open('users.json', 'r') as o:
                                    users = json.load(o)
                                coins = users[f'{member.id}']['coins']
                                a = int(coins)
                                c = a+j
                                users[f'{member.id}']['coins'] = c
                
                                with open('users.json', 'w') as o:
                                    json.dump(users, o)
                    
                                await ctx.send(embed=embed)
                                return
                            elif bt1 == at1 and bt1 <= 21:
                                botcard4 = random.choice(list(cards.items()))
                                b4 = int(botcard4[1])
                                bt2 = bt1+b4               
                                if bt2 <= 21:
                                    embed = discord.Embed(title='Blackjack')
                                    embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                                    embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                                    embed.set_footer(text='You Lost')
                                    await ctx.send(embed=embed)
                                    return
                        elif bt > at1 and bt > 21:
                            embed = discord.Embed(title='Blackjack')
                            embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                            embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]}')
                            embed.set_footer(text='Dealer busted you won')
                            j = (l*2)
                            with open('users.json', 'r') as o:
                                users = json.load(o)
                            coins = users[f'{member.id}']['coins']
                            a = int(coins)
                            c = a+j
                            users[f'{member.id}']['coins'] = c
                
                            with open('users.json', 'w') as o:
                                json.dump(users, o)
                    
                            await ctx.send(embed=embed)
                            return
                        elif bt == at1 and bt <= 21:
                            botcard3 = random.choice(list(cards.items()))
                            b3 = int(botcard3[1])
                            bt1 = bt+b3                
                            if bt1 <= 21:
                                embed = discord.Embed(title='Blackjack')
                                embed.add_field(name=f'User: {at1}', value=f'{usercard1[0]} {usercard2[0]} {usercard3[0]}')
                                embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                                embed.set_footer(text='You Lost')
                                await ctx.send(embed=embed)        
                                return    
            elif uans == 'Stay' or uans == 'stay':
                if b1 > at0:
                    embed = discord.Embed(title='Blackjack')
                    embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
                    embed.add_field(name=f'Dealer: {b1}', value=f'{botcard1[0]}')
                    embed.set_footer(text='You Lost')
                    await ctx.send(embed=embed)
                    return
                botcard2 = random.choice(list(cards.items()))
                b2 = int(botcard2[1])
                bt = b1+b2
                if bt > at0 and bt <=21:
                    embed = discord.Embed(title='Blackjack')
                    embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
                    embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]}')
                    embed.set_footer(text='You Lost')
                    await ctx.send(embed=embed)        
                    return
                elif bt <= at0:
                    botcard3 = random.choice(list(cards.items()))
                    b3 = int(botcard3[1])
                    bt1 = bt+b3
                    if bt1 > at0 and bt1 <= 21:
                        embed = discord.Embed(title='Blackjack')
                        embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
                        embed.add_field(name=f'Dealer: {bt1}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                        embed.set_footer(text='You Lost')
                        await ctx.send(embed=embed)
                        return
                    elif bt1 <= at0:
                        botcard4 = random.choice(list(cards.items()))
                        b4 = int(botcard4[1])
                        bt2 = bt1+b4
                        if bt2 > at0 and bt2 <= 21:
                            embed = discord.Embed(title='Blackjack')
                            embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
                            embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                            embed.set_footer(text='You Lost')
                            await ctx.send(embed=embed)
                            return
                        elif bt2 <= at0:
                            botcard5 = random.choice(list(cards.items()))
                            b5 = int(botcard5[1])
                            bt3 = bt2+b5
                            if bt3 > at0 and bt3 <= 21:
                                embed = discord.Embed(title='Blackjack')
                                embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
                                embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                embed.set_footer(text='You Lost')
                                await ctx.send(embed=embed)
                            elif bt3 < at0 and bt3 <=21:
                                embed = discord.Embed(title='Blackjack')
                                embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
                                embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                embed.set_footer(text='You Won')
                                j = (l*2)
                                with open('users.json', 'r') as o:
                                    users = json.load(o)
                                coins = users[f'{member.id}']['coins']
                                a = int(coins)
                                c = a+j
                                users[f'{member.id}']['coins'] = c
                
                                with open('users.json', 'w') as o:
                                    json.dump(users, o)
                    
                                await ctx.send(embed=embed)
                                return
                            elif bt3 == at0 and bt3 <=21:
                                embed = discord.Embed(title='Blackjack')
                                embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
                                embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                embed.set_footer(text='Draw')
                                j = l
                                with open('users.json', 'r') as o:
                                    users = json.load(o)
                                coins = users[f'{member.id}']['coins']
                                a = int(coins)
                                c = a+j
                                users[f'{member.id}']['coins'] = c
                
                                with open('users.json', 'w') as o:
                                    json.dump(users, o)
        
                                await ctx.send(embed=embed)   
                                return
                            elif bt3 > at0 and bt3 > 21:
                                embed = discord.Embed(title='Blackjack')
                                embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
                                embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                embed.set_footer(text='Dealer busted you won')
                                j = (l*2)
                                with open('users.json', 'r') as o:
                                    users = json.load(o)
                                coins = users[f'{member.id}']['coins']
                                a = int(coins)
                                c = a+j
                                users[f'{member.id}']['coins'] = c
                
                                with open('users.json', 'w') as o:
                                    json.dump(users, o)
                    
                                await ctx.send(embed=embed)
                                return
                        elif bt2 > at0 and bt2 > 21:
                            embed = discord.Embed(title='Blackjack')
                            embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
                            embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                            embed.set_footer(text='Dealer busted you won')
                            j = (l*2)
                            with open('users.json', 'r') as o:
                                users = json.load(o)
                            coins = users[f'{member.id}']['coins']
                            a = int(coins)
                            c = a+j
                            users[f'{member.id}']['coins'] = c
                
                            with open('users.json', 'w') as o:
                                json.dump(users, o)
                    
                            await ctx.send(embed=embed)
                            return
                        elif bt2 == at0 and bt2 <= 21:
                            botcard5 = random.choice(list(cards.items()))
                            b5 = int(botcard5[1])
                            bt3 = bt2+b5              
                            if bt3 <= 21:
                                embed = discord.Embed(title='Blackjack')
                                embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
                                embed.add_field(name=f'Dealer: {bt3}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]} {botcard5[0]}')
                                embed.set_footer(text='You Lost')
                                await ctx.send(embed=embed)        
                    elif bt1 > at0 and bt1 > 21:
                        embed = discord.Embed(title='Blackjack')
                        embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
                        embed.add_field(name=f'Dealer: {bt1}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                        embed.set_footer(text='Dealer busted you won')
                        j = (l*2)
                        with open('users.json', 'r') as o:
                            users = json.load(o)
                        coins = users[f'{member.id}']['coins']
                        a = int(coins)
                        c = a+j
                        users[f'{member.id}']['coins'] = c
                
                        with open('users.json', 'w') as o:
                            json.dump(users, o)
                    
                        await ctx.send(embed=embed)
                        return
                    elif bt1 == at0 and bt1 <= 21:
                        botcard4 = random.choice(list(cards.items()))
                        b4 = int(botcard4[1])
                        bt2 = bt1+b4               
                        if bt2 <= 21:
                            embed = discord.Embed(title='Blackjack')
                            embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
                            embed.add_field(name=f'Dealer: {bt2}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]} {botcard4[0]}')
                            embed.set_footer(text='You Lost')
                            await ctx.send(embed=embed)
                elif bt > at0 and bt > 21:
                    embed = discord.Embed(title='Blackjack')
                    embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
                    embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]}')
                    embed.set_footer(text='Dealer busted you won')
                    j = (l*2)
                    with open('users.json', 'r') as o:
                        users = json.load(o)
                    coins = users[f'{member.id}']['coins']
                    a = int(coins)
                    c = a+j
                    users[f'{member.id}']['coins'] = c
                
                    with open('users.json', 'w') as o:
                        json.dump(users, o)
                    
                    await ctx.send(embed=embed)
                    return
                elif bt == at0 and bt <= 21:
                    botcard3 = random.choice(list(cards.items()))
                    b3 = int(botcard3[1])
                    bt1 = bt+b3                
                    if bt1 <= 21:
                        embed = discord.Embed(title='Blackjack')
                        embed.add_field(name=f'User: {at0}', value=f'{usercard1[0]} {usercard2[0]}')
                        embed.add_field(name=f'Dealer: {bt}', value=f'{botcard1[0]} {botcard2[0]} {botcard3[0]}')
                        embed.set_footer(text='You Lost')
                        await ctx.send(embed=embed)        
                        return


@bot.command()
async def war(ctx, coin=0, *, value=None):
    member = ctx.message.author
    with open('users.json', 'r') as f:
        users = json.load(f)
    coins = users[f'{member.id}']['coins']
    q = int(coins)
    l = int(coin)
    guild = bot.get_guild(661211931558019072)
    channels = ["♠┃gambling"]
    if str(ctx.channel) in channels:
        if l == 0:
            embed = discord.Embed(title='Usage', description='.war amount High/Low\nMinimum = 1\nMaximum = 10000')
            await ctx.send(embed=embed)
            return
        elif q < l:
            await ctx.send('Not enough coins to play this game')
            return    
        elif l < 1:
            await ctx.send('Minimum = 1')
            return
        elif l > 10000:
            await ctx.send('Maximum = 10000')
            return
        elif value is None:
            await ctx.send('Specify your card High or Low')
            return
        elif value == 'High' or value == 'high':
            member = ctx.message.author
            with open('users.json', 'r') as f:
                users = json.load(f)
            coins = users[f'{member.id}']['coins']
            a = int(coins)
            c = a-l
            users[f'{member.id}']['coins'] = c
            
            with open('users.json', 'w') as f:
                json.dump(users, f)
                
            cards = {
                        '<:s1:768850367299059743>' : '14', '<:s2:768850837103312956>' : '2', '<:s3:768850899945783306>' : '3', '<:s4:768850944372506634>' : '4', '<:s5:768850999716085821>' : '5', '<:s6:768851264653492255>' : '6', '<:s7:768851446183231518>' : '7', '<:s8:768851501752778752>' : '8', '<:s9:768851558246907925>' : '9', '<:s10:768851614265770027>' : '10', '<:s11:768852890164133899>' : '11', '<:s12:768853368591482920>' : '12', '<:s13:768853449676292126>' : '13',
                        '<:c1:769137965011173407>' : '14', '<:c2:769138045060120577>' : '2', '<:c3:769138140018769931>' : '3', '<:c4:769138233425526785>' : '4', '<:c5:769138319527116801>' : '5', '<:c6:769138409284436009>' : '6', '<:c7:769139223072604160>' : '7', '<:c8:769139406170357761>' : '8', '<:c9:769139511980458014>' : '9', '<:c10:769139572524187668>' : '10', '<:c11:769139639369334785>' : '11', '<:c12:769139714094661652>' : '12', '<:c13:769139782579257364>' : '13',
                        '<:h1:769134733854244874>' : '14', '<:h2:769134834139922472>' : '2', '<:h3:769134950216630301>' : '3', '<:h4:769135040759201792>' : '4', '<:h5:769135134653153310>' : '5', '<:h6:769135246490075136>' : '6', '<:h7:769135338961502249>' : '7', '<:h8:769135437138231306>' : '8', '<:h9:769135546642726942>' : '9', '<:h10:769135637906980875>' : '10', '<:h11:769135928815517716>' : '11', '<:h12:769136041646096394>' : '12', '<:h13:769136141865189376>' : '13',
                        '<:d1:769136359847624714>' : '14', '<:d2:769136487895007232>' : '2', '<:d3:769136555746131968>' : '3', '<:d4:769136642572812319>' : '4', '<:d5:769136717218971658>' : '5', '<:d6:769136799213158400>' : '6', '<:d7:769136883267534848>' : '7', '<:d8:769136966981517312>' : '8', '<:d9:769137055779127297>' : '9', '<:d10:769137144878858280>' : '10', '<:d11:769137268505313320>' : '11', '<:d12:769137356518195240>' : '12', '<:d13:769137443286417428>' : '13'
                    }
            usercard = random.choice(list(cards.items()))
            botcard = random.choice(list(cards.items()))
            u = int(usercard[1])
            b = int(botcard[1])
            if u < b:
                embed = discord.Embed(title='War')
                embed.add_field(name=f'User: {u}', value=f'{usercard[0]}')
                embed.add_field(name=f'Dealer: {b}', value=f'{botcard[0]}')
                embed.set_footer(text='You Lost your card was lower')
                await ctx.send(embed=embed)
                return
            elif u > b:
                embed = discord.Embed(title='Blackjack')
                embed.add_field(name=f'User: {u}', value=f'{usercard[0]}')
                embed.add_field(name=f'Dealer: {b}', value=f'{botcard[0]}')
                embed.set_footer(text='You won your card was higher')
                j = (l*2)
                with open('users.json', 'r') as o:
                    users = json.load(o)
                coins = users[f'{member.id}']['coins']
                a = int(coins)
                c = a+j
                users[f'{member.id}']['coins'] = c
        
                with open('users.json', 'w') as o:
                    json.dump(users, o)
        
                await ctx.send(embed=embed)
                return
            elif u == b:
                embed = discord.Embed(title='Blackjack')
                embed.add_field(name=f'User: {u}', value=f'{usercard[0]}')
                embed.add_field(name=f'Dealer: {b}', value=f'{botcard[0]}')
                embed.set_footer(text='Draw both cards are equal')
                j = l
                with open('users.json', 'r') as o:
                    users = json.load(o)
                coins = users[f'{member.id}']['coins']
                a = int(coins)
                c = a+j
                users[f'{member.id}']['coins'] = c
        
                with open('users.json', 'w') as o:
                    json.dump(users, o)
        
                await ctx.send(embed=embed)
                return
        elif value == 'Low' or value == 'low':
            member = ctx.message.author
            with open('users.json', 'r') as f:
                users = json.load(f)
            coins = users[f'{member.id}']['coins']
            a = int(coins)
            c = a-l
            users[f'{member.id}']['coins'] = c
            
            with open('users.json', 'w') as f:
                json.dump(users, f)
                
            cards = {
                        '<:s1:768850367299059743>' : '14', '<:s2:768850837103312956>' : '2', '<:s3:768850899945783306>' : '3', '<:s4:768850944372506634>' : '4', '<:s5:768850999716085821>' : '5', '<:s6:768851264653492255>' : '6', '<:s7:768851446183231518>' : '7', '<:s8:768851501752778752>' : '8', '<:s9:768851558246907925>' : '9', '<:s10:768851614265770027>' : '10', '<:s11:768852890164133899>' : '11', '<:s12:768853368591482920>' : '12', '<:s13:768853449676292126>' : '13',
                        '<:c1:769137965011173407>' : '14', '<:c2:769138045060120577>' : '2', '<:c3:769138140018769931>' : '3', '<:c4:769138233425526785>' : '4', '<:c5:769138319527116801>' : '5', '<:c6:769138409284436009>' : '6', '<:c7:769139223072604160>' : '7', '<:c8:769139406170357761>' : '8', '<:c9:769139511980458014>' : '9', '<:c10:769139572524187668>' : '10', '<:c11:769139639369334785>' : '11', '<:c12:769139714094661652>' : '12', '<:c13:769139782579257364>' : '13',
                        '<:h1:769134733854244874>' : '14', '<:h2:769134834139922472>' : '2', '<:h3:769134950216630301>' : '3', '<:h4:769135040759201792>' : '4', '<:h5:769135134653153310>' : '5', '<:h6:769135246490075136>' : '6', '<:h7:769135338961502249>' : '7', '<:h8:769135437138231306>' : '8', '<:h9:769135546642726942>' : '9', '<:h10:769135637906980875>' : '10', '<:h11:769135928815517716>' : '11', '<:h12:769136041646096394>' : '12', '<:h13:769136141865189376>' : '13',
                        '<:d1:769136359847624714>' : '14', '<:d2:769136487895007232>' : '2', '<:d3:769136555746131968>' : '3', '<:d4:769136642572812319>' : '4', '<:d5:769136717218971658>' : '5', '<:d6:769136799213158400>' : '6', '<:d7:769136883267534848>' : '7', '<:d8:769136966981517312>' : '8', '<:d9:769137055779127297>' : '9', '<:d10:769137144878858280>' : '10', '<:d11:769137268505313320>' : '11', '<:d12:769137356518195240>' : '12', '<:d13:769137443286417428>' : '13'
                    }
            usercard = random.choice(list(cards.items()))
            botcard = random.choice(list(cards.items()))
            u = int(usercard[1])
            b = int(botcard[1])
            if u > b:
                embed = discord.Embed(title='War')
                embed.add_field(name=f'User: {u}', value=f'{usercard[0]}')
                embed.add_field(name=f'Dealer: {b}', value=f'{botcard[0]}')
                embed.set_footer(text='You Lost your card was higher')
                await ctx.send(embed=embed)
                return
            elif u < b:
                embed = discord.Embed(title='Blackjack')
                embed.add_field(name=f'User: {u}', value=f'{usercard[0]}')
                embed.add_field(name=f'Dealer: {b}', value=f'{botcard[0]}')
                embed.set_footer(text='You won your card was lower')
                j = (l*2)
                with open('users.json', 'r') as o:
                    users = json.load(o)
                coins = users[f'{member.id}']['coins']
                a = int(coins)
                c = a+j
                users[f'{member.id}']['coins'] = c
        
                with open('users.json', 'w') as o:
                    json.dump(users, o)
        
                await ctx.send(embed=embed)
                return
            elif u == b:
                embed = discord.Embed(title='Blackjack')
                embed.add_field(name=f'User: {u}', value=f'{usercard[0]}')
                embed.add_field(name=f'Dealer: {b}', value=f'{botcard[0]}')
                embed.set_footer(text='Draw both cards are equal')
                j = l
                with open('users.json', 'r') as o:
                    users = json.load(o)
                coins = users[f'{member.id}']['coins']
                a = int(coins)
                c = a+j
                users[f'{member.id}']['coins'] = c
        
                with open('users.json', 'w') as o:
                    json.dump(users, o)
        
                await ctx.send(embed=embed)
                return

                
bot.loop.create_task(time_check())
         
bot.run(token)
        

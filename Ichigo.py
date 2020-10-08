from discord.ext.commands import Bot
from discord.ext import commands
import time
from discord.utils import get
import discord
import asyncio
import json
import random
import datetime

bot = commands.Bot(command_prefix=".")

token = open("token.txt","r").read()

bot.remove_command('help')

warn= ""
kick = ""
mute = ""
unmute = ""
ban = ""
unban = ""


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


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1
        users[f'{user.id}']['last_message'] = 0
        users[f'{user.id}']['info'] = None
        users[f'{user.id}']['bg'] = "https://i.imgur.com/DY2CKvu.png"
        users[f'{user.id}']['av'] = "None"
        


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
        role = discord.utils.get(member.guild.roles, name="Monster-Hunter")
        await member.add_roles(role)
        return
    elif lvl_end == 50:
        member = message.author
        role = discord.utils.get(member.guild.roles, name="Hero")
        await member.add_roles(role)
        return







@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


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


@bot.command(aliases=["purge"])
@commands.has_role("Inn Keepers")
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


@bot.command(aliases=["w"])
@commands.has_role("Waiters")
async def warn(ctx, member: discord.Member = None, *, reason=None):
    guild = bot.get_guild(661211931558019072)
    if member is None:
        await ctx.channel.purge(limit=1)
        await ctx.send("Member Not Found")
    elif member.bot:
        await ctx.channel.purge(limit=1)
        await ctx.send("Fool you can't warn the mighty one")
        return
    elif reason is None:
        await ctx.channel.purge(limit=1)
        await ctx.send("Reason Required")
        return
    else:
        member == member
    staff = discord.utils.get(member.guild.roles, name="Waiters")
    if staff in member.roles:
        await ctx.channel.purge(limit=1)
        await ctx.send("You can't warn the staff member")
    else:
        global warn
        warn = "({1}) warned ({0}) reason ({2})".format(member, ctx.message.author, reason)
        reason=reason
        embed = discord.Embed(title="Warn", description=f" You got a warning for **{reason}**\n \nServer: {guild.name}", colour=13882323)
        await member.send(content=None, embed=embed)
        await ctx.channel.purge(limit=1)
        print(f"Time: {time.asctime( time.localtime(time.time()) )}, Warn: {warn}\n")
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {time.asctime( time.localtime(time.time()) )}, Warn: {warn}\n")
        except Exception as e:
            print(e)



@bot.command(aliases=["k"])
@commands.has_any_role("Waiters", "Bot")
async def kick(ctx, member: discord.Member = None, *, reason=None):
    guild = bot.get_guild(661211931558019072)
    if member is None:
        await ctx.channel.purge(limit=1)
        await ctx.send("Member Not Found")
    elif member.bot:
        await ctx.channel.purge(limit=1)
        await ctx.send("Fool you can't kick the mighty one")
        return
    elif reason is None:
        await ctx.channel.purge(limit=1)
        await ctx.send("Reason Required")
        return
    else:
        member == member
    staff = discord.utils.get(member.guild.roles, name="Waiters")
    if staff in member.roles:
        await ctx.channel.purge(limit=1)
        await ctx.send("You can't kick the staff member")
    else:
        embed = discord.Embed(title="Kicked", description=f" You got kicked  for **{reason}**\n \nServer: {guild.name}", colour=13882323)
        await member.send(content=None, embed=embed)
        await member.kick(reason=reason)
        await ctx.channel.purge(limit=1)
        global kick
        kick = "({1}) kicked ({0}) reason ({2})".format(member, ctx.message.author, reason)
        print(f"Time: {time.asctime( time.localtime(time.time()) )}, Kick: {kick}\n")
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {time.asctime( time.localtime(time.time()) )}, Kick: {kick}\n")
        except Exception as e:
            print(e)


@bot.command(aliases=["b"])
@commands.has_any_role("Inn Keepers", "Bot")
async def ban(ctx, member: discord.Member = None, *, reason=None):
    guild = bot.get_guild(661211931558019072)
    if member is None:
        await ctx.channel.purge(limit=1)
        await ctx.send("Member Not Found")
    elif member.bot:
        await ctx.channel.purge(limit=1)
        await ctx.send("Fool you can't ban the mighty one")
        return
    elif reason is None:
        await ctx.channel.purge(limit=1)
        await ctx.send("Reason Required")
        return
    else:
        embed = discord.Embed(title="Banned", description=f" You got banned for **{reason}** talk to @Azog The Defiler#5131 if you are serious or there was some misunderstanding\n \nServer: {guild.name}", colour=13882323)
        await member.send(content=None, embed=embed)
        await member.ban(reason=reason)
        await ctx.channel.purge(limit=1)
        global ban
        ban = "({1}) banned ({0}) reason ({2})".format(member, ctx.message.author, reason)
        print(f"Time: {time.asctime( time.localtime(time.time()) )}, Ban: {ban}\n")
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {time.asctime( time.localtime(time.time()) )}, Ban: {ban}\n")
        except Exception as e:
            print(e)


@bot.command(aliases=["sban"])
@commands.has_role("Inn Keepers")
async def serverban(ctx, id: int, *, reason=None):
    if reason is None:
        await ctx.channel.purge(limit=1)
        await ctx.send("Reason Required")
        return
    elif member.bot:
        await ctx.channel.purge(limit=1)
        await ctx.send("Fool you can't ban the mighty one")
        return
    else:
        user = await bot.fetch_user(id)
        await ctx.channel.purge(limit=1)
        await ctx.guild.ban(user)
        await ctx.send(f'Banned {id}')
        global ban
        reason=reason
        sban = "({1}) server banned ({0}) reason ({2})".format(id, ctx.message.author, reason)
        print(f"Time: {time.asctime( time.localtime(time.time()) )}, Serverban: {sban}\n")
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {time.asctime( time.localtime(time.time()) )}, SBan: {sban}\n")
        except Exception as e:
            print(e)

@bot.command(aliases=["ub"])
@commands.has_role("Inn Keepers")
async def unban(ctx, id: int, *, reason=None):
    if reason is None:
        await ctx.channel.purge(limit=1)
        await ctx.send("Reason Required")
        return
    elif member.bot:
        await ctx.channel.purge(limit=1)
        await ctx.send("Fool you can't ban or unban the mighty one")
        return
    else:
        user = await bot.fetch_user(id)
        await ctx.channel.purge(limit=1)
        await ctx.guild.unban(user)
        await ctx.send(f'Successfully Unbanned {user.name}#{user.discriminator}')
        global unban
        unban = "({1}) unbanned ({0}) reason ({2})".format(id, ctx.message.author, reason)
        print(f"Time: {time.asctime( time.localtime(time.time()) )}, Unban: {unban}\n")
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {time.asctime( time.localtime(time.time()) )}, Unban: {unban}\n")
        except Exception as e:
            print(e)


@bot.command(aliases=["m"])
@commands.has_role("Waiters")
async def mute(ctx, member: discord.Member = None, *, reason=None):
    guild = bot.get_guild(661211931558019072)
    if member is None:
        await ctx.channel.purge(limit=1)
        await ctx.send("Member Not Found")
        return
    elif member.bot:
        await ctx.channel.purge(limit=1)
        await ctx.send("Fool you can't mute the mighty one")
        return
    else:
        member == member
    staff = discord.utils.get(member.guild.roles, name="Waiters")
    role = discord.utils.get(member.guild.roles, name="Muted")
    if role in member.roles:
        await ctx.channel.purge(limit=1)
        await ctx.send("User is already Muted")
    elif staff in member.roles:
        await ctx.channel.purge(limit=1)
        await ctx.send("You can't mute the staff member")
    else:
        await member.add_roles(role)
        await ctx.channel.purge(limit=1)
        await ctx.send("**{0}** was muted by **{1}**!".format(member, ctx.message.author))
        embed = discord.Embed(title="Muted", description=f" You got muted for **{reason}**\n \nServer: {guild.name}", colour=13882323)
        await member.send(content=None, embed=embed)
        global mute
        mute = "({1}) muted ({0}) reason ({2})".format(member, ctx.message.author, reason)
        print(f"Time: {time.asctime( time.localtime(time.time()) )}, Mute: {mute}\n")
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {time.asctime( time.localtime(time.time()) )}, Mute: {mute}\n")
        except Exception as e:
            print(e)


@bot.command(pass_context = True, aliases=["um"])
@commands.has_role("Waiters")
async def unmute(ctx, member: discord.Member = None, *, reason=None):
    guild = bot.get_guild(661211931558019072)
    role = discord.utils.get(member.guild.roles, name="Muted")
    if member is None:
        await ctx.channel.purge(limit=1)
        await ctx.send("Member Not Found")
    elif member.bot:
        await ctx.channel.purge(limit=1)
        await ctx.send("Fool you cant warn the mighty one")
        return
    elif role not in member.roles:
        await ctx.channel.purge(limit=1)
        await ctx.send("User is not muted")
    else:
        await member.remove_roles(role)
        await ctx.channel.purge(limit=1)
        await ctx.send("**{0}** was unmuted by **{1}**!".format(member, ctx.message.author))
        embed = discord.Embed(title="Unmuted", description=f" You are now unmuted\n \nServer: {guild.name}", colour=13882323)
        await member.send(content=None, embed=embed)
        global unmute
        unmute = "({1}) unmuted ({0}) reason ({2})".format(member, ctx.message.author, reason)
        print(f"Time: {time.asctime( time.localtime(time.time()) )}, Unmute: {unmute}\n")
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {time.asctime( time.localtime(time.time()) )}, Unmute: {unmute}\n")
        except Exception as e:
            print(e)


@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)
    role = discord.utils.get(member.guild.roles, name="Wanderer")
    await member.add_roles(role)
    e = discord.Embed()
    e.set_image(url="https://cdn.discordapp.com/attachments/686941615490596922/686941777248124940/Underworld.jpg")
    guild = bot.get_guild(661211931558019072)
    for channel in member.guild.channels:
        if str(channel) == "⚔┃wanderers-guild":
            await channel.send(f"""Welcome to the **{guild.name}** {member.mention} """, embed=e)
            return


@bot.command()
async def help(ctx):
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
        embed = discord.Embed(title="Bot Commands", description="Here are all the bot commands \n \n**.ping** = "
                                                                "\"Replies with latency\" \n**.pfp** = \""
                                                                "Shows user\'s profile picture\" \n**.userinfo** = \"Shows "
                                                                "user\'s info\" \n**.serverinfo** = \"Shows server info\" \n"
                                                                "**.profile**= \"Shows user\'s server profile \"\n"
                                                                "**.edit**= \"For changing customizable info\"\n"
                                                                "**.avatars** = \"Sends pictures to choose an avatar for the profile\"\n", colour=0x101010)
        await ctx.send(content=None, embed=embed)


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
async def staff(ctx):
    channels = ["🏛┃council"]
    if str(ctx.channel) in channels:
        embed = discord.Embed(title="Staff Commands", description="Here are all the staff commands \n \n \n __**kick/k**__ = "
                                                                        "\"Kicks user\" \n __**mute/m**__ = \""
                                                                        "Mutes the user\" \n __**unmute/um**__ = \"Unmutes the user\" \n", colour=16711935)
        await ctx.send(content=None, embed=embed)


@bot.command()
async def profile(ctx, member: discord.Member = None):
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
        if member is not None:
            id = member.id
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
                    av = None
                else:
                    info = users[str(id)]['info']
                    bg = users[str(id)]['bg']
                    av = users[str(id)]['av']
                    if user.is_avatar_animated():
                        embed = discord.Embed()
                        embed.set_image(url=f"{bg}")
                        embed.set_footer(text=f"ID: {user.id}")
                        embed.add_field(name="__**Profile:**__", value=f"**Discord Name:** {user}\n"
                                                                        f"**Nickname:** {user.nick}\n"
                                                                        f"**Member Since:** {join_days}\n"
                                                                        f"**Level:** {level}\n\n\n"
                                                                        f"**Info:** {info}\n"
                                                                        f"**Avatar:** {av}")
                        await ctx.send(embed=embed)
                        return
                    else:
                        embed = discord.Embed()
                        embed.set_image(url=f"{bg}")
                        embed.set_footer(text=f"ID: {user.id}")
                        embed.add_field(name="__**Profile:**__", value=f"**Discord Name:** {user}\n"
                                                                        f"**Nickname:** {user.nick}\n"
                                                                        f"**Member Since:** {join_days}\n"
                                                                        f"**Level:** {level}\n\n\n"
                                                                        f"**Info:** {info}\n"
                                                                        f"**Avatar:** {av}")
                        await ctx.send(embed=embed)
                        return
        else:
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
                av = None
            else:
                info = users[str(id)]['info']
                bg = users[str(id)]['bg']
                av = users[str(id)]['av']
                if user.is_avatar_animated():
                    embed = discord.Embed()
                    embed.set_image(url=f"{bg}")
                    embed.set_footer(text=f"ID: {user.id}")
                    embed.add_field(name="__**Profile:**__", value=f"**Discord Name:** {user}\n"
                                                                    f"**Nickname:** {user.nick}\n"
                                                                    f"**Member Since:** {join_days}\n"
                                                                    f"**Level:** {level}\n\n\n"
                                                                    f"**Info:** {info}\n"
                                                                    f"**Avatar:** {av}")
                    await ctx.send(embed=embed)
                    return
                else:
                    embed = discord.Embed()
                    embed.set_image(url=f"{bg}")
                    embed.set_footer(text=f"ID: {user.id}")
                    embed.add_field(name="__**Profile:**__", value=f"**Discord Name:** {user}\n"
                                                                    f"**Nickname:** {user.nick}\n"
                                                                    f"**Member Since:** {join_days}\n"
                                                                    f"**Level:** {level}\n\n\n"
                                                                    f"**Info:** {info}\n"
                                                                    f"**Avatar:** {av}")
                await ctx.send(embed=embed)
                return

@bot.command()
async def edit(ctx, *, info):
    channels = ["🤖┃machinery"]
    if str(ctx.channel) in channels:
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
async def event(message, user: discord.Member = None):
    channels = ["🗣┃event-wall"]
    if str(message.channel) in channels:
        await message.channel.purge(limit=1)
        embed = discord.Embed(colour=0x4B0082)
        embed.add_field(name="**Event**", value=f"React to :scroll: to get **Bard** role. "
                                                f"You will get notified whenever there is an event\n\n"
                                                f"So don\'t forget to react")
        message = await message.channel.send(embed=embed)
        await message.add_reaction("\U0001F4DC")
        await message.add_reaction(u"\u274C")
        emote = ['\U0001F4DC', u'\u274C']
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


@bot.command()
@commands.has_role("Inn Keepers")
async def avatars(message, user: discord.Member = None):
    channels = ["🤖┃machinery"]
    if str(message.channel) in channels:
        user = message.author
        uu = user.id
        embed = discord.Embed(title="**Spike Spiegel**", colour=0x4B0082)
        embed.set_image(url="https://i.imgur.com/Xc94Jr6.png")
        message = await message.channel.send(embed=embed)
        await message.add_reaction(u"\u2705")
        await message.add_reaction(u"\u274C")
        emote = [u"\u274C", u"\u2705"]
        while True:
            def check(reaction, user):
                return (reaction.message.id == message.id) and (user != bot.user) and (str(reaction) in emote)
            reaction, user = await bot.wait_for('reaction_add', check=check)
            if str(reaction) == u"\u274C":
                await message.delete()
                embed = discord.Embed(title="**Angelo Lagusa**", colour=0x4B0082)
                embed.set_image(url="https://i.imgur.com/E6pmTsg.png")
                message = await message.channel.send(embed=embed)
                await message.add_reaction(u"\u2705")
                await message.add_reaction(u"\u274C")
                emote = [u"\u274C", u"\u2705"]
                while True:
                    def check(reaction, user):
                        return (reaction.message.id == message.id) and (user != bot.user) and (str(reaction) in emote)
                    reaction, user = await bot.wait_for('reaction_add', check=check)
                    if str(reaction) == u"\u274C":
                        await message.delete()
                        embed = discord.Embed(title="**Kakashi Hatake**", colour=0x4B0082)
                        embed.set_image(url="https://i.imgur.com/lYzFU4h.png")
                        message = await message.channel.send(embed=embed)
                        await message.add_reaction(u"\u2705")
                        await message.add_reaction(u"\u274C")
                        emote = [u"\u274C", u"\u2705"]
                        while True:
                            def check(reaction, user):
                                return (reaction.message.id == message.id) and (user != bot.user) and (str(reaction) in emote)
                            reaction, user = await bot.wait_for('reaction_add', check=check)
                            if str(reaction) == u"\u274C":
                                await message.delete()
                                embed = discord.Embed(title="**Kagehisa Anotsu**", colour=0x4B0082)
                                embed.set_image(url="https://i.imgur.com/vRuiLMg.png")
                                message = await message.channel.send(embed=embed)
                                await message.add_reaction(u"\u2705")
                                await message.add_reaction(u"\u274C")
                                emote = [u"\u274C", u"\u2705"]
                                while True:
                                    def check(reaction, user):
                                        return (reaction.message.id == message.id) and (user != bot.user) and (str(reaction) in emote)
                                    reaction, user = await bot.wait_for('reaction_add', check=check)
                                    if str(reaction) == u"\u274C":
                                        await message.delete()
                                        embed = discord.Embed(title="**Roy Mustang**", colour=0x4B0082)
                                        embed.set_image(url="https://i.imgur.com/ipNdi7X.png")
                                        message = await message.channel.send(embed=embed)
                                        await message.add_reaction(u"\u2705")
                                        await message.add_reaction(u"\u274C")
                                        emote = [u"\u274C", u"\u2705"]
                                        while True:
                                            def check(reaction, user):
                                                return (reaction.message.id == message.id) and (user != bot.user) and (str(reaction) in emote)
                                            reaction, user = await bot.wait_for('reaction_add', check=check)
                                            if str(reaction) == u"\u274C":
                                                await message.delete()
                                                embed = discord.Embed(title="**Minato Namikaze**", colour=0x4B0082)
                                                embed.set_image(url="https://i.imgur.com/CqiDOJj.png")
                                                message = await message.channel.send(embed=embed)
                                                await message.add_reaction(u"\u2705")
                                                await message.add_reaction(u"\u274C")
                                                emote = [u"\u274C", u"\u2705"]
                                                while True:
                                                    def check(reaction, user):
                                                        return (reaction.message.id == message.id) and (user != bot.user) and (str(reaction) in emote)
                                                    reaction, user = await bot.wait_for('reaction_add', check=check)
                                                    if str(reaction) == u"\u274C":
                                                        await message.delete()
                                                        guild = bot.get_guild(661211931558019072)
                                                        channel = guild.get_channel(686918214327861266)
                                                        await channel.send("It seems like we ran out of avatars")
                                                    elif str(reaction) == u"\u2705":
                                                        await message.delete()
                                                        bg = "https://i.imgur.com/CqiDOJj.png"
                                                        av = "Minato Namikaze"
                                                        with open('users.json', 'r') as p:
                                                            users = json.load(p)
                                                
                                                        await back(users, user, bg, av)
                                                
                                                        with open('users.json', 'w') as p:
                                                            json.dump(users, p)
                                                
                                                        await message.channel.send('Added')
                                            elif str(reaction) == u"\u2705":
                                                await message.delete()
                                                bg = "https://i.imgur.com/ipNdi7X.png"
                                                av = "Roy Mustang"
                                                with open('users.json', 'r') as p:
                                                    users = json.load(p)
                                        
                                                await back(users, user, bg, av)
                                        
                                                with open('users.json', 'w') as p:
                                                    json.dump(users, p)
                                        
                                                await message.channel.send('Added')
                                    elif str(reaction) == u"\u2705":
                                        await message.delete()
                                        bg = "https://i.imgur.com/vRuiLMg.png"
                                        av = "Kagehisa Anotsu"
                                        with open('users.json', 'r') as p:
                                            users = json.load(p)
                                
                                        await back(users, user, bg, av)
                                
                                        with open('users.json', 'w') as p:
                                            json.dump(users, p)
                                
                                        await message.channel.send('Added')
                            elif str(reaction) == u"\u2705":
                                await message.delete()
                                bg = "https://i.imgur.com/lYzFU4h.png"
                                av = "Kakashi Hatake"
                                with open('users.json', 'r') as p:
                                    users = json.load(p)

                                await back(users, user, bg, av)

                                with open('users.json', 'w') as p:
                                    json.dump(users, p)

                                await message.channel.send('Added')
                    elif str(reaction) == u"\u2705":
                        await message.delete()
                        bg = "https://i.imgur.com/E6pmTsg.png"
                        av = "Angelo Lagusa"
                        with open('users.json', 'r') as p:
                            users = json.load(p)

                        await back(users, user, bg, av)

                        with open('users.json', 'w') as p:
                            json.dump(users, p)

                        await message.channel.send('Added')
            elif str(reaction) == u"\u2705":
                await message.delete()
                bg = "https://i.imgur.com/Xc94Jr6.png"
                av = "Spike Spiegel"
                with open('users.json', 'r') as p:
                    users = json.load(p)

                await back(users, user, bg, av)

                with open('users.json', 'w') as p:
                    json.dump(users, p)
                await message.channel.send('Added')
async def back(users, user, bg, av):
    if f'{user.id}' in users:
        users[f'{user.id}']['bg'] = bg
        users[f'{user.id}']['av'] = av
        return



        
bot.run(token)

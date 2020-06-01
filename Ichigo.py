import discord
from discord.ext import commands

client = commands.Bot(command_prefix=".")


@client.command()
async def ping(ctx):
    await ctx.send("Pong!")


@client.command()
async def serverinfo(ctx):
    server = client.get_guild(661211931558019072)
    channels = ["commands"]
    if str(ctx.channel) in channels:
        embed = discord.Embed(title="Server Information", colour=12632256)
        embed.add_field(name="Server Name:", value="Hell", inline=False)
        embed.add_field(name="Server Owner", value="Azog The Smoker#7877", inline=False)
        embed.add_field(name="Server Created:", value="Mon Dec 30 2019", inline=False)
        embed.add_field(name="Member Count:", value=f"""{server.member_count}""")
    await ctx.send(embed=embed)


@client.command()
async def clear(ctx, amount=50):
    await ctx.channel.purge(limit=amount)


@client.command()
async def kick(ctx, member: discord.Member = None, *, reason=None):
    if member is None:
        await ctx.send("Member Not Found")
    else:
        await member.kick(reason=reason)
        await ctx.channel.purge(limit=1)


@client.command()
async def ban(ctx, member: discord.Member = None, *, reason=None):
    if member is None:
        await ctx.send("Member Not Found")
    else:
        await member.ban(reason=reason)
        await ctx.channel.purge(limit=1)


@client.event
async def on_member_join(member, ctx):
    role = ctx.guild.get_role(686919779562553356)
    e = discord.Embed()
    e.set_image(url="https://cdn.discordapp.com/attachments/686941615490596922/686941777248124940/Underworld.jpg")
    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send(f"""Welcome to the Underworld {member.mention} """, embed=e)
            await member.add_roles(role, atomic=True)

@client.command()
async def commands(ctx):
    channels = ["commands"]
    if str(ctx.channel) in channels:
        embed = discord.Embed(title="Bot Commands", description="Here are all the bot commands \n \n \n __**ping**__ = "
                                                                "\"Replies with Pong\" \n __**stats**__ = "
                                                                "\"Sends stats of the server\" \n __**avatar**__ = \""
                                                                "Shows user\'s avatar\" \n __**userinfo**__ = \"Shows "
                                                                "user\'s info\" \n __**serverinfo**__ = \"Shows server info\" \n", colour=16711935)
        await ctx.send(content=None, embed=embed)


@client.command()
async def userinfo(ctx, *, user: discord.Member = None):
    channels = ["commands"]
    if str(ctx.channel) in channels:
        if user is None:
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


@client.command()
async def avatar(ctx, *, user: discord.Member = None):
    channels = ["commands"]
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


client.run("NjUyMDY3MjUzMDgwMDMxMjMz.XnDPvA.3-6i5zNh2bfl2MCxyf1JHJsRTAs")

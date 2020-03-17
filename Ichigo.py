import discord
from discord.ext import commands

messages = joined = 0


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

client = commands.Bot(command_prefix=".")


@client.command()
async def ping(ctx):
    await ctx.send("Pong!")


@client.command()
async def stats(ctx):
    server = client.get_guild(661211931558019072)
    channels = ["commands"]
    if str(ctx.channel) in channels:
        await ctx.send(f"""Owner: Azog The Defiler\nNumber of Members: {server.member_count}""")


@client.command()
async def clear(ctx, amount=50):
    await ctx.channel.purge(limit=amount)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)


@client.event
async def on_member_join(member):
    e = discord.Embed()
    e.set_image(url="https://cdn.discordapp.com/attachments/686941615490596922/686941777248124940/Underworld.jpg")
    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send(f"""Welcome to the Underworld {member.mention} """, embed=e)


@client.command()
async def commands(ctx):
    server = client.get_guild(661211931558019072)
    channels = ["commands"]
    if str(ctx.channel) in channels:
        embed = discord.Embed(title="Bot Commands", description="Here are all the bot commands \n \n \n __**ping**__ = "
                                                                "\"Replies with Pong\" \n __**stats**__ = "
                                                                "\"Sends stats of the server\"", colour=16711935)
        await ctx.send(content=None, embed=embed)


client.run(token)

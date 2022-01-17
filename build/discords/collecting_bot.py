import asyncio
import discord
from discord.ext import commands

# command prefix ^
bot = commands.Bot(command_prefix="^")
bot_token = "[your bot tokken]"


def file_write(file_name, hash):
    file = "./%s.txt" % (file_name)
    tmp = list()

    # default message
    message = "error"
    try:
        with open(file, "r") as f:
            for line in f:
                tmp.append(line.strip())
            if hash in tmp:
                message = "already existing"
                return message
    except(Exception):
        pass
    tmp.append(hash)
    with open(file, "w") as f:
        for line in tmp:
            f.write(line + '\n')

    # print("%s %s saved" % (file_name, hash))

    message = "%s: %s \nsaved" % (file_name, hash)
    return message


manual = discord.Embed(
    title="command list",
    description='''collecting bot
    command prefix: ^''',
    color=0xffffff
    )

manual.add_field(
    name="^state",
    value="check if bot is alive",
    inline=False
    )

manual.add_field(
    name="^channel [channel hash]",
    value='''collect channel hash value.
    you can know if it is already exist''',
    inline=False
    )

manual.add_field(
    name="^user [user hash]",
    value='''collect user hash value.
    you can know if it is already exist''',
    inline=False
    )


@bot.event
async def on_ready():
    print("on!")


@bot.command()
async def command(ctx):
    await ctx.send(embed=manual)


@bot.command()
async def state(ctx):
    await ctx.send("alive")


@bot.command()
async def channel(ctx, channel_hash):
    # add work here
    result = file_write("channel", channel_hash)
    await ctx.send(result)


@bot.command()
async def user(ctx, user_hash):
    # add work here
    result = file_write("user", user_hash)
    await ctx.send(result)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("command not found")
        await ctx.send(embed=manual)

bot.run(bot_token)

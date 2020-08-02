import discord.ext
import json, functions, datetime
from discord.ext import commands

try:
    with open('settings.json') as configFile:
        config = json.load(configFile)
        token = config['token']
        prefix = config['prefix']
except Exception as e:
    print(e)

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_guild_join(guild):
    guilds = functions.read_guildsFile()
    guildList = []
    for x in guilds:
        guildList.append(x['id'])
    if guild.id not in guildList:
        now = datetime.datetime.now()
        data = {
            'id': guild.id,
            'owner': guild.owner.id,
            'admins': [],
            'badwords':[],
            'enabled': 1,
            'logs': 1,
            'joined': now.strftime("%Y-%m-%d %H:%M:%S")
        }
        guilds.append(data)
        try:
            with open('guilds.json', 'w') as outfile:
                json.dump(guilds, outfile, indent=4)
        except Exception as e:
            print(e)

@bot.command()
async def blacklist(ctx):
    """
    Shows a list of all blacklsted words.
    To add or remove words from the blacklist, please use the 'blacklist_add' or 'blacklist_remove' command. Notice that these commands are only available for permitted users.
    """
    guilds = functions.read_guildsFile()
    for x in guilds:
        if x['id'] == ctx.guild.id:
            sep = "\n"
            wordList = sep.join(x['badwords'])
            if len(wordList) < 1:
                wordList = "*Your blacklist is empty!*"
            embed = discord.Embed(  title = 'BadWords Blacklist', 
                                    description = 'This is a list of all balcklisted words on this server. To add or remove words from the blacklist, please use the "blacklist_add" or "blacklist_remove" command (admins only)',
                                    colour=discord.Colour(0xeb8c34))
            embed.add_field(name = "List", value = wordList)
            await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def blacklist_add(ctx, arg1 = None):
    """
    Adds a word to your blacklist
    To add a phrase out of more than one word, use quotation marks. Example: "more than one word"
    """
    guilds = functions.read_guildsFile()
    for x in guilds:
        if x['id'] == ctx.guild.id:
            if arg1 not in x['badwords']:
                try:
                    x['badwords'].append(arg1.lower())
                    functions.write_guildsFile(guilds)
                    await ctx.send('`' + arg1 + '` was added to your blacklist!')
                except Exception as e:
                    print(e)
            else:
                await ctx.send("`" + arg1 + "` is already on your blacklist!")

@bot.command()
@commands.has_permissions(administrator=True)
async def blacklist_remove(ctx, arg1 = None):
    """
    Removes a word from your blacklist
    To remove a phrase out of more than one word, use quotation marks. Example: "more than one word"
    To show your actual blacklisted words, use the blacklist command.
    """
    guilds = functions.read_guildsFile()
    for x in guilds:
        if x['id'] == ctx.guild.id:
            if arg1.lower() in x['badwords']:
                try:
                    x['badwords'].remove(arg1.lower())
                    functions.write_guildsFile(guilds)
                    await ctx.send('`' + arg1 + '` was removed from your blacklist!')
                except Exception as e:
                    print(e)
            else:
                await ctx.send("`" + arg1 + "` is not on your blacklist!")

@bot.command()
@commands.has_permissions(administrator=True)
async def logs_on(ctx):
    """
    Enables logs
    To view logs, create a channel with the name "logs" and give the bot permission to send messages in it. The bot will detect the channel automaticaally and post logs when a message was deleted.
    """
    guilds = functions.read_guildsFile()
    for x in guilds:
        if x['id'] == ctx.guild.id:
            if x['logs'] == 1:
                await ctx.send('Logs already enabled! Create a channel "logs" to see them.')
            else:
                x['logs'] = 1
                functions.write_guildsFile(guilds)
                await ctx.send('Logs enabled!')

@bot.command()
@commands.has_permissions(administrator=True)
async def logs_off(ctx):
    """
    Disables logs
    Use this command to disable logs in your "logs" channel.
    """
    guilds = functions.read_guildsFile()
    for x in guilds:
        if x['id'] == ctx.guild.id:
            if x['logs'] == 0:
                await ctx.send('Logs already disabled!')
            else:
                x['logs'] = 0
                functions.write_guildsFile(guilds)
                await ctx.send('Logs disabled!')

@bot.event
async def on_command_error(ctx, error):
    """The event triggered when an error is raised while invoking a command.
    Parameters
    ------------
    ctx: commands.Context
        The context used for command invocation.
    error: commands.CommandError
        The Exception raised.
    """
    await ctx.send(error)

@bot.event
async def on_error(ctx, error):
    print('----------------------------------------------')
    print('ERROR !!! ERROR !!! ERROR !!! ERROR !!! ERROR')
    print(error)
    print(ctx)
    print('----------------------------------------------')

@bot.event
async def on_message(ctx):
    if ctx.author.id == bot.user.id:
        return
    else:
        guilds = functions.read_guildsFile()
        for x in guilds:
            if x['id'] == ctx.guild.id:
                for y in x['badwords']:
                    if y in ctx.content.lower():
                        await ctx.delete()
                        await ctx.channel.send('Watch your profanity, <@' + str(ctx.author.id) + '> !!')
                        trigger = y
                        try:
                            if x['logs'] == 1:
                                channel = discord.utils.get(ctx.guild.text_channels, name="logs")
                                embed = discord.Embed(  title = 'Message deleted', 
                                                        description = 'Bad word detected! Message was deleted automatically.',
                                                        colour=discord.Colour(0xf20000),
                                                        timestamp=datetime.datetime.utcfromtimestamp(datetime.datetime.now().timestamp()))
                                embed.add_field(name = '__User__', value = '**' + str(ctx.author) + '**\n' + str(ctx.author.id), inline = False)
                                embed.add_field(name = '__Triggered word__', value = trigger, inline = False)
                                embed.add_field(name = '__Channel__', value = '**' + ctx.channel.name + '**\n' + str(ctx.channel.id))
                                embed.add_field(name = '__Server__', value = '**' + ctx.guild.name + '**\n' + str(ctx.guild.id))
                                embed.add_field(name = '__Message__', value = ctx.content, inline = False)
                                #embed.set_author(name = str(ctx.author), icon_url = ctx.author.avatar_url)
                                embed.set_thumbnail(url = ctx.author.avatar_url)
                                await channel.send(embed = embed)
                        except:
                            pass
    await bot.process_commands(ctx)

bot.run(token)
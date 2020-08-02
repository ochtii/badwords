import discord, json, datetime
import functions
from discord.ext import commands
from pprint import pprint

# getting settings from settings.json
try:
    with open('settings.json') as configFile:
        config = json.load(configFile)
        token = config['token']
        prefix = config['prefix']
        ochtii = config['ochtii']
except Exception as e:
    print(e)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
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
            'joined': now.strftime("%Y-%m-%d %H:%M:%S")
        }
        guilds.append(data)
        try:
            with open('guilds.json', 'w') as outfile:
                json.dump(guilds, outfile, indent=4)
        except Exception as e:
            print(e)
        

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower()
    command = msg.split()[0][len(prefix):]
    isCommand = False
    
    guilds = functions.read_guildsFile()

    for x in guilds:
        if x['id'] == message.guild.id:
            if message.author.id == x['owner']:
                owner = True
            elif message.author.id in x['admins']:
                admin = True
            else:
                owner = False
                admin = False

    if msg.startswith(prefix):

        if command == "help" or command == "?":
            isCommand = True
            await message.channel.send('ok')

        if command == "blacklist_add":
            isCommand = True
            await message.channel.send('ok')

        if command == "blacklist_remove":
            isCommand = True
            await message.channel.send('ok')

        if command == "blacklist":
            isCommand = True
            if admin == False or owner == False:
                await message.channel.send('Missing Permission!')
            else:
                for x in guilds:
                    if x['id'] == message.guild.id:
                        sep = "\n"
                        wordList = sep.join(x['badwords'])
                        embed = discord.Embed(  title = 'BadWords Blacklist', 
                                                description = 'This is a list of all balcklisted words on this server. To add or remove words from this list, use `' + prefix + 'help`.',
                                                colour=discord.Colour(0xeb8c34))
                        embed.add_field(name = "List", value = wordList)
                        await message.channel.send(embed = embed)
            
        if command == "admin_add":
            isCommand = True
            await message.channel.send('ok')

        if command == "admin_remove":
            isCommand = True
            await message.channel.send('ok')
        
        if command == "enable":
            isCommand = True
            await message.channel.send('ok')

        if command == "disable":
            isCommand = True
            pprint(message.author.guild_permissions.administrator)

    if isCommand == False:
        for x in guilds:
            if x['id'] == message.guild.id:
                for y in x['badwords']:
                    if y in msg:
                        await message.delete()




client.run(token)
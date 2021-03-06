import io
import discord
from discord.ext import commands
import random
import sqlite3
import urllib
from prettytable import PrettyTable

description = '''Version one BPMbot basic functionality introduced'''
bot = commands.Bot(command_prefix='?', description=description, case_insensitive=True)

def getEmbed(song):
    title = song[0]
    # ac = 0
    # for char in title:
    #     if ord(char)>3000:
    #         ac+=2
    #     else:
    #         ac+=1
    # print (str(ac)+' : '+song[0])
    # print (str(len(song[1]))+ ' : '+song[1])

    em = discord.Embed()
    jacket ='https://furiousdcsl.github.io/jackets/'+urllib.parse.quote(song[5])
    #jacket = jacket.replace(' ', '%20')
    print (jacket)
    em.set_thumbnail(url = jacket)
    if len(song[1])>0:
        em.add_field(name=song[0],value=song[1], inline = True)
    else:
        em.add_field(name=song[0], value='\u200b', inline = True)
    if len(song[3])>0:
        em.add_field(name=song[2],value='\t'+song[3], inline = True)
    else:
        em.add_field(name=song[2], value='\u200b', inline = True)
    em.add_field(name = 'BPM', value = song[7], inline = True)
    em.add_field(name = 'Folder', value = song[6], inline = True)
    return em

def getBPMCEmbed(song, bpm):
    em = getEmbed(song)
    wantBPM = float(bpm)
    songBPM = float(song[8])

    mul = wantBPM / songBPM
    (lowMul, highMul) = getClosestMultipiler(mul)

    em.add_field(name = 'BPM conversion', value = f'```Low mul:   {lowMul:.2f}\tBPM: {lowMul*songBPM:.2f}\nIdeal mul: {mul:.2f}\tBPM: {mul*songBPM:.2f}\nHigh mul:  {highMul:.2f}\tBPM: {highMul*songBPM:.2f}```' )
    return em

def getMessage(song):
    x = PrettyTable()
    x.border = False
    x.header = False
    x.field_names = ['1','2','3','4']
    x.add_row(['Title:', song[0],'Artist:', song[2]])
    if len(song[1]) >0 and len (song[3]) >0:
        x.add_row([' ', song[1] , ' ', song[3]] )
    elif len(song[1])>0:
        x.add_row([' ', song[1], '', ''])
    elif len(song[3])>0:
        x.add_row(['', '', ' ', song[3]])
    x.add_row(['BPM:', song[7], 'Folder:', song[6]])
    x.align['1'] = 'r'
    x.align['2'] = 'l'
    x.align['3'] = 'r'
    x.align['4'] = 'l'

    print(x)
    message = x.get_string()
    return message

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

def isAdmin(user):
    if user.id == 153749984599080960: # FIX ME
        return True
    else:
        return False

@bot.command(aliases = ['quit'])
async def exit(ctx):
    if isAdmin(ctx.message.author):
        await ctx.send('Shutting down.')
        await bot.logout()
    else:
        await ctx.send('Only bot admind may exit bot.')

@bot.command(aliases = ['s', 'ser'])
async def search(ctx, *, song):
    """Look for song partial matches work. (If you type "?search 300" it will show MAX 300, X-Special and SMM Mix)"""

    search = AceCur.execute('SELECT * FROM songs WHERE title LIKE ? OR title_translation LIKE ?', ('%'+song+'%','%'+song+'%'))
    songs = []
    for row in search:
        songs.append(row)
    search = AceCur.execute('SELECT * FROM songs WHERE title = ? COLLATE NOCASE or title_translation = ?  COLLATE NOCASE', (song,song))
    exact_match = []
    for row in search:
        exact_match.append(row)
    if len(exact_match)>0:
        em = getEmbed(exact_match[0])
        await ctx.send(embed = em)

    elif len(songs)>5:
        with open('results.txt','w',encoding='utf-8') as resultsFile:
            for item in songs:
                resultsFile.writelines(getMessage(item))
                resultsFile.writelines('\n\n')
        await ctx.send('Too many results')
        await ctx.send(f'Here is a file with all {len(songs)}results.', file=discord.File('results.txt','results.txt'))

    elif len(songs) == 0:
        await ctx.send ('No results, try again.')
    else:
        for item in songs:
            em = getEmbed(item)
            await ctx.send(embed = em)

@bot.command(aliases = ['sa'])
async def searchartist(ctx, *, artist):
    """Look for song by artist"""
    search = AceCur.execute('Select * FROM songs WHERE artist LIKE ? or artist_translation LIKE ?', ('%'+artist+'%','%'+artist+'%'))

    songs = []
    for row in search:
        songs.append(row)
    if len(songs)>5:
        with open('results.txt','w',encoding='utf-8') as resultsFile:
            for item in songs:
                resultsFile.writelines(getMessage(item))
                resultsFile.writelines('\n\n')
        await ctx.send('Too many results')
        await ctx.send(f'Here is a file with all {len(songs)} results.', file=discord.File('results.txt','results.txt'))
    elif len(songs) == 0:
        await ctx.send ('No results, try again.')
    else:
        for item in songs:
            message = getEmbed(item)
            await ctx.send(embed = message)


@bot.command(aliases = ['bpmc', 'convert'])
async def bpmconvert(ctx, bpm, *, song):
    """convert song bpm to x format must be "?bpmc <Desired BPM> <song name>""
        example:  ?bpmc 420 max 300
    """
    search = AceCur.execute('SELECT * FROM songs WHERE title LIKE ? OR title_translation LIKE ?', ('%'+song+'%','%'+song+'%'))
    songs = []
    for row in search:
        songs.append(row)
    search = AceCur.execute('SELECT * FROM songs WHERE title = ? COLLATE NOCASE or title_translation = ?  COLLATE NOCASE', (song,song))
    exact_match = []
    for row in search:
        exact_match.append(row)
    if len(exact_match)>0:
        em = getBPMCEmbed(exact_match[0], bpm)
        await ctx.send(embed = em)

    elif len(songs)>5:
        with open('results.txt','w',encoding='utf-8') as resultsFile:
            for item in songs:
                resultsFile.writelines(getBPMCMessage(item, bpm))
                resultsFile.writelines('\n\n')
        await ctx.send('Too many results')
        await ctx.send(f'Here is a file with all {len(songs)}results.', file=discord.File('results.txt','results.txt'))

    elif len(songs) == 0:
        await ctx.send ('No results, try again.')
    else:
        for item in songs:
            em = getBPMCEmbed(item, bpm)
            await ctx.send(embed = em)

@bot.command()
async def mmod(ctx, *, song):
    """convert prefered speed to x format "?mmod <song name>"
        example:  ?mmod max 300
    """
    search = UserCur.execute('SELECT mmod FROM users WHERE id = ?', (ctx.message.author.id,))
    result = search.fetchone()
    print(result)
    if result == None or result[0]  == 0:
        await ctx.send('Mmod not set. set it by entering ?setmmod <bpm>')
        return
    else:
        bpm = result[0]

    search = AceCur.execute('SELECT * FROM songs WHERE title LIKE ? OR title_translation LIKE ?', ('%'+song+'%','%'+song+'%'))
    songs = []
    for row in search:
        songs.append(row)
    search = AceCur.execute('SELECT * FROM songs WHERE title = ? COLLATE NOCASE or title_translation = ?  COLLATE NOCASE', (song,song))
    exact_match = []
    for row in search:
        exact_match.append(row)
    if len(exact_match)>0:
        em = getBPMCEmbed(exact_match[0], bpm)
        await ctx.send(embed = em)

    elif len(songs)>5:
        with open('results.txt','w',encoding='utf-8') as resultsFile:
            for item in songs:
                resultsFile.writelines(getBPMCMessage(item, bpm))
                resultsFile.writelines('\n\n')
        await ctx.send('Too many results')
        await ctx.send(f'Here is a file with all {len(songs)}results.', file=discord.File('results.txt','results.txt'))

    elif len(songs) == 0:
        await ctx.send ('No results, try again.')
    else:
        for item in songs:
            em = getBPMCEmbed(item, bpm)
            await ctx.send(embed = em)

@bot.command()
async def setmmod(ctx, bpm):
    """ Set mmod """
    search = UserCur.execute('SELECT * FROM users WHERE id = ?', (ctx.message.author.id,))
    result = search.fetchone()
    try:
        bpm = int (bpm)
    except:
        await ctx.send('Invalid BPM')
        return
    if result == None:
        UserCur.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?)',(ctx.message.author.id, ctx.message.author.name, bpm, 0, 0))
    else:
        UserCur.execute('UPDATE users SET mmod = ? where id = ?', (bpm, ctx.message.author.id))

    UserDB.commit()
    await ctx.send('mmod set.')


def getClosestMultipiler(mul):

    if mul <.25:
        return (.25,.25)
    elif mul <.5:
        return(.25,.5)
    elif mul <.75:
        return (.5,.75)
    elif mul <1.0:
        return  (.75,1.0)
    elif mul < 1.25:
        return (1.0,1.25)
    elif mul < 1.5:
        return (1.25,1.5)
    elif mul < 1.75:
        return (1.5,1.75)
    elif mul < 2.0:
        return (1.75,2.0)
    elif mul < 2.25:
        return (2.0,2.25)
    elif mul < 2.5:
        return (2.25,2.5)
    elif mul < 2.75:
        return (2.5,2.75)
    elif mul < 3.0:
        return (2.75,3.0)
    elif mul < 3.25:
        return (3.0,3.25)
    elif mul < 3.5:
        return (3.25,3.5)
    elif mul < 3.75:
        return (3.5,3.75)
    elif mul < 4.0:
        return (3.75,4.0)
    elif mul < 4.5:
        return (4.0,4.5)
    elif mul < 5.0:
        return (4.5,5.0)
    elif mul < 5.5:
        return (5.0,5.5)
    elif mul < 6.0:
        return (5.5,6.0)
    elif mul < 6.5:
        return (6.0,6.5)
    elif mul < 7.0:
        return (6.5,7.0)
    elif mul < 7.5:
        return (7.0,7.5)
    elif mul < 8.0:
        return (7.5,8.0)
    else:
         return(8.0,8.0)




AceDB = sqlite3.connect('ace.db')
AceCur = AceDB.cursor()

UserDB = sqlite3.connect('user.db')
user_table = """CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        mmod INTEGER,
                        level INTEGER,
                        adminLevel INTEGER
                        )"""


UserCur = UserDB.cursor()
UserCur.execute(user_table)
with open ('bot_token.txt','r') as tokenfile:
    token = tokenfile.readline().strip()
bot.run(token)

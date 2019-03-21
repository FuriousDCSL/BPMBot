import json
import io
import discord
from discord.ext import commands
import random

description = '''Version one BPMbot basic functionality introduced'''
bot = commands.Bot(command_prefix='?', description=description)


def getMessage(item):
    message = 'Title:\t' +item['name']
    if len(item['name_translation'])>0:
        message += '\ntranslit:\t'+item['name_translation']
    message +='\nArtist:\t' + item['artist']
    if len(item['artist_translation']):
        message += '\ntranslit:\t' + item['artist_translation']
    message += '\nFolder:\t' + item['folder']
    message += '\nBPM:\t'+item['bpm']
    return message

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def search(ctx, *, song):
    """Look for song partial matches work. (If you type "?search 300" it will show MAX 300, X-Special and SMM Mix)"""
    songs = []
    exact_match = []
    for item in aceJSON:
        if song.lower() in item['name'].lower()  or song.lower() in item['name_translation'].lower():
            songs.append(item)
        if song.lower() == item['name'].lower()  or song.lower() == item['name_translation'].lower():
            exact_match.append(item)
    if len(songs)>5:
        if len(exact_match)>0:
            message = 'Too many results to show all. Showing exact match.\n' + getMessage(exact_match[0])
            await ctx.send(message, file=discord.File('jackets/'+exact_match[0]['jacket'],'jacket.png'))
        else:
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
            message = getMessage(item)
            await ctx.send(message, file=discord.File('jackets/'+item['jacket'],'jacket.png'))

@bot.command()
async def searchartist(ctx, *, artist):
    """Look for song by artist"""
    songs = []
    for item in aceJSON:
        if artist.lower() in item['artist'].lower()  or artist.lower() in item['artist_translation'].lower():
            jacket = 'jackets/' + item['jacket']
            songname = item['name']
            bpm = item['bpm']
            songs.append(item)

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
            message = getMessage(item)
            await ctx.send(message, file=discord.File('jackets/'+item['jacket'],'jacket.png'))

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


@bot.command()
async def bpmconvert(ctx, bpm, *, song):
    """convert song bpm to x format must be "?bpmconvert <Desired BPM> <full song name>"" use search function to get full song name
        example:  ?bpmconvert 420 max 300

        currently you will get an exact value so set it higher or lower to aprox desired bpm
    """
    for item in aceJSON:
        if song.lower() == item['name'].lower()  or song.lower() == item['name_translation'].lower():
            songbpm = item['bpm'].split('-')
            songname = item['name']
            if len(songbpm)>1:
                songtopbpm=float(songbpm[-1])
            else:
                songtopbpm =float(songbpm[0])

            wantbpm = float(bpm)
            mul = wantbpm/songtopbpm
            message = getMessage (item)
            await ctx.send(message)
            closestMul = getClosestMultipiler(mul)
            message = f'Ideal multiplier:\t{mul:.2f}\tBPM:\t{wantbpm}\nLow multiplier:\t{closestMul[0]:.2f}\tBPM:\t{closestMul[0]*songtopbpm:.2f}\nHigh multiplier:\t{closestMul[1]}\tBPM:\t{closestMul[1]*songtopbpm:.2f}\n'
            await ctx.send(message, file=discord.File('jackets/'+item['jacket'],'jacket.png'))


with io.open('ace.json', encoding='utf-8') as aceJSONFile:
    aceJSON = json.load(aceJSONFile)

bot.run('NTU2NzU5NzMwODExMzA1OTk1.D2-ahg.jEuiAJi6_yeANWMNXY2ir7GX1ZQ')

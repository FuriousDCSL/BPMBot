import json
import io
import sqlite3

def parseBPM(bpm):
    bpms = bpm.split('-')
    return [int(bpms[-1]),int(bpms[0])]

def main():
    with io.open('ace.json', encoding='utf-8') as aceJSONFile:
        aceJSON = json.load(aceJSONFile)
    try:
        conn = sqlite3.connect('ace.db')
    except Error as e:
        print(e)



    song_table = """CREATE TABLE IF NOT EXISTS songs (
                        title TEXT NOT NULL,
                        title_translation TEXT,
                        artist TEXT,
                        artist_translation TEXT,
                        alias TEXT,
                        jacket TEXT,
                        folder TEXT,
                        bpm TEXT,
                        maxBPM INTEGER,
                        minBPM INTEGER,
                        genre TEXT,
                        begSP_difficulty INTEGER,
                        begSP_shock INTEGER,
                        BSP_difficulty INTEGER,
                        BSP_shock INTEGER,
                        DSP_difficulty INTEGER,
                        DSP_shock INTEGER,
                        ESP_difficulty INTEGER,
                        ESP_shock INTEGER,
                        CSP_difficulty INTEGER,
                        CSP_shock INTEGER,
                        BDP_difficulty INTEGER,
                        BDP_shock INTEGER,
                        DDP_difficulty INTEGER,
                        DDP_shock INTEGER,
                        EDP_difficulty INTEGER,
                        EDP_shock INTEGER,
                        CDP_difficulty INTEGER,
                        CDP_shock INTEGER,
                        us_locked INTEGER,
                        unlock INTEGER)"""

    c = conn.cursor()
    c.execute(song_table)

    for item in aceJSON:
        print (item['name'])
        song = []
        song.append(item['name'])
        song.append(item['name_translation'])
        song.append(item['artist'])
        song.append(item['artist_translation'])
        song.append("")
        song.append(item['jacket'])
        song.append(item['folder'])
        song.append(item['bpm'])
        song.extend(parseBPM(item['bpm']))
        song.append(item['genre'])
        keys = item['single'].keys()
        if 'beginner' in keys and item['single']['beginner'] != None:
            song.append(item['single']['beginner']['difficulty'])
            shock = item['single']['beginner']['shock']
            if shock == '-':
                song.append(-1)
            else:
                song.append(int(shock))
        else:
             song.extend( [-1, -1])
        if 'basic' in keys and item['single']['basic'] != None:
            song.append(item['single']['basic']['difficulty'])
            shock = item['single']['basic']['shock']
            if shock == '-':
                song.append(-1)
            else:
                song.append(int(shock))
        else:
             song.extend( [-1, -1])
        if 'difficult' in keys and item['single']['difficult'] != None:
            song.append(item['single']['difficult']['difficulty'])
            shock = item['single']['difficult']['shock']
            if shock == '-':
                song.append(-1)
            else:
                song.append(int(shock))
        else:
             song.extend( [-1, -1])
        if 'expert' in keys and item['single']['expert'] != None:
            song.append(item['single']['expert']['difficulty'])
            shock = item['single']['expert']['shock']
            if shock == '-':
                song.append(-1)
            else:
                song.append(int(shock))
        else:
             song.extend( [-1, -1])
        if 'challenge' in keys and item['single']['challenge'] != None:
            song.append(item['single']['challenge']['difficulty'])
            shock = item['single']['challenge']['shock']
            if shock == '-':
                song.append(-1)
            else:
                song.append(int(shock))
        else:
             song.extend( [-1, -1])
        keys = item['double'].keys()

        if 'basic' in keys and item['double']['basic'] != None:
            song.append(item['double']['basic']['difficulty'])
            shock = item['double']['basic']['shock']
            if shock == '-':
                song.append(-1)
            else:
                song.append(int(shock))
        else:
             song.extend( [-1, -1])
        if 'difficult' in keys and item['double']['difficult'] != None:
            song.append(item['double']['difficult']['difficulty'])
            shock = item['double']['difficult']['shock']
            if shock == '-':
                song.append(-1)
            else:
                song.append(int(shock))
        else:
             song.extend( [-1, -1])
        if 'expert' in keys and item['double']['expert'] != None:
            song.append(item['double']['expert']['difficulty'])
            shock = item['double']['expert']['shock']
            if shock == '-':
                song.append(-1)
            else:
                song.append(int(shock))
        else:
             song.extend( [-1, -1])
        if 'challenge' in keys and item['double']['challenge'] != None:
            song.append(item['double']['challenge']['difficulty'])
            shock = item['double']['challenge']['shock']
            if shock == '-':
                song.append(-1)
            else:
                song.append(int(shock))
        else:
             song.extend( [-1, -1])
        keys = item.keys()
        if 'us_locked' in keys and item['us_locked']:
            song.append(1)
        else:
            song.append(0)
        if 'unlock' in keys and item['unlock']:
            song.append(1)
        else:
            song.append(0)

        c.execute('INSERT INTO songs VALUES (?, ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', song)

    conn.commit()
    c.close()
if __name__ == '__main__':
    main()

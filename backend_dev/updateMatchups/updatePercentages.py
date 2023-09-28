import pandas as pd
import json

matchups = []
filenameRead = "./percentages.txt"

fileRead = open(filenameRead, "r")


wholeFile = fileRead.readlines()
groups = {'AFCNorth': ['Ravens', 'Bengals', 'Browns', 'Steelers'], 'AFCSouth': ['Titans', 'Colts', 'Jaguars', 'Texans'], 'AFCEast': ['Bills', 'Jets', 'Dolphins', 'Patriots'], 'AFCWest': ['Cheifs', 'Chargers', 'Broncos', 'Raiders'], 'AFC': ['Ravens', 'Bengals', 'Browns', 'Steelers', 'Titans', 'Colts', 'Jaguars', 'Texans', 'Bills', 'Jets', 'Dolphins', 'Patriots', 'Cheifs', 'Chargers', 'Broncos', 'Raiders'], 'NFCNorth': ['Vikings', 'Packers', 'Bears', 'Lions'], 'NFCSouth': ['Buccaneers', 'Falcons', 'Saints', 'Panthers'], 'NFCEast': ['Cowboys', 'Giants', 'Eagles', 'Commanders'], 'NFCWest': ['49ers', 'Rams', 'Seahawks', 'Cardinals'], 'NFC': ['Vikings', 'Packers', 'Bears', 'Lions', 'Buccaneers', 'Falcons', 'Saints', 'Panthers', 'Cowboys', 'Giants', 'Eagles', 'Commanders', '49ers', 'Rams', 'Seahawks', 'Cardinals']}
results = {'AFC':[0,0], 'AFCNorth':[0,0], 'AFCSouth':[0,0], 'AFCEast':[0,0], 'AFCWest':[0,0], 'NFC':[0,0], 'NFCNorth':[0,0], 'NFCSouth':[0,0], 'NFCEast':[0,0], 'NFCWest':[0,0]}
week = 0
year = 0

for line in wholeFile:
    data = line.split(',')

    if len(data) > 1:
        awayTeam = data[0]
        homeTeam = data[1]
        winner = data[2]
        outcome = data[-1][0]

        if outcome == '1':
            if awayTeam not in results:
                results[awayTeam] = [100,1]
            else:
                results[awayTeam] = [results[awayTeam][0] + 100, results[awayTeam][1] + 1]

            if homeTeam not in results:
                results[homeTeam] = [100,1]
            else:
                results[homeTeam] = [results[homeTeam][0] + 100, results[homeTeam][1] + 1]


            if awayTeam in groups['AFC']:
                results['AFC'] = [results['AFC'][0]  + 100, results['AFC'][1] + 1]

                if awayTeam in groups['AFCNorth']:
                    results['AFCNorth'] = [results['AFCNorth'][0]  + 100, results['AFCNorth'][1] + 1]
                elif awayTeam in groups['AFCSouth']:
                    results['AFCSouth'] = [results['AFCSouth'][0]  + 100, results['AFCSouth'][1] + 1]
                elif awayTeam in groups['AFCEast']:
                    results['AFCEast'] = [results['AFCEast'][0]  + 100, results['AFCEast'][1] + 1]
                elif awayTeam in groups['AFCWest']:
                    results['AFCWest'] = [results['AFCWest'][0]  + 100, results['AFCWest'][1] + 1]

            elif awayTeam in groups['NFC']:
                results['NFC'] = [results['NFC'][0]  + 100, results['NFC'][1] + 1]

                if awayTeam in groups['NFCNorth']:
                    results['NFCNorth'] = [results['NFCNorth'][0]  + 100, results['NFCNorth'][1] + 1]
                elif awayTeam in groups['NFCSouth']:
                    results['NFCSouth'] = [results['NFCSouth'][0]  + 100, results['NFCSouth'][1] + 1]
                elif awayTeam in groups['NFCEast']:
                    results['NFCEast'] = [results['NFCEast'][0]  + 100, results['NFCEast'][1] + 1]
                elif awayTeam in groups['NFCWest']:
                    results['NFCWest'] = [results['NFCWest'][0]  + 100, results['NFCWest'][1] + 1]

            if homeTeam in groups['AFC']:
                results['AFC'] = [results['AFC'][0]  + 100, results['AFC'][1] + 1]

                if homeTeam in groups['AFCNorth']:
                    results['AFCNorth'] = [results['AFCNorth'][0]  + 100, results['AFCNorth'][1] + 1]
                elif homeTeam in groups['AFCSouth']:
                    results['AFCSouth'] = [results['AFCSouth'][0]  + 100, results['AFCSouth'][1] + 1]
                elif homeTeam in groups['AFCEast']:
                    results['AFCEast'] = [results['AFCEast'][0]  + 100, results['AFCEast'][1] + 1]
                elif homeTeam in groups['AFCWest']:
                    results['AFCWest'] = [results['AFCWest'][0]  + 100, results['AFCWest'][1] + 1]

            elif homeTeam in groups['NFC']:
                results['NFC'] = [results['NFC'][0]  + 100, results['NFC'][1] + 1]

                if homeTeam in groups['NFCNorth']:
                    results['NFCNorth'] = [results['NFCNorth'][0]  + 100, results['NFCNorth'][1] + 1]
                elif homeTeam in groups['NFCSouth']:
                    results['NFCSouth'] = [results['NFCSouth'][0]  + 100, results['NFCSouth'][1] + 1]
                elif homeTeam in groups['NFCEast']:
                    results['NFCEast'] = [results['NFCEast'][0]  + 100, results['NFCEast'][1] + 1]
                elif homeTeam in groups['NFCWest']:
                    results['NFCWest'] = [results['NFCWest'][0]  + 100, results['NFCWest'][1] + 1]

            results[f'{year} Week {week}'] = [results[f'{year} Week {week}'][0] + 100, results[f'{year} Week {week}'][1] + 1]

        else:
            if awayTeam not in results:
                results[awayTeam] = [0,1]
            else:
                results[awayTeam] = [results[awayTeam][0] + 0, results[awayTeam][1] + 1]

            if homeTeam not in results:
                results[homeTeam] = [0,1]
            else:
                results[homeTeam] = [results[homeTeam][0] + 0, results[homeTeam][1] + 1]


            if awayTeam in groups['AFC']:
                results['AFC'] = [results['AFC'][0]  + 0, results['AFC'][1] + 1]

                if awayTeam in groups['AFCNorth']:
                    results['AFCNorth'] = [results['AFCNorth'][0]  + 0, results['AFCNorth'][1] + 1]
                elif awayTeam in groups['AFCSouth']:
                    results['AFCSouth'] = [results['AFCSouth'][0]  + 0, results['AFCSouth'][1] + 1]
                elif awayTeam in groups['AFCEast']:
                    results['AFCEast'] = [results['AFCEast'][0]  + 0, results['AFCEast'][1] + 1]
                elif awayTeam in groups['AFCWest']:
                    results['AFCWest'] = [results['AFCWest'][0]  + 0, results['AFCWest'][1] + 1]

            elif awayTeam in groups['NFC']:
                results['NFC'] = [results['NFC'][0]  + 0, results['NFC'][1] + 1]

                if awayTeam in groups['NFCNorth']:
                    results['NFCNorth'] = [results['NFCNorth'][0]  + 0, results['NFCNorth'][1] + 1]
                elif awayTeam in groups['NFCSouth']:
                    results['NFCSouth'] = [results['NFCSouth'][0]  + 0, results['NFCSouth'][1] + 1]
                elif awayTeam in groups['NFCEast']:
                    results['NFCEast'] = [results['NFCEast'][0]  + 0, results['NFCEast'][1] + 1]
                elif awayTeam in groups['NFCWest']:
                    results['NFCWest'] = [results['NFCWest'][0]  + 0, results['NFCWest'][1] + 1]

            if homeTeam in groups['AFC']:
                results['AFC'] = [results['AFC'][0]  + 0, results['AFC'][1] + 1]

                if homeTeam in groups['AFCNorth']:
                    results['AFCNorth'] = [results['AFCNorth'][0]  + 0, results['AFCNorth'][1] + 1]
                elif homeTeam in groups['AFCSouth']:
                    results['AFCSouth'] = [results['AFCSouth'][0]  + 0, results['AFCSouth'][1] + 1]
                elif homeTeam in groups['AFCEast']:
                    results['AFCEast'] = [results['AFCEast'][0]  + 0, results['AFCEast'][1] + 1]
                elif homeTeam in groups['AFCWest']:
                    results['AFCWest'] = [results['AFCWest'][0]  + 0, results['AFCWest'][1] + 1]

            elif homeTeam in groups['NFC']:
                results['NFC'] = [results['NFC'][0]  + 0, results['NFC'][1] + 1]

                if homeTeam in groups['NFCNorth']:
                    results['NFCNorth'] = [results['NFCNorth'][0]  + 0, results['NFCNorth'][1] + 1]
                elif homeTeam in groups['NFCSouth']:
                    results['NFCSouth'] = [results['NFCSouth'][0]  + 0, results['NFCSouth'][1] + 1]
                elif homeTeam in groups['NFCEast']:
                    results['NFCEast'] = [results['NFCEast'][0]  + 0, results['NFCEast'][1] + 1]
                elif homeTeam in groups['NFCWest']:
                    results['NFCWest'] = [results['NFCWest'][0]  + 0, results['NFCWest'][1] + 1]

            results[f'{year} Week {week}'] = [results[f'{year} Week {week}'][0] + 0, results[f'{year} Week {week}'][1] + 1]

    else:
        weekOrYear = data[0][:-1]
        if weekOrYear == '2022':
            year = 2022
        elif weekOrYear == '2023':
            year = 2023
        else:
            week = weekOrYear
            results[f'{year} Week {week}'] = [0,0]




finalResults = {}
for team in results:
    finalResults[team] = round(results[team][0]/results[team][1],2)


filenameWrite = "./percentages.json"
with open(filenameWrite, "w") as outfile:
    json.dump(finalResults, outfile)


fileRead.close()





print('Here we go')



data = {'New York Knicks': [['-1','-115'],['214.5','-112'],'-118'], 'Cleveland Cavaliers': [['+1','-105'],['214.5','-108'],'-102'], 'San Antonio Spurs': [['+7','-112'],['225.5','-110'],'+230'], 'Pheniox Suns':[['-7','-108'],['225.5','-110'],'-285'], 'Orlando Magic':[['+6','-108'],['220','-110'],'+210'], 'Los Angles Clippers':[['-6','-112'],['220','-110'],'-258']}

for team in data: 
    spread, overUnder, moneyLine = data[team]
    favored = 0
    spreadLine, spreadOdds = spread
    overUnderLine, overUnderOdds = overUnder
    if int(spreadLine) < 0:
        favored = 1
    

    print(f'{team}    =>      Spread => {spreadLine} {spreadOdds}    OU => {overUnderLine} {overUnderOdds}    ML => {moneyLine} favored => {favored}')

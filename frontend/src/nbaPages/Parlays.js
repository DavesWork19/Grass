import '../Fonts.css';
import { useLayoutEffect } from 'react';
import { todaysGames } from './todaysGames';
import { legalNbaTeamLogos } from '../constants';

const Parlays = (props) => {
  useLayoutEffect(() => {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth',
    });
  });
  const parlay = props.parlay;

  const parlays = [];

  for (let i = 0; i < parlay.length; i++) {
    const parlayValues = parlay[i].split(',');
    for (let j = 2; j < todaysGames.length; j++) {
      if (todaysGames[j].includes(parlayValues[0])) {
        const todaysGameValues = todaysGames[j].split(',');
        if (parlayValues[2] === 'spread') {
          if (parlayValues[3] === '1') {
            parlays.push(
              `${todaysGameValues[0]}_${todaysGameValues[2]}_${todaysGameValues[3]}_${todaysGameValues[4]}_Ride`
            );
          } else if (parlayValues[3] === '0') {
            parlays.push(
              `${todaysGameValues[0]}_${todaysGameValues[2]}_${todaysGameValues[3]}_${todaysGameValues[4]}_Fade`
            );
          }
        } else if (parlayValues[2] === 'overUnder') {
          if (parlayValues[3] === '1') {
            parlays.push(
              `${todaysGameValues[0]}_${todaysGameValues[1]}_${todaysGameValues[2]}_${todaysGameValues[5]}_Over`
            );
          } else if (parlayValues[3] === '0') {
            parlays.push(
              `${todaysGameValues[0]}_${todaysGameValues[1]}_${todaysGameValues[2]}_${todaysGameValues[5]}_Under`
            );
          }
        }
      }
    }
  }

  return (
    <div className='border border-bottom-0 border-secondary rounded'>
      <div>
        {parlays.map((data) => {
          const [time, team1, team2, line, overUnderCall] = data.split('_');

          const updatedTeam2 =
            team2.includes('-') || team2.includes('+')
              ? team2
              : legalNbaTeamLogos[team2];

          let updatedLine = -1;
          if (line === '0') {
            updatedLine = 'Not Cover';
          } else if (line === '1') {
            updatedLine = 'Cover';
          } else {
            updatedLine = line;
          }

          return (
            <div key={data} className='container-fluid'>
              <div className='row border-bottom border-secondary rounded'>
                <span className='col-2'>{time.slice(0, time.length - 1)}</span>
                <span className='col-3'>{legalNbaTeamLogos[team1]}</span>
                <span className='col-3'>{updatedTeam2}</span>
                <span className='col-2'>{updatedLine}</span>
                <span className='col-2'>{overUnderCall}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Parlays;

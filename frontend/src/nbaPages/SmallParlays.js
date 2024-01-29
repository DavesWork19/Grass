import '../Fonts.css';
import { useLayoutEffect } from 'react';
import { todaysGames } from './todaysGames';
import { smallParlay } from './smallParlay';

const SmallParlays = () => {
  useLayoutEffect(() => {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth',
    });
  });

  const parlays = [];

  for (let i = 0; i < smallParlay.length; i++) {
    const smallParlayValue = smallParlay[i].split(',');
    for (let j = 2; j < todaysGames.length; j++) {
      const todaysGameValues = todaysGames[j].split(',');
      if (todaysGames[j].includes(smallParlayValue[0])) {
        if (smallParlayValue[2] === 'spread') {
          if (smallParlayValue[3] === '1') {
            parlays.push(
              `${todaysGameValues[0]}_ _${smallParlayValue[0]}_${todaysGameValues[3]}_Cover`
            );
          } else if (smallParlayValue[3] === '0') {
            parlays.push(
              `${todaysGameValues[0]}_ _${smallParlayValue[0]}_${todaysGameValues[3]}_Not Cover`
            );
          }
        } else if (smallParlayValue[2] === 'overUnder') {
          if (smallParlayValue[3] === '1') {
            parlays.push(
              `${todaysGameValues[0]}_${todaysGameValues[1]}_${todaysGameValues[2]}_${todaysGameValues[5]}_Over`
            );
          } else if (smallParlayValue[3] === '0') {
            parlays.push(
              `${todaysGameValues[0]}_${todaysGameValues[1]}_${todaysGameValues[2]}_${todaysGameValues[5]}_Under`
            );
          }
        }
      }
    }
  }

  return (
    <div className='border border-dark rounded'>
      <div>
        {parlays.map((data) => {
          const [time, team1, team2, overUnderLine, overUnderCall] =
            data.split('_');
          if (team1 !== ' ') {
            return (
              <div key={data} className='row'>
                <span className='col-2'>
                  {time.slice(0, time.length - 1)}
                  {' PM EST'}
                </span>
                <span className='col-3'>{team1}</span>
                <span className='col-3'>{team2}</span>
                <span className='col-2'>{overUnderLine}</span>
                <span className='col-2'>{overUnderCall}</span>
              </div>
            );
          } else {
            return (
              <div key={data} className='row'>
                <span className='col-2'>
                  {time.slice(0, time.length - 1)}
                  {' PM EST'}
                </span>
                <span className='col-6'>{team2}</span>
                <span className='col-2'>{overUnderLine}</span>
                <span className='col-2'>{overUnderCall}</span>
              </div>
            );
          }
        })}
      </div>
    </div>
  );
};

export default SmallParlays;

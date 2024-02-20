import '../Fonts.css';
import { todaysGames } from './todaysGames';
import { legalNbaTeamLogos } from '../constants';

const Parlays = (props) => {
  const parlay = props.parlay;

  const parlays = [];

  for (let i = 0; i < parlay.length; i++) {
    const parlayValues = parlay[i].split(',');
    for (let j = 2; j < todaysGames.length; j++) {
      if (todaysGames[j].includes(parlayValues[0])) {
        const todaysGameValues = todaysGames[j].split(',');
        if (parlayValues[2] === 'spread') {
          if (parlayValues[3] === '1') {
            if (todaysGameValues[4] === '1') {
              parlays.push(
                `${todaysGameValues[0]}_${todaysGameValues[2]}_${todaysGameValues[3]}_Cover_Ride`
              );
            } else if (todaysGameValues[4] === '0') {
              parlays.push(
                `${todaysGameValues[0]}_${todaysGameValues[2]}_${todaysGameValues[3]}_Not Cover_Ride`
              );
            }
          } else if (parlayValues[3] === '0') {
            if (todaysGameValues[4] === '1') {
              parlays.push(
                `${todaysGameValues[0]}_${todaysGameValues[2]}_${todaysGameValues[3]}_Cover_Fade`
              );
            } else if (todaysGameValues[4] === '0') {
              parlays.push(
                `${todaysGameValues[0]}_${todaysGameValues[2]}_${todaysGameValues[3]}_Not Cover_Fade`
              );
            }
          }
        } else if (parlayValues[2] === 'overUnder') {
          if (parlayValues[3] === '1') {
            if (todaysGameValues[6] === '1') {
              parlays.push(
                `${todaysGameValues[0]}_${todaysGameValues[2]}_${todaysGameValues[5]}_Over_Ride`
              );
            } else if (todaysGameValues[6] === '0') {
              parlays.push(
                `${todaysGameValues[0]}_${todaysGameValues[2]}_${todaysGameValues[5]}_Under_Ride`
              );
            }
          } else if (parlayValues[3] === '0') {
            if (todaysGameValues[6] === '1') {
              parlays.push(
                `${todaysGameValues[0]}_${todaysGameValues[2]}_${todaysGameValues[5]}_Over_Fade`
              );
            } else if (todaysGameValues[6] === '0') {
              parlays.push(
                `${todaysGameValues[0]}_${todaysGameValues[2]}_${todaysGameValues[5]}_Under_Fade`
              );
            }
          }
        }
      }
    }
  }

  return (
    <div className='border border-bottom-0 border-secondary rounded'>
      <div>
        {parlays.map((data) => {
          const [time, team, line, coverOrNot, rideOrNot] = data.split('_');
          return (
            <div key={data} className='container-fluid'>
              <div className='row border-bottom border-secondary rounded'>
                <span className='col-2'>{time.slice(0, time.length - 1)}</span>
                <span className='col-3'>{legalNbaTeamLogos[team]}</span>
                <span className='col-3'>{line}</span>
                <span className='col-2'>{coverOrNot}</span>
                <span className='col-2'>{rideOrNot}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Parlays;

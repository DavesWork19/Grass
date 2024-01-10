import { useState } from 'react';
import TeamInfo from '../nflPages/TeamInfo';
import { percentages } from './percentages';
import { todaysGames } from './todaysGames';
import '../Fonts.css';

const OverallPercents = (props) => {
  const [showPercentages, setShowPercentages] = useState(false);

  const spread = percentages['overall_spread'];
  const overUnder = percentages['overall_overUnder'];
  const parlay = percentages['overall_parlay'];
  const today = todaysGames.slice(0, 1)[0];

  const daySpread = percentages[`overall_${today}_spread`];
  const dayOverUnder = percentages[`overall_${today}_overUnder`];
  const dayParlay = percentages[`overall_${today}_parlay`];

  const hours = props.hours;
  const hoursArray = [...hours];

  const handleShowPercentages = () => {
    setShowPercentages(true);
  };

  const handleTooManyPercentages = () => {
    setShowPercentages(false);
  };

  return (
    <div className='lightText me-2'>
      {showPercentages ? (
        <div className='row'>
          <div className='col-12'>
            <button
              className='btn btn-light'
              onClick={handleTooManyPercentages}
            >
              {'Too Many Percentages'}
            </button>
            <TeamInfo info={{ title: 'Overall Spread', percent: spread }} />
            <TeamInfo
              info={{ title: 'Overall Over Under', percent: overUnder }}
            />
            <TeamInfo info={{ title: 'Overall Parlay', percent: parlay }} />
            <TeamInfo
              info={{
                title: `Overall Spreads on ${today}`,
                percent: daySpread,
              }}
            />
            <TeamInfo
              info={{
                title: `Overall Over Unders on ${today}`,
                percent: dayOverUnder,
              }}
            />
            <TeamInfo
              info={{
                title: `Overall Parlays on ${today}`,
                percent: dayParlay,
              }}
            />
            {hoursArray.map((hour) => (
              <div key={hour}>
                <TeamInfo
                  info={{
                    title: `Overall Spread at ${hour}`,
                    percent:
                      percentages[`overall_Time_${hour}_${hour}59_spread`],
                  }}
                />
                <TeamInfo
                  info={{
                    title: `Overall Over Under at ${hour}`,
                    percent:
                      percentages[`overall_Time_${hour}_${hour}59_overUnder`],
                  }}
                />
                <TeamInfo
                  info={{
                    title: `Overall Parlay at ${hour}`,
                    percent:
                      percentages[`overall_Time_${hour}_${hour}59_parlay`],
                  }}
                />
              </div>
            ))}
          </div>
        </div>
      ) : (
        <button className='btn btn-light' onClick={handleShowPercentages}>
          {'Show Overall Percentages'}
        </button>
      )}
    </div>
  );
};

export default OverallPercents;

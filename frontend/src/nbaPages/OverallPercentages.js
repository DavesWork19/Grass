import { useState } from 'react';
import TeamInfo from '../nflPages/TeamInfo';
import { percentages } from './percentages';
import { todaysGames } from './todaysGames';
import '../Fonts.css';

const OverallPercents = () => {
  const [showPercentages, setShowPercentages] = useState(false);

  const spread = percentages['overall_spread'];
  const overUnder = percentages['overall_overUnder'];
  const parlay = percentages['overall_parlay'];
  const today = todaysGames.slice(0, 1)[0];
  const daySpread = percentages[`overall_${today}_spread`];
  const dayOverUnder = percentages[`overall_${today}_overUnder`];
  const dayParlay = percentages[`overall_${today}_parlay`];

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
            <TeamInfo info={{ title: 'Overall Spread', percent: spread }} />
            <TeamInfo
              info={{ title: 'Overall Over Under', percent: overUnder }}
            />
            <TeamInfo info={{ title: 'Overall Parlay', percent: parlay }} />
            <TeamInfo
              info={{ title: `Spreads on ${today}`, percent: daySpread }}
            />
            <TeamInfo
              info={{ title: `Over Unders on ${today}`, percent: dayOverUnder }}
            />
            <TeamInfo
              info={{ title: `Parlays on ${today}`, percent: dayParlay }}
            />
          </div>
          <button className='btn btn-light' onClick={handleTooManyPercentages}>
            Too Many Percentages
          </button>
        </div>
      ) : (
        <div className='row'>
          <button className='btn btn-light' onClick={handleShowPercentages}>
            {'Overall Percentages'}
          </button>
        </div>
      )}
    </div>
  );
};

export default OverallPercents;

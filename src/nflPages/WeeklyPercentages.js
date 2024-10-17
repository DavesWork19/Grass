import { useState } from 'react';
import percentages from './percentages.json';
import './HomePagePercentages.css';
import '../Fonts.css';

const WeeklyPercents = () => {
  const [weeklyPercent2022, setWeeklyPercent2022] = useState(false);
  const [weeklyPercent2023, setWeeklyPercent2023] = useState(false);
  const weekArray2022 = [];
  const weekArray2023 = [];
  const showAllPercents = !weeklyPercent2022 && !weeklyPercent2023;

  for (const line in percentages) {
    if (line.includes('Week')) {
      if (line.includes('2022')) {
        weekArray2022.push(line);
      } else if (line.includes('2023')) {
        weekArray2023.push(line);
      }
    }
  }

  const handle2022Percentages = () => {
    setWeeklyPercent2022(true);
  };
  const handle2023Percentages = () => {
    setWeeklyPercent2023(true);
  };

  const handleShowAllPercentages = () => {
    setWeeklyPercent2022(false);
    setWeeklyPercent2023(false);
  };

  return (
    <div className='lightText me-2'>
      {showAllPercents ? (
        <div className='row'>
          <button
            className='btn btn-light col-12 col-md-6'
            onClick={handle2022Percentages}
          >
            {'2022 Weekly Percentages'}
          </button>
          <button
            className='btn btn-light col-12 col-md-6'
            onClick={handle2023Percentages}
          >
            {'2023 Weekly Percentages'}
          </button>
        </div>
      ) : (
        <div className='row'>
          <div className='col-12'>
            {weeklyPercent2022
              ? weekArray2022.map((weekData) => {
                  const weekTitle = `${weekData.split(' ')[1]} ${
                    weekData.split(' ')[2]
                  }`;

                  return (
                    <span className='d-inline-block me-2' key={weekData}>
                      <div className='border-bottom'>{weekTitle}</div>
                      <div>{percentages[weekData].toFixed(2)}</div>
                    </span>
                  );
                })
              : null}
            {weeklyPercent2023
              ? weekArray2023.map((weekData) => {
                  const weekTitle = `${weekData.split(' ')[1]} ${
                    weekData.split(' ')[2]
                  }`;

                  return (
                    <span className='d-inline-block me-2' key={weekData}>
                      <div className='border-bottom'>{weekTitle}</div>
                      <div>{percentages[weekData].toFixed(2)}</div>
                    </span>
                  );
                })
              : null}
          </div>
          <button
            className='btn btn-light col-12'
            onClick={handleShowAllPercentages}
          >
            Show All Percentages
          </button>
        </div>
      )}
    </div>
  );
};

export default WeeklyPercents;

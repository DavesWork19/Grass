import '../Fonts.css';
import { percentages } from '../nbaPages/percentages';
import { todaysGames } from '../nbaPages/todaysGames';
import PercentDataTableGameDayRow from '../percentDataTableComps/PercentDataTableGameDayRow';

const PercentDataTable = (props) => {
  const title = props.title;
  const percentagesName = props.percentagesName;
  const hours = props.hours;
  const checksAndXs = props?.checksAndXs;
  const hoursArray = [...hours];
  const today = todaysGames.slice(0, 1)[0];

  const addPercentText = (text) => `${text}%`;

  const checkNA = (value) => {
    return value === 'NA' ? value : value.toFixed(2);
  };

  const spread = addPercentText(
    checkNA(percentages[`${percentagesName}_spread`])
  );
  const overUnder = addPercentText(
    checkNA(percentages[`${percentagesName}_overUnder`])
  );
  const parlay = addPercentText(
    checkNA(percentages[`${percentagesName}_parlay`])
  );

  const daySpread = addPercentText(
    checkNA(percentages[`${percentagesName}_${today}_spread`])
  );
  const dayOverUnder = addPercentText(
    checkNA(percentages[`${percentagesName}_${today}_overUnder`])
  );
  const dayParlay = addPercentText(
    checkNA(percentages[`${percentagesName}_${today}_parlay`])
  );

  const spread1dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_spread_1`])
  );
  const overUnder1dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_overUnder_1`])
  );
  const parlay1dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_parlay_1`])
  );
  const spread2dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_spread_2`])
  );
  const overUnder2dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_overUnder_2`])
  );
  const parlay2dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_parlay_2`])
  );
  const spread3dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_spread_3`])
  );
  const overUnder3dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_overUnder_3`])
  );
  const parlay3dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_parlay_3`])
  );
  const spread4dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_spread_4`])
  );
  const overUnder4dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_overUnder_4`])
  );
  const parlay4dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_parlay_4`])
  );
  const spread5dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_spread_5`])
  );
  const overUnder5dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_overUnder_5`])
  );
  const parlay5dayago = addPercentText(
    checkNA(percentages[`${percentagesName}_last_games_parlay_5`])
  );

  const gameDay1Text = checksAndXs ? ' Game Ago' : ' Day Ago';
  const gameDayText = checksAndXs ? ' Games Ago' : ' Days Ago';

  const headingText =
    'col-4 tableHeaderNormalWeight text-start text-sm-center ps-1';
  const headingSpreadText = checksAndXs
    ? 'col-3 pe-0 text-end tableHeaderNormalWeight'
    : 'col-3 pe-0 text-end pe-lg-3 tableHeaderNormalWeight';
  const spreadText = 'col-3 text-start ps-2 text-sm-center';

  const overUnderText = checksAndXs
    ? 'col-3 text-start ps-1 ps-sm-3'
    : 'col-3 text-start ps-1 ps-sm-3 ps-lg-5';
  const parlayText = 'col-2 text-start p-0';

  return (
    <div className='container bg-dark rounded p-3 pt-0'>
      <div className='row'>
        <div className='col-12'>
          <h2 className='py-3 boldText lightText'>{title}</h2>
        </div>
      </div>

      <div className='row bg-black rounded py-1'>
        <div className='col-3'></div>
        <div className={headingSpreadText}>{'Spread'}</div>
        <div className='col-4 tableHeaderNormalWeight text-sm-center'>
          {'Over Under'}
        </div>
        <div className='col-2 tableHeaderNormalWeight text-start p-0'>
          {'Parlay'}
        </div>
      </div>
      <div className='row'>
        <div className='col-12 p-3'></div>
      </div>
      <div className='row bg-black py-1 rounded-top border-bottom border-dark'>
        <div className={headingText}>{'Overall'}</div>
        <div className={spreadText}>{spread}</div>
        <div className={overUnderText}>{overUnder}</div>
        <div className={parlayText}>{parlay}</div>
      </div>
      {hoursArray.map((hour) => (
        <div className='row bg-black py-1 border-bottom border-dark' key={hour}>
          <div className={headingText}>{`At ${hour}PM`}</div>
          <div className={spreadText}>
            {addPercentText(
              checkNA(
                percentages[`${percentagesName}_Time_${hour}_${hour}59_spread`]
              )
            )}
          </div>
          <div className={overUnderText}>
            {addPercentText(
              checkNA(
                percentages[
                  `${percentagesName}_Time_${hour}_${hour}59_overUnder`
                ]
              )
            )}
          </div>
          <div className={parlayText}>
            {addPercentText(
              checkNA(
                percentages[`${percentagesName}_Time_${hour}_${hour}59_parlay`]
              )
            )}
          </div>
        </div>
      ))}
      <div className='row bg-black py-1 rounded-bottom'>
        <div className={headingText}>{today}</div>
        <div className={spreadText}>{daySpread}</div>
        <div className={overUnderText}>{dayOverUnder}</div>
        <div className={parlayText}>{dayParlay}</div>
      </div>
      <div className='row'>
        <div className='col-12 p-3'></div>
      </div>
      <PercentDataTableGameDayRow
        data={{
          title: `1 ${gameDay1Text}`,
          spread: spread1dayago,
          overUnder: overUnder1dayago,
          parlay: parlay1dayago,
          checksAndXs,
        }}
      />
      <PercentDataTableGameDayRow
        data={{
          title: `2 ${gameDayText}`,
          spread: spread2dayago,
          overUnder: overUnder2dayago,
          parlay: parlay2dayago,
          checksAndXs,
        }}
      />
      <PercentDataTableGameDayRow
        data={{
          title: `3 ${gameDayText}`,
          spread: spread3dayago,
          overUnder: overUnder3dayago,
          parlay: parlay3dayago,
          checksAndXs,
        }}
      />
      <PercentDataTableGameDayRow
        data={{
          title: `4 ${gameDayText}`,
          spread: spread4dayago,
          overUnder: overUnder4dayago,
          parlay: parlay4dayago,
          checksAndXs,
        }}
      />
      <PercentDataTableGameDayRow
        data={{
          title: `5 ${gameDayText}`,
          spread: spread5dayago,
          overUnder: overUnder5dayago,
          parlay: parlay5dayago,
          checksAndXs,
        }}
      />
    </div>
  );
};

export default PercentDataTable;

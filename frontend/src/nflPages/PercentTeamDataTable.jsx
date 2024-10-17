import '../Fonts.css';
import percentages from './percentages.json';

const PercentTeamDataTable = (props) => {
  const team = props.team;
  const homeTeam = props.homeTeam;
  const weekDay = props.weekDay.split(',')[0];
  const time = props.time;
  const checksAndXs = props?.checksAndXs;

  const day = weekDay.slice(0, 3);

  const hours = time.split(' ')[0];
  const ampm = time.split(' ')[1];
  const updatedHours =
    ampm === 'PM' ? +hours.split(':')[0] + 12 : hours.split(':')[0];

  const addPercentText = (text) => (text !== 'NA' ? `${text}%` : 'N/A');

  const checkNA = (value) => {
    return value === -1 ? 'NA' : value.toFixed(2);
  };

  const spread = addPercentText(checkNA(percentages[`${team}_spread`]));
  const overUnder = addPercentText(checkNA(percentages[`${team}_total`]));
  const parlay = addPercentText(checkNA(percentages[`${team}_parlay`]));

  const homeSpread = addPercentText(
    checkNA(percentages[`${team}_home_spread`])
  );
  const homeOverUnder = addPercentText(
    checkNA(percentages[`${team}_home_total`])
  );
  const homeParlay = addPercentText(
    checkNA(percentages[`${team}_home_parlay`])
  );

  const awaySpread = addPercentText(
    checkNA(percentages[`${team}_away_spread`])
  );
  const awayOverUnder = addPercentText(
    checkNA(percentages[`${team}_away_total`])
  );
  const awayParlay = addPercentText(
    checkNA(percentages[`${team}_away_parlay`])
  );

  const location = homeTeam ? 'Home' : 'Away';
  const locationSpread = homeTeam ? homeSpread : awaySpread;
  const locationOverUnder = homeTeam ? homeOverUnder : awayOverUnder;
  const locationParlay = homeTeam ? homeParlay : awayParlay;

  const daySpread = addPercentText(
    checkNA(percentages[`${team}_${day}_spread`])
  );
  const dayOverUnder = addPercentText(
    checkNA(percentages[`${team}_${day}_total`])
  );
  const dayParlay = addPercentText(
    checkNA(percentages[`${team}_${day}_parlay`])
  );

  const timeSpread = addPercentText(
    checkNA(percentages[`${team}_${updatedHours}_spread`])
  );
  const timeOverUnder = addPercentText(
    checkNA(percentages[`${team}_${updatedHours}_total`])
  );
  const timeParlay = addPercentText(
    checkNA(percentages[`${team}_${updatedHours}_parlay`])
  );

  const headingText =
    'col-4 tableHeaderNormalWeight text-start text-sm-center ps-1';
  const headingSpreadText = checksAndXs
    ? 'col-3 pe-0 text-end tableHeaderNormalWeight'
    : 'col-3 pe-0 text-end pe-lg-3 tableHeaderNormalWeight';
  const spreadText = 'col-3 text-start ps-2 text-sm-center';
  const overUnderText = checksAndXs
    ? 'col-3 text-start ps-1 ps-sm-3'
    : 'col-3 text-start ps-1 ps-sm-3';
  const parlayText = 'col-2 text-start p-0';

  return (
    <div className='container bg-dark rounded p-3 pt-0'>
      <div className='row'>
        <div className='col-12'>
          <h2 className='py-3 boldText lightText'>{team}</h2>
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
        <div className={headingText}>{'Team'}</div>
        <div className={spreadText}>{spread}</div>
        <div className={overUnderText}>{overUnder}</div>
        <div className={parlayText}>{parlay}</div>
      </div>
      <div className='row bg-black py-1 border-bottom border-dark'>
        <div className={headingText}>{location}</div>
        <div className={spreadText}>{locationSpread}</div>
        <div className={overUnderText}>{locationOverUnder}</div>
        <div className={parlayText}>{locationParlay}</div>
      </div>
      <div className='row bg-black py-1 border-bottom border-dark'>
        <div className={headingText}>{weekDay}</div>
        <div className={spreadText}>{daySpread}</div>
        <div className={overUnderText}>{dayOverUnder}</div>
        <div className={parlayText}>{dayParlay}</div>
      </div>
      <div className='row bg-black py-1 rounded-bottom'>
        <div className={headingText}>{`${hours} ${ampm}`}</div>
        <div className={spreadText}>{timeSpread}</div>
        <div className={overUnderText}>{timeOverUnder}</div>
        <div className={parlayText}>{timeParlay}</div>
      </div>
      <div className='row'>
        <div className='col-12 p-3'></div>
      </div>
    </div>
  );
};

export default PercentTeamDataTable;

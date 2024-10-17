import '../Fonts.css';
import percentages from './percentages.json';

const PercentOverallDataTable = (props) => {
  const checksAndXs = props?.checksAndXs;

  const addPercentText = (text) => (text !== 'NA' ? `${text}%` : 'N/A');

  const checkNA = (value) => {
    return value === -1 ? 'NA' : value.toFixed(2);
  };

  const showData = (spread, overUnder, parlay) => {
    if (spread === 'N/A' && overUnder === 'N/A' && parlay === 'N/A') {
      return false;
    } else {
      return true;
    }
  };

  const spread = addPercentText(checkNA(percentages['overall_spread']));
  const overUnder = addPercentText(checkNA(percentages['overall_total']));
  const parlay = addPercentText(checkNA(percentages['overall_parlay']));

  const homeSpread = addPercentText(checkNA(percentages['home_spread']));
  const homeOverUnder = addPercentText(checkNA(percentages['home_total']));
  const homeParlay = addPercentText(checkNA(percentages['home_parlay']));

  const awaySpread = addPercentText(checkNA(percentages['away_spread']));
  const awayOverUnder = addPercentText(checkNA(percentages['away_total']));
  const awayParlay = addPercentText(checkNA(percentages['away_parlay']));

  const mondaySpread = addPercentText(
    checkNA(percentages['overall_Mon_spread'])
  );
  const mondayOverUnder = addPercentText(
    checkNA(percentages['overall_Mon_total'])
  );
  const mondayParlay = addPercentText(
    checkNA(percentages['overall_Mon_parlay'])
  );
  const tuesdaySpread = addPercentText(
    checkNA(percentages['overall_Tue_spread'])
  );
  const tuesdayOverUnder = addPercentText(
    checkNA(percentages['overall_Tue_total'])
  );
  const tuesdayParlay = addPercentText(
    checkNA(percentages['overall_Tue_parlay'])
  );
  const wednesdaySpread = addPercentText(
    checkNA(percentages['overall_Wed_spread'])
  );
  const wednesdayOverUnder = addPercentText(
    checkNA(percentages['overall_Wed_total'])
  );
  const wednesdayParlay = addPercentText(
    checkNA(percentages['overall_Wed_parlay'])
  );
  const thursdaySpread = addPercentText(
    checkNA(percentages['overall_Thu_spread'])
  );
  const thursdayOverUnder = addPercentText(
    checkNA(percentages['overall_Thu_total'])
  );
  const thursdayParlay = addPercentText(
    checkNA(percentages['overall_Thu_parlay'])
  );
  const fridaySpread = addPercentText(
    checkNA(percentages['overall_Fri_spread'])
  );
  const fridayOverUnder = addPercentText(
    checkNA(percentages['overall_Fri_total'])
  );
  const fridayParlay = addPercentText(
    checkNA(percentages['overall_Fri_parlay'])
  );
  const saturdaySpread = addPercentText(
    checkNA(percentages['overall_Sat_spread'])
  );
  const saturdayOverUnder = addPercentText(
    checkNA(percentages['overall_Sat_total'])
  );
  const saturdayParlay = addPercentText(
    checkNA(percentages['overall_Sat_parlay'])
  );
  const sundaySpread = addPercentText(
    checkNA(percentages['overall_Sun_spread'])
  );
  const sundayOverUnder = addPercentText(
    checkNA(percentages['overall_Sun_total'])
  );
  const sundayParlay = addPercentText(
    checkNA(percentages['overall_Sun_parlay'])
  );

  const time8Spread = addPercentText(checkNA(percentages['overall_8_spread']));
  const time8OverUnder = addPercentText(
    checkNA(percentages['overall_8_total'])
  );
  const time8Parlay = addPercentText(checkNA(percentages['overall_8_parlay']));
  const time9Spread = addPercentText(checkNA(percentages['overall_9_spread']));
  const time9OverUnder = addPercentText(
    checkNA(percentages['overall_9_total'])
  );
  const time9Parlay = addPercentText(checkNA(percentages['overall_9_parlay']));
  const time10Spread = addPercentText(
    checkNA(percentages['overall_10_spread'])
  );
  const time10OverUnder = addPercentText(
    checkNA(percentages['overall_10_total'])
  );
  const time10Parlay = addPercentText(
    checkNA(percentages['overall_10_parlay'])
  );
  const time11Spread = addPercentText(
    checkNA(percentages['overall_11_spread'])
  );
  const time11OverUnder = addPercentText(
    checkNA(percentages['overall_11_total'])
  );
  const time11Parlay = addPercentText(
    checkNA(percentages['overall_11_parlay'])
  );
  const time12Spread = addPercentText(
    checkNA(percentages['overall_12_spread'])
  );
  const time12OverUnder = addPercentText(
    checkNA(percentages['overall_12_total'])
  );
  const time12Parlay = addPercentText(
    checkNA(percentages['overall_12_parlay'])
  );
  const time13Spread = addPercentText(
    checkNA(percentages['overall_13_spread'])
  );
  const time13OverUnder = addPercentText(
    checkNA(percentages['overall_13_total'])
  );
  const time13Parlay = addPercentText(
    checkNA(percentages['overall_13_parlay'])
  );
  const time14Spread = addPercentText(
    checkNA(percentages['overall_14_spread'])
  );
  const time14OverUnder = addPercentText(
    checkNA(percentages['overall_14_total'])
  );
  const time14Parlay = addPercentText(
    checkNA(percentages['overall_14_parlay'])
  );
  const time15Spread = addPercentText(
    checkNA(percentages['overall_15_spread'])
  );
  const time15OverUnder = addPercentText(
    checkNA(percentages['overall_15_total'])
  );
  const time15Parlay = addPercentText(
    checkNA(percentages['overall_15_parlay'])
  );
  const time16Spread = addPercentText(
    checkNA(percentages['overall_16_spread'])
  );
  const time16OverUnder = addPercentText(
    checkNA(percentages['overall_16_total'])
  );
  const time16Parlay = addPercentText(
    checkNA(percentages['overall_16_parlay'])
  );
  const time17Spread = addPercentText(
    checkNA(percentages['overall_17_spread'])
  );
  const time17OverUnder = addPercentText(
    checkNA(percentages['overall_17_total'])
  );
  const time17Parlay = addPercentText(
    checkNA(percentages['overall_17_parlay'])
  );
  const time18Spread = addPercentText(
    checkNA(percentages['overall_18_spread'])
  );
  const time18OverUnder = addPercentText(
    checkNA(percentages['overall_18_total'])
  );
  const time18Parlay = addPercentText(
    checkNA(percentages['overall_18_parlay'])
  );
  const time19Spread = addPercentText(
    checkNA(percentages['overall_19_spread'])
  );
  const time19OverUnder = addPercentText(
    checkNA(percentages['overall_19_total'])
  );
  const time19Parlay = addPercentText(
    checkNA(percentages['overall_19_parlay'])
  );
  const time20Spread = addPercentText(
    checkNA(percentages['overall_20_spread'])
  );
  const time20OverUnder = addPercentText(
    checkNA(percentages['overall_20_total'])
  );
  const time20Parlay = addPercentText(
    checkNA(percentages['overall_20_parlay'])
  );
  const time21Spread = addPercentText(
    checkNA(percentages['overall_21_spread'])
  );
  const time21OverUnder = addPercentText(
    checkNA(percentages['overall_21_total'])
  );
  const time21Parlay = addPercentText(
    checkNA(percentages['overall_21_parlay'])
  );
  const time22Spread = addPercentText(
    checkNA(percentages['overall_22_spread'])
  );
  const time22OverUnder = addPercentText(
    checkNA(percentages['overall_22_total'])
  );
  const time22Parlay = addPercentText(
    checkNA(percentages['overall_22_parlay'])
  );
  const time23Spread = addPercentText(
    checkNA(percentages['overall_23_spread'])
  );
  const time23OverUnder = addPercentText(
    checkNA(percentages['overall_23_total'])
  );
  const time23Parlay = addPercentText(
    checkNA(percentages['overall_23_parlay'])
  );
  const time24Spread = addPercentText(
    checkNA(percentages['overall_24_spread'])
  );
  const time24OverUnder = addPercentText(
    checkNA(percentages['overall_24_total'])
  );
  const time24Parlay = addPercentText(
    checkNA(percentages['overall_24_parlay'])
  );

  const week1Spread = addPercentText(checkNA(percentages['Week_1_spread']));
  const week1Total = addPercentText(checkNA(percentages['Week_1_total']));
  const week1Parlay = addPercentText(checkNA(percentages['Week_1_parlay']));

  const week2Spread = addPercentText(checkNA(percentages['Week_2_spread']));
  const week2Total = addPercentText(checkNA(percentages['Week_2_total']));
  const week2Parlay = addPercentText(checkNA(percentages['Week_2_parlay']));

  const week3Spread = addPercentText(checkNA(percentages['Week_3_spread']));
  const week3Total = addPercentText(checkNA(percentages['Week_3_total']));
  const week3Parlay = addPercentText(checkNA(percentages['Week_3_parlay']));

  const week4Spread = addPercentText(checkNA(percentages['Week_4_spread']));
  const week4Total = addPercentText(checkNA(percentages['Week_4_total']));
  const week4Parlay = addPercentText(checkNA(percentages['Week_4_parlay']));

  const week5Spread = addPercentText(checkNA(percentages['Week_5_spread']));
  const week5Total = addPercentText(checkNA(percentages['Week_5_total']));
  const week5Parlay = addPercentText(checkNA(percentages['Week_5_parlay']));

  const week6Spread = addPercentText(checkNA(percentages['Week_6_spread']));
  const week6Total = addPercentText(checkNA(percentages['Week_6_total']));
  const week6Parlay = addPercentText(checkNA(percentages['Week_6_parlay']));

  const week7Spread = addPercentText(checkNA(percentages['Week_7_spread']));
  const week7Total = addPercentText(checkNA(percentages['Week_7_total']));
  const week7Parlay = addPercentText(checkNA(percentages['Week_7_parlay']));

  const week8Spread = addPercentText(checkNA(percentages['Week_8_spread']));
  const week8Total = addPercentText(checkNA(percentages['Week_8_total']));
  const week8Parlay = addPercentText(checkNA(percentages['Week_8_parlay']));

  const week9Spread = addPercentText(checkNA(percentages['Week_9_spread']));
  const week9Total = addPercentText(checkNA(percentages['Week_9_total']));
  const week9Parlay = addPercentText(checkNA(percentages['Week_9_parlay']));

  const week10Spread = addPercentText(checkNA(percentages['Week_10_spread']));
  const week10Total = addPercentText(checkNA(percentages['Week_10_total']));
  const week10Parlay = addPercentText(checkNA(percentages['Week_10_parlay']));

  const week11Spread = addPercentText(checkNA(percentages['Week_11_spread']));
  const week11Total = addPercentText(checkNA(percentages['Week_11_total']));
  const week11Parlay = addPercentText(checkNA(percentages['Week_11_parlay']));

  const week12Spread = addPercentText(checkNA(percentages['Week_12_spread']));
  const week12Total = addPercentText(checkNA(percentages['Week_12_total']));
  const week12Parlay = addPercentText(checkNA(percentages['Week_12_parlay']));

  const week13Spread = addPercentText(checkNA(percentages['Week_13_spread']));
  const week13Total = addPercentText(checkNA(percentages['Week_13_total']));
  const week13Parlay = addPercentText(checkNA(percentages['Week_13_parlay']));

  const week14Spread = addPercentText(checkNA(percentages['Week_14_spread']));
  const week14Total = addPercentText(checkNA(percentages['Week_14_total']));
  const week14Parlay = addPercentText(checkNA(percentages['Week_14_parlay']));

  const week15Spread = addPercentText(checkNA(percentages['Week_15_spread']));
  const week15Total = addPercentText(checkNA(percentages['Week_15_total']));
  const week15Parlay = addPercentText(checkNA(percentages['Week_15_parlay']));

  const week16Spread = addPercentText(checkNA(percentages['Week_16_spread']));
  const week16Total = addPercentText(checkNA(percentages['Week_16_total']));
  const week16Parlay = addPercentText(checkNA(percentages['Week_16_parlay']));

  const week17Spread = addPercentText(checkNA(percentages['Week_17_spread']));
  const week17Total = addPercentText(checkNA(percentages['Week_17_total']));
  const week17Parlay = addPercentText(checkNA(percentages['Week_17_parlay']));

  const week18Spread = addPercentText(checkNA(percentages['Week_18_spread']));
  const week18Total = addPercentText(checkNA(percentages['Week_18_total']));
  const week18Parlay = addPercentText(checkNA(percentages['Week_18_parlay']));

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
        <div className='col-12 p-3'></div>
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
      {showData(spread, overUnder, parlay) && (
        <div className='row bg-black py-1 rounded-top border-bottom border-dark'>
          <div className={headingText}>{'Overall'}</div>
          <div className={spreadText}>{spread}</div>
          <div className={overUnderText}>{overUnder}</div>
          <div className={parlayText}>{parlay}</div>
        </div>
      )}
      <div className='row'>
        <div className='col-12 p-3'></div>
      </div>
      {showData(homeSpread, homeOverUnder, homeParlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Home'}</div>
          <div className={spreadText}>{homeSpread}</div>
          <div className={overUnderText}>{homeOverUnder}</div>
          <div className={parlayText}>{homeParlay}</div>
        </div>
      )}
      {showData(awaySpread, awayOverUnder, awayParlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Away'}</div>
          <div className={spreadText}>{awaySpread}</div>
          <div className={overUnderText}>{awayOverUnder}</div>
          <div className={parlayText}>{awayParlay}</div>
        </div>
      )}
      <div className='row'>
        <div className='col-12 p-3'></div>
      </div>
      {showData(mondaySpread, mondayOverUnder, mondayParlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Monday'}</div>
          <div className={spreadText}>{mondaySpread}</div>
          <div className={overUnderText}>{mondayOverUnder}</div>
          <div className={parlayText}>{mondayParlay}</div>
        </div>
      )}
      {showData(tuesdaySpread, tuesdayOverUnder, tuesdayParlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Tuesday'}</div>
          <div className={spreadText}>{tuesdaySpread}</div>
          <div className={overUnderText}>{tuesdayOverUnder}</div>
          <div className={parlayText}>{tuesdayParlay}</div>
        </div>
      )}
      {showData(wednesdaySpread, wednesdayOverUnder, wednesdayParlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Wednesday'}</div>
          <div className={spreadText}>{wednesdaySpread}</div>
          <div className={overUnderText}>{wednesdayOverUnder}</div>
          <div className={parlayText}>{wednesdayParlay}</div>
        </div>
      )}
      {showData(thursdaySpread, thursdayOverUnder, thursdayParlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Thursday'}</div>
          <div className={spreadText}>{thursdaySpread}</div>
          <div className={overUnderText}>{thursdayOverUnder}</div>
          <div className={parlayText}>{thursdayParlay}</div>
        </div>
      )}
      {showData(fridaySpread, fridayOverUnder, fridayParlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Friday'}</div>
          <div className={spreadText}>{fridaySpread}</div>
          <div className={overUnderText}>{fridayOverUnder}</div>
          <div className={parlayText}>{fridayParlay}</div>
        </div>
      )}
      {showData(saturdaySpread, saturdayOverUnder, saturdayParlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Saturday'}</div>
          <div className={spreadText}>{saturdaySpread}</div>
          <div className={overUnderText}>{saturdayOverUnder}</div>
          <div className={parlayText}>{saturdayParlay}</div>
        </div>
      )}
      {showData(sundaySpread, sundayOverUnder, sundayParlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Sunday'}</div>
          <div className={spreadText}>{sundaySpread}</div>
          <div className={overUnderText}>{sundayOverUnder}</div>
          <div className={parlayText}>{sundayParlay}</div>
        </div>
      )}
      <div className='row'>
        <div className='col-12 p-3'></div>
      </div>
      {showData(time8Spread, time8OverUnder, time8Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'8 AM EDT'}</div>
          <div className={spreadText}>{time8Spread}</div>
          <div className={overUnderText}>{time8OverUnder}</div>
          <div className={parlayText}>{time8Parlay}</div>
        </div>
      )}
      {showData(time9Spread, time9OverUnder, time9Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'9 AM EDT'}</div>
          <div className={spreadText}>{time9Spread}</div>
          <div className={overUnderText}>{time9OverUnder}</div>
          <div className={parlayText}>{time9Parlay}</div>
        </div>
      )}
      {showData(time10Spread, time10OverUnder, time10Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'10 AM EDT'}</div>
          <div className={spreadText}>{time10Spread}</div>
          <div className={overUnderText}>{time10OverUnder}</div>
          <div className={parlayText}>{time10Parlay}</div>
        </div>
      )}
      {showData(time11Spread, time11OverUnder, time11Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'11 AM EDT'}</div>
          <div className={spreadText}>{time11Spread}</div>
          <div className={overUnderText}>{time11OverUnder}</div>
          <div className={parlayText}>{time11Parlay}</div>
        </div>
      )}
      {showData(time12Spread, time12OverUnder, time12Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'12 PM EDT'}</div>
          <div className={spreadText}>{time12Spread}</div>
          <div className={overUnderText}>{time12OverUnder}</div>
          <div className={parlayText}>{time12Parlay}</div>
        </div>
      )}
      {showData(time13Spread, time13OverUnder, time13Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'1 PM EDT'}</div>
          <div className={spreadText}>{time13Spread}</div>
          <div className={overUnderText}>{time13OverUnder}</div>
          <div className={parlayText}>{time13Parlay}</div>
        </div>
      )}
      {showData(time14Spread, time14OverUnder, time14Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'2 PM EDT'}</div>
          <div className={spreadText}>{time14Spread}</div>
          <div className={overUnderText}>{time14OverUnder}</div>
          <div className={parlayText}>{time14Parlay}</div>
        </div>
      )}
      {showData(time15Spread, time15OverUnder, time15Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'13 PM EDT'}</div>
          <div className={spreadText}>{time15Spread}</div>
          <div className={overUnderText}>{time15OverUnder}</div>
          <div className={parlayText}>{time15Parlay}</div>
        </div>
      )}
      {showData(time16Spread, time16OverUnder, time16Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'4 PM EDT'}</div>
          <div className={spreadText}>{time16Spread}</div>
          <div className={overUnderText}>{time16OverUnder}</div>
          <div className={parlayText}>{time16Parlay}</div>
        </div>
      )}
      {showData(time17Spread, time17OverUnder, time17Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'5 PM EDT'}</div>
          <div className={spreadText}>{time17Spread}</div>
          <div className={overUnderText}>{time17OverUnder}</div>
          <div className={parlayText}>{time17Parlay}</div>
        </div>
      )}
      {showData(time18Spread, time18OverUnder, time18Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'6 PM EDT'}</div>
          <div className={spreadText}>{time18Spread}</div>
          <div className={overUnderText}>{time18OverUnder}</div>
          <div className={parlayText}>{time18Parlay}</div>
        </div>
      )}
      {showData(time19Spread, time19OverUnder, time19Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'7 PM EDT'}</div>
          <div className={spreadText}>{time19Spread}</div>
          <div className={overUnderText}>{time19OverUnder}</div>
          <div className={parlayText}>{time19Parlay}</div>
        </div>
      )}
      {showData(time20Spread, time20OverUnder, time20Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'8 PM EDT'}</div>
          <div className={spreadText}>{time20Spread}</div>
          <div className={overUnderText}>{time20OverUnder}</div>
          <div className={parlayText}>{time20Parlay}</div>
        </div>
      )}
      {showData(time21Spread, time21OverUnder, time21Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'9 PM EDT'}</div>
          <div className={spreadText}>{time21Spread}</div>
          <div className={overUnderText}>{time21OverUnder}</div>
          <div className={parlayText}>{time21Parlay}</div>
        </div>
      )}
      {showData(time22Spread, time22OverUnder, time22Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'10 PM EDT'}</div>
          <div className={spreadText}>{time22Spread}</div>
          <div className={overUnderText}>{time22OverUnder}</div>
          <div className={parlayText}>{time22Parlay}</div>
        </div>
      )}
      {showData(time23Spread, time23OverUnder, time23Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'11 PM EDT'}</div>
          <div className={spreadText}>{time23Spread}</div>
          <div className={overUnderText}>{time23OverUnder}</div>
          <div className={parlayText}>{time23Parlay}</div>
        </div>
      )}
      {showData(time24Spread, time24OverUnder, time24Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'12 AM EDT'}</div>
          <div className={spreadText}>{time24Spread}</div>
          <div className={overUnderText}>{time24OverUnder}</div>
          <div className={parlayText}>{time24Parlay}</div>
        </div>
      )}
      <div className='row'>
        <div className='col-12 p-3'></div>
      </div>
      {showData(week1Spread, week1Total, week1Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 1'}</div>
          <div className={spreadText}>{week1Spread}</div>
          <div className={overUnderText}>{week1Total}</div>
          <div className={parlayText}>{week1Parlay}</div>
        </div>
      )}
      {showData(week2Spread, week2Total, week2Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 2'}</div>
          <div className={spreadText}>{week2Spread}</div>
          <div className={overUnderText}>{week2Total}</div>
          <div className={parlayText}>{week2Parlay}</div>
        </div>
      )}
      {showData(week3Spread, week3Total, week3Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 3'}</div>
          <div className={spreadText}>{week3Spread}</div>
          <div className={overUnderText}>{week3Total}</div>
          <div className={parlayText}>{week3Parlay}</div>
        </div>
      )}
      {showData(week4Spread, week4Total, week4Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 4'}</div>
          <div className={spreadText}>{week4Spread}</div>
          <div className={overUnderText}>{week4Total}</div>
          <div className={parlayText}>{week4Parlay}</div>
        </div>
      )}
      {showData(week5Spread, week5Total, week5Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 5'}</div>
          <div className={spreadText}>{week5Spread}</div>
          <div className={overUnderText}>{week5Total}</div>
          <div className={parlayText}>{week5Parlay}</div>
        </div>
      )}
      {showData(week6Spread, week6Total, week6Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 6'}</div>
          <div className={spreadText}>{week6Spread}</div>
          <div className={overUnderText}>{week6Total}</div>
          <div className={parlayText}>{week6Parlay}</div>
        </div>
      )}
      {showData(week7Spread, week7Total, week7Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 7'}</div>
          <div className={spreadText}>{week7Spread}</div>
          <div className={overUnderText}>{week7Total}</div>
          <div className={parlayText}>{week7Parlay}</div>
        </div>
      )}
      {showData(week8Spread, week8Total, week8Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 8'}</div>
          <div className={spreadText}>{week8Spread}</div>
          <div className={overUnderText}>{week8Total}</div>
          <div className={parlayText}>{week8Parlay}</div>
        </div>
      )}
      {showData(week9Spread, week9Total, week9Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 9'}</div>
          <div className={spreadText}>{week9Spread}</div>
          <div className={overUnderText}>{week9Total}</div>
          <div className={parlayText}>{week9Parlay}</div>
        </div>
      )}
      {showData(week10Spread, week10Total, week10Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 10'}</div>
          <div className={spreadText}>{week10Spread}</div>
          <div className={overUnderText}>{week10Total}</div>
          <div className={parlayText}>{week10Parlay}</div>
        </div>
      )}
      {showData(week11Spread, week11Total, week11Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 11'}</div>
          <div className={spreadText}>{week11Spread}</div>
          <div className={overUnderText}>{week11Total}</div>
          <div className={parlayText}>{week11Parlay}</div>
        </div>
      )}
      {showData(week12Spread, week12Total, week12Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 12'}</div>
          <div className={spreadText}>{week12Spread}</div>
          <div className={overUnderText}>{week12Total}</div>
          <div className={parlayText}>{week12Parlay}</div>
        </div>
      )}
      {showData(week13Spread, week13Total, week13Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 13'}</div>
          <div className={spreadText}>{week13Spread}</div>
          <div className={overUnderText}>{week13Total}</div>
          <div className={parlayText}>{week13Parlay}</div>
        </div>
      )}
      {showData(week14Spread, week14Total, week14Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 14'}</div>
          <div className={spreadText}>{week14Spread}</div>
          <div className={overUnderText}>{week14Total}</div>
          <div className={parlayText}>{week14Parlay}</div>
        </div>
      )}
      {showData(week15Spread, week15Total, week15Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 15'}</div>
          <div className={spreadText}>{week15Spread}</div>
          <div className={overUnderText}>{week15Total}</div>
          <div className={parlayText}>{week15Parlay}</div>
        </div>
      )}
      {showData(week16Spread, week16Total, week16Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 16'}</div>
          <div className={spreadText}>{week16Spread}</div>
          <div className={overUnderText}>{week16Total}</div>
          <div className={parlayText}>{week16Parlay}</div>
        </div>
      )}
      {showData(week17Spread, week17Total, week17Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 17'}</div>
          <div className={spreadText}>{week17Spread}</div>
          <div className={overUnderText}>{week17Total}</div>
          <div className={parlayText}>{week17Parlay}</div>
        </div>
      )}
      {showData(week18Spread, week18Total, week18Parlay) && (
        <div className='row bg-black py-1 border-bottom border-dark'>
          <div className={headingText}>{'Week 18'}</div>
          <div className={spreadText}>{week18Spread}</div>
          <div className={overUnderText}>{week18Total}</div>
          <div className={parlayText}>{week18Parlay}</div>
        </div>
      )}
    </div>
  );
};

export default PercentOverallDataTable;

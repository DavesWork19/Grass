import './HomePage.css';
import '../Fonts.css';
import Matchups from './Matchups';
import {
  footerMessage1,
  footerMessage2,
  secretCode,
  parlaySecretCode,
} from '../constants';
import { upcomingWeekData } from './upcomingWeekData.js';
import GamblingHeader from '../commonComps/GamblingHeader';
import { Link } from 'react-router-dom';
import OverallPercents from './OverallPercentages';

const NFLHomePage = () => {
  const upcomingWeekDataFormatted = upcomingWeekData
    .slice(1)
    .map((data) => data.split('_'));
  const upcomingWeekDays = upcomingWeekDataFormatted.map((data) => data[0]);
  const uniqueWeekDays = [...new Set(upcomingWeekDays)];

  return (
    <main className='container-fluid text bg-black lightText'>
      <GamblingHeader
        title={`Week ${upcomingWeekData[0]}`}
        link={'gamblingHomePage'}
      />

      {uniqueWeekDays.map((day, index) => (
        <div className='row pb-5' key={day}>
          <Matchups day={day} />
        </div>
      ))}

      <div className='row'>
        <div className='col-12'>
          <OverallPercents />
        </div>
      </div>

      <footer className='row'>
        <div className='col-12 lightText'>
          {footerMessage1}
          {footerMessage2}
        </div>
      </footer>
      <div className='text-start'>
        <Link
          to={`/${secretCode}/Football/${parlaySecretCode}`}
          className='text-muted text-decoration-none'
        >
          {'Parlays'}
        </Link>
      </div>
    </main>
  );
};

export default NFLHomePage;

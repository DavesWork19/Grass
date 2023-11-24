import './HomePage.css';
import '../Fonts.css';
import { Link } from 'react-router-dom';
import Matchups from './MatchupsPage';
import WeeklyPercents from './WeeklyPercentages';
import { footerMessage1, footerMessage2 } from '../constants';
import { upcomingWeekData } from './upcomingWeekData.js';

const NewHome = () => {
  return (
    <main className='container-fluid nflSiteText bg-black'>
      <div className='row pt-2 pb-3'>
        <h1 className='col-12 lightText fs-1'>{`Week ${upcomingWeekData[0]}`}</h1>
      </div>

      <div className='row'>
        <Matchups />
      </div>

      <div className='row'>
        <WeeklyPercents />
      </div>

      <footer className='row'>
        <div className='col-12 lightText'>
          {footerMessage1}
          {footerMessage2}
        </div>
        <Link to='/' className='pt-5 text-end'>
          <button className='nflSiteTextRaw btn btn-outline-secondary'>
            {'Digits'}
          </button>
        </Link>
      </footer>
    </main>
  );
};

export default NewHome;

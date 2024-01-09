import './HomePage.css';
import '../Fonts.css';
import Matchups from './MatchupsPage';
import WeeklyPercents from './WeeklyPercentages';
import { footerMessage1, footerMessage2 } from '../constants';
import { upcomingWeekData } from './upcomingWeekData.js';
import NFLHeader from './Header';

const NFLHomePage = () => {
  return (
    <main className='container-fluid nflSiteText bg-black lightText'>
      <NFLHeader week={upcomingWeekData[0]} />

      <div className='row'>
        <Matchups />
      </div>

      <div className='row'>
        <div className='col-12'>
          <WeeklyPercents />
        </div>
      </div>

      <footer className='row'>
        <div className='col-12 lightText'>
          {footerMessage1}
          {footerMessage2}
        </div>
      </footer>
    </main>
  );
};

export default NFLHomePage;

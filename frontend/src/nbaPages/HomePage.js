import '../Fonts.css';
import NBAMatchups from './Matchups';
import { todaysGames } from './todaysGames';
import { footerMessage1, footerMessage2 } from '../constants';
import NBAHeader from './Header';
import OverallPercents from './OverallPercentages';

const NBAHomePage = () => {
  const todaysDayName = todaysGames.slice(0, 1)[0];
  const todaysDate = todaysGames.slice(1, 2)[0].split(',')[0];
  const date = `${todaysDayName} ${todaysDate}`;

  const times = todaysGames.slice(2).map((data) => data.split(',')[0]);
  const hours = times.map((data) => data.split(':')[0]);
  const unqiueHours = new Set(hours);

  return (
    <main className='container-fluid nflSiteText bg-black lightText'>
      <NBAHeader date={date} />

      <div className='row'>
        <NBAMatchups />
      </div>

      <div className='row'>
        <OverallPercents hours={unqiueHours} />
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

export default NBAHomePage;

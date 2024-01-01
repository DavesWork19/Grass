import '../Fonts.css';
import NBAMatchups from './Matchups';
import { todaysGames } from './todaysGames';
import { footerMessage1, footerMessage2 } from '../constants';
import NBAHeader from './Header';

const NBAHomePage = () => {
  const todaysDate = todaysGames.slice(0, 1)[0].split(',')[0];

  return (
    <main className='container-fluid nflSiteText bg-black lightText'>
      <NBAHeader date={todaysDate} />

      <div className='row'>
        <NBAMatchups />
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

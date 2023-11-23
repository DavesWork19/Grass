import './HomePage.css';
import '../Fonts.css';
import { Link } from 'react-router-dom';
import Matchups from './MatchupsPage';
import WeeklyPercents from './WeeklyPercentages';
import { footerMessage1, footerMessage2 } from '../constants';
import {
  TeamsPercents,
  ConferencePercent,
  DivisionPercent,
} from './HomePagePercentages';
import { upcomingWeekData } from './upcomingWeekData.js';

const NewHome = () => {
  return (
    <main className='container-fluid nflSiteText bg-black'>
      <div className='row pt-2 pb-3'>
        <h1 className='col-12 lightText fs-1'>{`Week ${upcomingWeekData[0]}`}</h1>
      </div>

      <div className='row'>
        <div className='col-4 AFCTable'>
          {DivisionPercent('AFC')}

          {ConferencePercent('AFCNorth')}
          {TeamsPercents(['Ravens', 'Bengals', 'Browns', 'Steelers'])}

          {ConferencePercent('AFCSouth')}
          {TeamsPercents(['Titans', 'Colts', 'Jaguars', 'Texans'])}

          {ConferencePercent('AFCEast')}
          {TeamsPercents(['Bills', 'Jets', 'Dolphins', 'Patriots'])}

          {ConferencePercent('AFCWest')}
          {TeamsPercents(['Chiefs', 'Chargers', 'Broncos', 'Raiders'])}
        </div>

        <div className='col-4'>
          <Matchups />
        </div>

        <div className='col-4 NFCTable'>
          {DivisionPercent('NFC')}

          {ConferencePercent('NFCNorth')}
          {TeamsPercents(['Vikings', 'Packers', 'Bears', 'Lions'])}

          {ConferencePercent('NFCSouth')}
          {TeamsPercents(['Buccaneers', 'Falcons', 'Saints', 'Panthers'])}

          {ConferencePercent('NFCEast')}
          {TeamsPercents(['Cowboys', 'Giants', 'Eagles', 'Commanders'])}

          {ConferencePercent('NFCWest')}
          {TeamsPercents(['49ers', 'Rams', 'Seahawks', 'Cardinals'])}
        </div>
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

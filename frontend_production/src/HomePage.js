import './HomePage.css';
import './Fonts.css';
import Matchups from './MatchupsPage';
import { footerMessage1, footerMessage2, weekHeading } from './constants';
import {
  TeamsPercents,
  ConferencePercent,
  DivisionPercent,
  WeeklyPercents,
} from './HomePagePercentages';

const NewHome = () => {
  return (
    <main className='container-fluid regularText'>
      <div className='row pt-2 pb-5'>
        <h1 className='col-12 lightText'>{weekHeading}</h1>
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

      <div className='row'>{WeeklyPercents()}</div>

      <footer className='row'>
        <div className='col-12 lightText'>
          {footerMessage1}
          {footerMessage2}
        </div>
      </footer>
    </main>
  );
};

export default NewHome;

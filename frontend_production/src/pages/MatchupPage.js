import { Link } from 'react-router-dom';
import './MatchupPage.css';
import '../Fonts.css';
import { weeklyResults } from './results.js';
import { backButton } from '../constants';

const MatchupPage = () => {
  const currentURL = window.location.pathname;
  const [awayTeam, homeTeam] = currentURL.slice(1, -1).split('At');

  const results = weeklyResults.find(
    (element) =>
      element.split(',')[0] === awayTeam || element.split(',')[2] === awayTeam
  );
  const [
    finalResultsWinner,
    finalResultsWinnerPoints,
    finalResultsLoser,
    finalResultsLoserPoints,
    finalResultsPercent,
  ] = results.split(',');

  return (
    <div className='regularText'>
      <h1 className='lightText'>
        {awayTeam}
        {' at the '}
        {homeTeam}
      </h1>

      <div className='row lightText'>
        <div className='col-12'>
          {finalResultsPercent}% chance of {finalResultsWinner} winning
        </div>
      </div>
      <div className='row lightText'>
        <div className='col-12'>Loser: {finalResultsLoser}</div>
      </div>
      <Link to='/'>
        <button className='matchupButton regularText'>{backButton}</button>
      </Link>
    </div>
  );
};

export default MatchupPage;

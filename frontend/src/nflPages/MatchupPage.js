import { useNavigate, Link } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import './MatchupPage.css';
import '../Fonts.css';
import { weeklyResults } from './results.js';
import { backButton } from '../constants';

const MatchupPage = () => {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const currentURL = pathname.split('/')[2];
  const [awayTeam, homeTeam] = currentURL.split('At');
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
    <div className='nflSiteText pb-5 bg-black vh-100 container-fluid'>
      <h1 className='lightText pb-5 pt-5'>
        {awayTeam}
        {' at the '}
        {homeTeam}
      </h1>

      <div className='row lightText'>
        <div className='col-12 timeText fs-3'>
          {finalResultsPercent}%{' '}
          <span className='nflSiteTextRaw'>{`chance of ${finalResultsWinner} winning`}</span>
        </div>
      </div>
      <div className='row lightText pb-5 fs-3'>
        <div className='col-12'>and {finalResultsLoser} Losing</div>
      </div>
      <Link
        to={'..'}
        onClick={(e) => {
          e.preventDefault();
          navigate(-1);
        }}
      >
        <button className='matchupButton nflSiteText'>{backButton}</button>
      </Link>
    </div>
  );
};

export default MatchupPage;

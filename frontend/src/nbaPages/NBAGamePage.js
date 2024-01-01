import { useNavigate, Link } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import '../Fonts.css';
import { backButton, matchUpPageText1, matchUpPageText2 } from '../constants';
import { useLayoutEffect } from 'react';
import { todaysGames } from './todaysGames';

const NBAGamePage = () => {
  useLayoutEffect(() => {
    window.scrollTo({
      top: 100,
      left: 100,
      behavior: 'smooth',
    });
  });

  const navigate = useNavigate();
  const { pathname } = useLocation();
  const currentURL = pathname.split('/')[3];
  console.log(currentURL);
  const [awayTeam, homeTeam] = currentURL.split('AT');
  const awayTeamName = awayTeam.split('%20').join(' ');
  const homeTeamName = homeTeam.split('%20').join(' ');
  const results = todaysGames.find(
    (element) =>
      element.split(',')[1] === awayTeamName ||
      element.split(',')[2] === homeTeamName
  );
  const [
    gameTime,
    awayTeamAgain,
    homeTeamAgain,
    homeTeamSpread,
    homeTeamCover,
    overUnder,
    overUnderCover,
  ] = results.split(',');

  const homeCover = +homeTeamCover ? 'cover ' : 'not cover ';
  const overUnderCoverName = +overUnderCover ? 'over' : 'under';

  console.log(results);
  console.log(awayTeamName, homeTeam);

  return (
    <div className='nflSiteText pb-5 bg-black lightText container-fluid vh-100'>
      <h1 className='pt-5'>{awayTeamName}</h1>
      <h1> {' at the '}</h1>
      <h1 className='pb-5'> {homeTeamName}</h1>

      <div className='row lightText'>
        <div className='col-12 timeText fs-3'>
          {`${homeTeamName} predicted to ${homeCover} ${homeTeamSpread}`}
        </div>
        <div className='col-12 timeText fs-3'>
          {`Predicted ${overUnderCoverName} ${overUnder}`}
        </div>
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
      <div className='row pt-5 lightText smallText'>
        <div className='col-12 pt-5'>{matchUpPageText1}</div>
        <div className='col-12'>{matchUpPageText2}</div>
      </div>
    </div>
  );
};

export default NBAGamePage;

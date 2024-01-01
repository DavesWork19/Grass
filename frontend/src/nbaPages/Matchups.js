import { Link } from 'react-router-dom';
import { nbaTeamLogos } from '../constants';
import ATLogo from '../logos/atLogo1.png';
import '../Fonts.css';
import { todaysGames } from './todaysGames';

const NBAMatchups = () => {
  const setTeam = (team) => {
    return (
      <div>
        <img className='teamImgs' src={nbaTeamLogos[team]} alt='logo' />
      </div>
    );
  };
  return todaysGames.slice(1).map((data) => {
    const [gameTime, awayTeam, homeTeam] = data.split(',');
    const link = `${awayTeam}AT${homeTeam}`;

    return (
      <Link to={link} key={link} className='col-12'>
        <button className='btn btn-light mt-1 mb-5 px-5'>
          <div className='timeText timeMobileText border-bottom border-black mb-1'>
            {`${gameTime}m EST`}
          </div>
          <div className='row'>
            <div className='col-4'>{setTeam(awayTeam)}</div>
            <div className='col-4'>
              <img className='atSymbol' src={ATLogo} alt='atLogo' />
            </div>
            <div className='col-4'>{setTeam(homeTeam)}</div>
          </div>
        </button>
      </Link>
    );
  });
};

export default NBAMatchups;

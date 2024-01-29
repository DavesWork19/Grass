import { Link } from 'react-router-dom';
import { legalNbaTeamLogos } from '../constants';
import ATLogo from '../logos/atLogo1.png';
import '../Fonts.css';
import { todaysGames } from './todaysGames';

const NBAMatchups = () => {
  const setTeam = (team, textPos) => {
    return (
      <div className={`legalTeamNames text-${textPos}`}>
        {/* <img className='teamImgs' src={nbaTeamLogos[team]} alt='logo' /> */}
        {legalNbaTeamLogos[team]}
      </div>
    );
  };
  return todaysGames.slice(2).map((data) => {
    const [gameTime, awayTeam, homeTeam] = data.split(',');
    const link = `${awayTeam}AT${homeTeam}`;

    return (
      <Link to={link} key={link} className='col-12'>
        <button className='btn btn-light mt-1 mb-5 px-sm-5'>
          <div className='timeText timeMobileText border-bottom border-black mb-3'>
            {`${gameTime}m EST`}
          </div>
          <div className='row'>
            <div className='col-5 col-sm-4'>{setTeam(awayTeam, 'start')}</div>
            <div className='col-2 col-sm-4 px-0'>
              <img className='atSymbol' src={ATLogo} alt='atLogo' />
            </div>
            <div className='col-5 col-sm-4'>{setTeam(homeTeam, 'end')}</div>
          </div>
        </button>
      </Link>
    );
  });
};

export default NBAMatchups;

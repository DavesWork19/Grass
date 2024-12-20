import { Link } from 'react-router-dom';
import ATLogo from '../logos/atLogo1.png';
import '../Fonts.css';
import { todaysGames } from './todaysGames';

const NBAMatchups = () => {
  const setTeam = (team, textPos) => {
    return (
      <div className={`legalTeamNames boldText text-${textPos}`}>
        {/* <img className='teamImgs' src={nbaTeamLogos[team]} alt='logo' /> */}
        {team}
      </div>
    );
  };
  return todaysGames.slice(2).map((data) => {
    const [gameTime, awayTeamILL, homeTeamILL] = data.split(',');
    // const awayTeam = legalNbaTeamLogos[awayTeamILL];
    // const homeTeam = legalNbaTeamLogos[homeTeamILL];
    const secondLastElement = gameTime.length - 1;
    const lastAwayElement = awayTeamILL.split(' ').length - 1;
    const lastHomeElement = homeTeamILL.split(' ').length - 1;
    const updatedGameTime = gameTime.slice(0, secondLastElement);
    const ampm = gameTime[secondLastElement].toUpperCase();
    const awayTeam = awayTeamILL.split(' ')[lastAwayElement];
    const homeTeam = homeTeamILL.split(' ')[lastHomeElement];
    const link = `${awayTeam}AT${homeTeam}`;

    return (
      <Link to={link} key={link} className='col-12'>
        <button className='btn btn-light mt-1 mb-5 px-sm-5 boldText border-dark slateGrayBackground'>
          <div className='border-bottom border-black mb-3'>
            {`${updatedGameTime} ${ampm}M EDT`}
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

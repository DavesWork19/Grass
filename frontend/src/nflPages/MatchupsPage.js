import { Link } from 'react-router-dom';
import { upcomingWeekData } from './upcomingWeekData.js';
import percentages from './percentages.json';
import { legalNFLTeams } from '../constants';
import ATLogo from '../logos/atLogo1.png';
import '../Fonts.css';

const Matchups = () => {
  const setTeam = (team, textPos) => {
    return (
      <div className={`legalNFLTeamNames text-${textPos}`}>
        {/* <img className='teamImgs' src={teamLogos[team]} alt='logo' /> */}
        <div>{legalNFLTeams[team]}</div>
        <div>{percentages[team].toFixed(2)}</div>
      </div>
    );
  };

  return upcomingWeekData.slice(1).map((data) => {
    const [
      date,
      time,
      am_pm,
      timeZone,
      awayTeam,
      homeTeam,
      temp,
      weather,
      wind,
    ] = data.split('_');
    const link = `${awayTeam}At${homeTeam}`;
    const [hour, minute] = time.split(':');
    const timeLabel = `${parseInt(hour)}:${minute} ${am_pm} ${timeZone}`;

    return (
      <Link to={link} key={link} className='col-12'>
        <button className='btn btn-light mt-1 mb-5 px-sm-5'>
          <div className='timeText timeMobileText'>{date}</div>
          <div className='timeText timeMobileText border-bottom border-black mb-1'>
            {timeLabel}
          </div>
          <div className='row'>
            <div className='col-5 col-sm-4 px-0'>
              {setTeam(awayTeam, 'start')}
            </div>
            <div className='col-2 col-sm-4 px-0'>
              <img className='atSymbol w-50' src={ATLogo} alt='atLogo' />
            </div>
            <div className='col-5 col-sm-4 px-0'>
              {setTeam(homeTeam, 'end')}
            </div>
          </div>
        </button>
      </Link>
    );
  });
};

export default Matchups;

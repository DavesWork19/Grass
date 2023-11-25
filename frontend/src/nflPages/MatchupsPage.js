import { Link } from 'react-router-dom';
import './MatchupsPage.css';
import { upcomingWeekData } from './upcomingWeekData.js';
import percentages from './percentages.json';
import { teamLogos } from '../constants';
import ATLogo from '../logos/atLogo1.png';
import '../Fonts.css';

const Matchups = () => {
  const setTeam = (team) => {
    return (
      <div>
        <img className='teamImgs' src={teamLogos[team]} alt='logo' />
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
        <button className='btn btn-light mt-1 mb-5 px-5'>
          <div className='timeText timeMobileText'>{date}</div>
          <div className='timeText timeMobileText border-bottom border-black mb-1'>
            {timeLabel}
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

export default Matchups;

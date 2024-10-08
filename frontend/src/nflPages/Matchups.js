import { Link } from 'react-router-dom';
import { upcomingWeekData } from './upcomingWeekData.js';
import { legalNFLTeams } from '../constants';
import ATLogo from '../logos/atLogo1.png';
import '../Fonts.css';

const Matchups = (props) => {
  const givenDay = props.day;

  const times = upcomingWeekData.slice(1).map((data) => {
    const splitData = data.split('_');
    if (givenDay === splitData[0]) return splitData[1];
    return -1;
  });
  const timeSet = [...new Set(times)];
  const uniqueWeekTimes = timeSet.filter((time) => time !== -1);

  console.log(uniqueWeekTimes);

  const setTeam = (team, textPos) => {
    return (
      <div className={`boldText text-${textPos}`}>
        {/* <img className='teamImgs' src={teamLogos[team]} alt='logo' /> */}
        <div>{legalNFLTeams[team]}</div>
      </div>
    );
  };

  return (
    <div className='border rounded'>
      <div className='text-center fs-2 pb-5'>{givenDay}</div>

      {upcomingWeekData.slice(1).map((data) => {
        const [
          weekDay,
          time,
          awayTeam,
          homeTeam,
          selectedTeam,
          selectedSpread,
          selectedSpreadCall,
          selectedTotal,
          selectedTotalCall,
        ] = data.split('_');
        const link = `${awayTeam}At${homeTeam}`;
        const day = weekDay.split(' - ')[0];
        const updatedTime = time[0] === '0' ? time.slice(1) : time;

        if (day !== givenDay) {
          return null;
        }

        return (
          <div key={link} className='row'>
            <Link
              to={link}
              state={{
                weekDay,
                updatedTime,
                awayTeam,
                homeTeam,
                selectedTeam,
                selectedSpread,
                selectedSpreadCall,
                selectedTotal,
                selectedTotalCall,
              }}
              className='col-12'
            >
              <button className='btn btn-light mt-1 mb-5 px-sm-5 boldText border-dark slateGrayBackground col-12 col-sm-8'>
                <div className='border-bottom border-black mb-1'>
                  {updatedTime}
                </div>
                <div className='row'>
                  <div className='col-5 col-sm-4'>
                    {setTeam(awayTeam, 'start')}
                  </div>
                  <div className='col-2 col-sm-4 px-0'>
                    <img className='atSymbol' src={ATLogo} alt='atLogo' />
                  </div>
                  <div className='col-5 col-sm-4'>
                    {setTeam(homeTeam, 'end')}
                  </div>
                </div>
              </button>
            </Link>
          </div>
        );
      })}
    </div>
  );
};

export default Matchups;

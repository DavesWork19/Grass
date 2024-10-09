import { Link } from 'react-router-dom';
import { upcomingWeekData } from './upcomingWeekData.js';
import ATLogo from '../logos/atLogo1.png';
import '../Fonts.css';

const Matchups = (props) => {
  const givenDay = props.day;

  const setTeam = (team, textPos) => {
    return (
      <div className={`boldText text-${textPos}`}>
        {/* <img className='teamImgs' src={teamLogos[team]} alt='logo' /> */}
        <div>{team}</div>
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
        const day = weekDay.split(' - ')[0];

        if (day !== givenDay) {
          return null;
        }
        const link = `${awayTeam}At${homeTeam}`;
        const updatedTime = time[0] === '0' ? time.slice(1) : time;
        const homeCover = +selectedSpreadCall ? true : false;
        const homeSpreadCall = homeCover ? 'Cover' : null;
        const awaySpreadCall = homeCover ? null : 'Cover';
        const overUnderCoverName = +selectedTotalCall ? 'Over' : 'Under';

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
                <div className='row border-bottom border-black mx-2 mx-sm-0 pb-1'>
                  <div className='col-12'>{updatedTime}</div>
                </div>
                <div className='row py-1'>
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
                <div className='row border-top border-black mx-2 mx-sm-0 py-1'>
                  <div className='col-4'>
                    {awaySpreadCall ?? `${overUnderCoverName} ${selectedTotal}`}
                  </div>
                  <div className='col-4'>{selectedSpread}</div>
                  <div className='col-4'>
                    {homeSpreadCall ?? `${overUnderCoverName} ${selectedTotal}`}
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

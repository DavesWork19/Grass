import { useLocation } from 'react-router-dom';
import './MatchupPage.css';
import '../Fonts.css';
import { matchUpPageText1, matchUpPageText2 } from '../constants';
import { useLayoutEffect } from 'react';
import GamblingHeader from '../commonComps/GamblingHeader';
import PercentTeamDataTable from './PercentTeamDataTable';

const MatchupPage = (props) => {
  useLayoutEffect(() => {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth',
    });
  });

  const { state } = useLocation();

  const {
    weekDay,
    updatedTime,
    awayTeam,
    homeTeam,
    selectedTeam,
    selectedSpread,
    selectedSpreadCall,
    selectedTotal,
    selectedTotalCall,
  } = state;

  const homeCover = +selectedSpreadCall ? 'cover ' : 'not cover ';
  const overUnderCoverName = +selectedTotalCall ? 'over' : 'under';

  return (
    <div className='text lightText pb-5 bg-black container-fluid'>
      <GamblingHeader title={weekDay} subTitle={updatedTime} link={'back'} />

      <div className='fs-1'>{`${awayTeam} at ${homeTeam}`}</div>

      <div className='row mt-5'>
        <div className='col-12  fs-3'>
          {`${selectedTeam} predicted to ${homeCover} ${selectedSpread}`}
        </div>
        <div className='col-12  fs-3'>
          {`Predicted ${overUnderCoverName} ${selectedTotal}`}
        </div>
      </div>

      <div className='row pt-5 mt-5 pb-3'>
        <div className='col-md-6'>
          <PercentTeamDataTable
            team={awayTeam}
            homeTeam={false}
            weekDay={weekDay}
            time={updatedTime}
          />
        </div>
        <div className='col-md-6 mt-sm-0 mt-5'>
          <PercentTeamDataTable
            team={homeTeam}
            homeTeam={true}
            weekDay={weekDay}
            time={updatedTime}
          />
        </div>
      </div>

      <div className='row pt-5 smallText'>
        <div className='col-12 pt-5'>{matchUpPageText1}</div>
        <div className='col-12'>{matchUpPageText2}</div>
      </div>
    </div>
  );
};

export default MatchupPage;

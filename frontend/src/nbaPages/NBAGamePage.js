import { useLocation } from 'react-router-dom';
import '../Fonts.css';
import {
  matchUpPageText1,
  matchUpPageText2,
  nbaTeamShortNames,
} from '../constants';
import { useLayoutEffect } from 'react';
import { todaysGames } from './todaysGames';
import GamblingHeader from '../commonComps/GamblingHeader';
import PercentDataTable from '../commonComps/PercentDataTable';

const NBAGamePage = () => {
  useLayoutEffect(() => {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth',
    });
  });

  const { pathname } = useLocation();
  const currentURL = pathname.split('/')[3];
  const [awayTeam, homeTeam] = currentURL.split('AT');
  const results = todaysGames.find(
    (element) =>
      element.split(',')[1]?.includes(awayTeam) ||
      element.split(',')[2]?.includes(homeTeam)
  );

  const [homeTeamSpread, homeTeamCover, overUnder, overUnderCover] = results
    .split(',')
    .slice(3);
  const [gameTime] = results.split(',')[0];
  const hour = gameTime.split(':')[0];

  const homeCover = +homeTeamCover ? 'cover ' : 'not cover ';
  const overUnderCoverName = +overUnderCover ? 'over' : 'under';

  return (
    <div className='text lightText pb-5 bg-black  container-fluid'>
      <GamblingHeader title={`${awayTeam} at ${homeTeam}`} link={'back'} />

      <div className='row mt-5'>
        <div className='col-12  fs-3'>
          {`${homeTeam} predicted to ${homeCover} ${homeTeamSpread}`}
        </div>
        <div className='col-12  fs-3'>
          {`Predicted ${overUnderCoverName} ${overUnder}`}
        </div>
      </div>

      <div className='row pt-5 mt-5 pb-3'>
        <div className='col-md-6'>
          <PercentDataTable
            title={awayTeam}
            percentagesName={nbaTeamShortNames[awayTeam]}
            hours={new Set([hour])}
            checksAndXs={true}
          />
        </div>
        <div className='col-md-6 mt-sm-0 mt-5'>
          <PercentDataTable
            title={homeTeam}
            percentagesName={nbaTeamShortNames[homeTeam]}
            hours={new Set([hour])}
            checksAndXs={true}
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

export default NBAGamePage;

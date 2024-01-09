import { useNavigate, Link } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import '../Fonts.css';
import {
  backButton,
  teamStatsText,
  matchUpPageText1,
  matchUpPageText2,
  nbaTeamShortNames,
} from '../constants';
import { useLayoutEffect } from 'react';
import { todaysGames } from './todaysGames';
import { percentages } from './percentages';
import TeamInfo from '../nflPages/TeamInfo';

const NBAGamePage = () => {
  useLayoutEffect(() => {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth',
    });
  });

  const navigate = useNavigate();
  const { pathname } = useLocation();
  const currentURL = pathname.split('/')[3];
  const [awayTeam, homeTeam] = currentURL.split('AT');
  const awayTeamName = awayTeam.split('%20').join(' ');
  const homeTeamName = homeTeam.split('%20').join(' ');
  const results = todaysGames.find(
    (element) =>
      element.split(',')[1] === awayTeamName ||
      element.split(',')[2] === homeTeamName
  );
  const todaysDayName = todaysGames.slice(0, 1)[0];
  const [
    gameTime,
    awayTeamAgain,
    homeTeamAgain,
    homeTeamSpread,
    homeTeamCover,
    overUnder,
    overUnderCover,
  ] = results.split(',');
  const hour = gameTime.split(':')[0];

  const homeCover = +homeTeamCover ? 'cover ' : 'not cover ';
  const overUnderCoverName = +overUnderCover ? 'over' : 'under';

  //Away Percentages
  const awayTeamSpreadPercent =
    percentages[`${nbaTeamShortNames[awayTeamName]}_spread`];
  const awayTeamOverUnderPercent =
    percentages[`${nbaTeamShortNames[awayTeamName]}_overUnder`];
  const awayTeamParlayPercent =
    percentages[`${nbaTeamShortNames[awayTeamName]}_parlay`];
  const awayTeamTimeSpreadPercent =
    percentages[
      `${nbaTeamShortNames[awayTeamName]}_Time_${hour}_${hour}59_spread`
    ];
  const awayTeamTimeOverUnderPercent =
    percentages[
      `${nbaTeamShortNames[awayTeamName]}_Time_${hour}_${hour}59_overUnder`
    ];
  const awayTeamTimeParlayPercent =
    percentages[
      `${nbaTeamShortNames[awayTeamName]}_Time_${hour}_${hour}59_parlay`
    ];
  const awayTeamDaySpreadPercent =
    percentages[`${nbaTeamShortNames[awayTeamName]}_${todaysDayName}_spread`];
  const awayTeamDayOverUnderPercent =
    percentages[
      `${nbaTeamShortNames[awayTeamName]}_${todaysDayName}_overUnder`
    ];
  const awayTeamDayParlayPercent =
    percentages[`${nbaTeamShortNames[awayTeamName]}_${todaysDayName}_parlay`];

  //Home Percentages
  const homeTeamSpreadPercent =
    percentages[`${nbaTeamShortNames[homeTeamName]}_spread`];
  const homeTeamOverUnderPercent =
    percentages[`${nbaTeamShortNames[homeTeamName]}_overUnder`];
  const homeTeamParlayPercent =
    percentages[`${nbaTeamShortNames[homeTeamName]}_parlay`];
  const homeTeamTimeSpreadPercent =
    percentages[
      `${nbaTeamShortNames[homeTeamName]}_Time_${hour}_${hour}59_spread`
    ];
  const homeTeamTimeOverUnderPercent =
    percentages[
      `${nbaTeamShortNames[homeTeamName]}_Time_${hour}_${hour}59_overUnder`
    ];
  const homeTeamTimeParlayPercent =
    percentages[
      `${nbaTeamShortNames[homeTeamName]}_Time_${hour}_${hour}59_parlay`
    ];
  const homeTeamDaySpreadPercent =
    percentages[`${nbaTeamShortNames[homeTeamName]}_${todaysDayName}_spread`];
  const homeTeamDayOverUnderPercent =
    percentages[
      `${nbaTeamShortNames[homeTeamName]}_${todaysDayName}_overUnder`
    ];
  const homeTeamDayParlayPercent =
    percentages[`${nbaTeamShortNames[homeTeamName]}_${todaysDayName}_parlay`];

  return (
    <div className='nflSiteText pb-5 bg-black lightText container-fluid'>
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

      <div className='row lightText pt-5 pb-3 border-bottom'>
        <div className='col-12'>{teamStatsText}</div>
      </div>
      <div className='row lightText'>
        <div className='col-6'>
          <div className='pt-3 pb-3'>{awayTeamName}</div>
          <TeamInfo
            info={{ title: 'spread', percent: awayTeamSpreadPercent }}
          />
          <TeamInfo
            info={{
              title: 'over under',
              percent: awayTeamOverUnderPercent,
            }}
          />
          <TeamInfo
            info={{
              title: 'parlay',
              percent: awayTeamParlayPercent,
            }}
          />
          <TeamInfo
            info={{
              title: `spread at ${hour}PM`,
              percent: awayTeamTimeSpreadPercent,
            }}
          />
          <TeamInfo
            info={{
              title: `over under at ${hour}PM`,
              percent: awayTeamTimeOverUnderPercent,
            }}
          />
          <TeamInfo
            info={{
              title: `parlay at ${hour}PM`,
              percent: awayTeamTimeParlayPercent,
            }}
          />
          <TeamInfo
            info={{
              title: `spread when ${todaysDayName}`,
              percent: awayTeamDaySpreadPercent,
            }}
          />
          <TeamInfo
            info={{
              title: `over under when ${todaysDayName}`,
              percent: awayTeamDayOverUnderPercent,
            }}
          />
          <TeamInfo
            info={{
              title: `parlay when ${todaysDayName}`,
              percent: awayTeamDayParlayPercent,
            }}
          />
        </div>
        <div className='col-6 border-start'>
          <div className='pt-3 pb-3'>{homeTeamName}</div>
          <TeamInfo
            info={{ title: 'spread', percent: homeTeamSpreadPercent }}
          />
          <TeamInfo
            info={{
              title: 'over under',
              percent: homeTeamOverUnderPercent,
            }}
          />
          <TeamInfo
            info={{
              title: 'parlay',
              percent: homeTeamParlayPercent,
            }}
          />
          <TeamInfo
            info={{
              title: `spread at ${hour}PM`,
              percent: homeTeamTimeSpreadPercent,
            }}
          />
          <TeamInfo
            info={{
              title: `over under at ${hour}PM`,
              percent: homeTeamTimeOverUnderPercent,
            }}
          />
          <TeamInfo
            info={{
              title: `parlay at ${hour}PM`,
              percent: homeTeamTimeParlayPercent,
            }}
          />
          <TeamInfo
            info={{
              title: `spread when ${todaysDayName}`,
              percent: homeTeamDaySpreadPercent,
            }}
          />
          <TeamInfo
            info={{
              title: `over under when ${todaysDayName}`,
              percent: homeTeamDayOverUnderPercent,
            }}
          />
          <TeamInfo
            info={{
              title: `parlay when ${todaysDayName}`,
              percent: homeTeamDayParlayPercent,
            }}
          />
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

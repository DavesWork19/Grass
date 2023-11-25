import { useNavigate, Link } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import './MatchupPage.css';
import '../Fonts.css';
import { weeklyResults } from './results.js';
import percentages from './percentages.json';
import TeamInfo from './TeamInfo';
import {
  teamInfo,
  backButton,
  teamStatsText,
  matchUpPageText1,
  matchUpPageText2,
  awayTeamAwayPercentText,
  homeTeamHomePercentText,
  winnerPredictedPercentText,
  loserPredictedPercentText,
} from '../constants';

const MatchupPage = () => {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const currentURL = pathname.split('/')[2];
  const [awayTeam, homeTeam] = currentURL.split('At');
  const results = weeklyResults.find(
    (element) =>
      element.split(',')[0] === awayTeam || element.split(',')[0] === homeTeam
  );

  const [predictedWinner, Day, finalResultsPercent] = results.split(',');

  const awayTeamPredictedText =
    predictedWinner === awayTeam
      ? winnerPredictedPercentText
      : loserPredictedPercentText;

  const homeTeamPredictedText =
    predictedWinner === homeTeam
      ? winnerPredictedPercentText
      : loserPredictedPercentText;

  const awayTeamInfo = teamInfo[awayTeam];
  const awayTeamConference = awayTeamInfo.split(' ')[0];
  const awayTeamDivisionPercent = percentages[awayTeamInfo];
  const awayTeamConferencePercent = percentages[awayTeamConference];
  const awayTeamAwayPercent = percentages[`${awayTeam}_away`];
  const awayTeamDayPercent = percentages[`${awayTeam}_day_${Day}`];
  const awayTeamPredictedPercent =
    predictedWinner === awayTeam
      ? percentages[`${awayTeam}_predictedWinner`]
      : percentages[`${awayTeam}_predictedLoser`];

  const homeTeamInfo = teamInfo[homeTeam];
  const homeTeamConference = homeTeamInfo.split(' ')[0];
  const homeTeamDivisionPercent = percentages[homeTeamInfo];
  const homeTeamConferencePercent = percentages[homeTeamConference];
  const homeTeamHomePercent = percentages[`${homeTeam}_home`];
  const homeTeamDayPercent = percentages[`${homeTeam}_day_${Day}`];
  const homeTeamPredictedPercent =
    predictedWinner === homeTeam
      ? percentages[`${homeTeam}_predictedWinner`]
      : percentages[`${homeTeam}_predictedLoser`];

  return (
    <div className='nflSiteText pb-5 bg-black container-fluid'>
      <h1 className='lightText pb-5 pt-5'>
        {awayTeam}
        {' at the '}
        {homeTeam}
      </h1>

      <div className='row lightText'>
        <div className='col-12 timeText fs-3'>
          {finalResultsPercent}%{' '}
          <span className='nflSiteTextRaw'>{`chance of ${predictedWinner} winning`}</span>
        </div>
      </div>
      <div className='row lightText pt-5 pb-3 border-bottom'>
        <div className='col-12'>{teamStatsText}</div>
      </div>
      <div className='row lightText'>
        <div className='col-6'>
          <div className='pt-3 pb-3'>{awayTeam}</div>
          <TeamInfo
            info={{ title: awayTeamInfo, percent: awayTeamDivisionPercent }}
          />
          <TeamInfo
            info={{
              title: awayTeamConference,
              percent: awayTeamConferencePercent,
            }}
          />
          <TeamInfo
            info={{
              title: awayTeamAwayPercentText,
              percent: awayTeamAwayPercent,
            }}
          />
          <TeamInfo
            info={{
              title: `When ${Day}`,
              percent: awayTeamDayPercent,
            }}
          />
          <TeamInfo
            info={{
              title: awayTeamPredictedText,
              percent: awayTeamPredictedPercent,
            }}
          />
        </div>
        <div className='col-6 border-start'>
          <div className='pt-3 pb-3'>{homeTeam}</div>
          <TeamInfo
            info={{
              title: homeTeamInfo,
              percent: homeTeamDivisionPercent,
            }}
          />
          <TeamInfo
            info={{
              title: homeTeamConference,
              percent: homeTeamConferencePercent,
            }}
          />
          <TeamInfo
            info={{
              title: homeTeamHomePercentText,
              percent: homeTeamHomePercent,
            }}
          />
          <TeamInfo
            info={{
              title: `When ${Day}`,
              percent: homeTeamDayPercent,
            }}
          />
          <TeamInfo
            info={{
              title: homeTeamPredictedText,
              percent: homeTeamPredictedPercent,
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

export default MatchupPage;

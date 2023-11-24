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
  matchUpPageText,
} from '../constants';

const MatchupPage = () => {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const currentURL = pathname.split('/')[2];
  const [awayTeam, homeTeam] = currentURL.split('At');
  const results = weeklyResults.find(
    (element) =>
      element.split(',')[0] === awayTeam || element.split(',')[2] === awayTeam
  );
  const [
    finalResultsWinner,
    finalResultsWinnerPoints,
    finalResultsLoser,
    finalResultsLoserPoints,
    finalResultsPercent,
  ] = results.split(',');

  const awayTeamInfo = teamInfo[awayTeam];
  const awayTeamConference = awayTeamInfo.split(' ')[0];
  const awayTeamDivisionPercent = percentages[awayTeamInfo];
  const awayTeamConferencePercent = percentages[awayTeamConference];
  const awayInfo = {
    conference: awayTeamConference,
    division: awayTeamInfo,
    conferencePercent: awayTeamConferencePercent,
    divisionPercent: awayTeamDivisionPercent,
  };

  const homeTeamInfo = teamInfo[homeTeam];
  const homeTeamConference = homeTeamInfo.split(' ')[0];
  const homeTeamDivisionPercent = percentages[homeTeamInfo];
  const homeTeamConferencePercent = percentages[homeTeamConference];
  const homeInfo = {
    conference: homeTeamConference,
    division: homeTeamInfo,
    conferencePercent: homeTeamConferencePercent,
    divisionPercent: homeTeamDivisionPercent,
  };

  return (
    <div className='nflSiteText pb-5 bg-black vh-100 container-fluid'>
      <h1 className='lightText pb-5 pt-5'>
        {awayTeam}
        {' at the '}
        {homeTeam}
      </h1>

      <div className='row lightText'>
        <div className='col-12 timeText fs-3'>
          {finalResultsPercent}%{' '}
          <span className='nflSiteTextRaw'>{`chance of ${finalResultsWinner} winning`}</span>
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
        <div className='col-12 pt-5'>{matchUpPageText}</div>
      </div>
    </div>
  );
};

export default MatchupPage;

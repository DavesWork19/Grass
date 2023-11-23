import percentages from './percentages.json';
import './HomePagePercentages.css';
import '../Fonts.css';

export const TeamsPercents = (teams) => {
  const [team1, team2, team3, team4] = teams;
  const teamsPercentages = [
    { team: team1, percent: percentages[team1].toFixed(2) },
    { team: team2, percent: percentages[team2].toFixed(2) },
    { team: team3, percent: percentages[team3].toFixed(2) },
    { team: team4, percent: percentages[team4].toFixed(2) },
  ];
  teamsPercentages.sort((a, b) => a.percent - b.percent);

  return (
    <div className='pb-sm-5 mb-sm-5'>
      <h4 className='row'>
        <span className='col-12 text-start ps-1 ps-sm-3 ps-lg-5 col-sm-5 nflSiteTeamText'>{`${teamsPercentages[3].team}`}</span>
        <span className='col-12 col-sm-2'>{''}</span>
        <span className='col-12 text-start px-1 ps-sm-4 col-sm-5 nflSiteTeamText'>{`${teamsPercentages[3].percent}%`}</span>
      </h4>
      <h4 className='row'>
        <span className='col-12 text-start ps-1 ps-sm-3 ps-lg-5 col-sm-5 nflSiteTeamText'>{`${teamsPercentages[2].team}`}</span>
        <span className='col-12 col-sm-2'>{''}</span>
        <span className='col-12 text-start px-1 ps-sm-4 col-sm-5 nflSiteTeamText'>{`${teamsPercentages[2].percent}%`}</span>
      </h4>
      <h4 className='row'>
        <span className='col-12 text-start ps-1 ps-sm-3 ps-lg-5 col-sm-5 nflSiteTeamText'>{`${teamsPercentages[1].team}`}</span>
        <span className='col-12 col-sm-2'>{''}</span>
        <span className='col-12 text-start px-1 ps-sm-4 col-sm-5 nflSiteTeamText'>{`${teamsPercentages[1].percent}%`}</span>
      </h4>
      <h4 className='row'>
        <span className='col-12 text-start ps-1 ps-sm-3 ps-lg-5 col-sm-5 nflSiteTeamText'>{`${teamsPercentages[0].team}`}</span>
        <span className='col-12 col-sm-2'>{''}</span>
        <span className='col-12 text-start px-1 ps-sm-4 col-sm-5 nflSiteTeamText'>{`${teamsPercentages[0].percent}%`}</span>
      </h4>
    </div>
  );
};

export const ConferencePercent = (conference) => {
  const conferenceTitle = conference.slice(3);

  return (
    <h3 className='row pt-5 pb-2 conferences'>
      <span className='col-12 text-start text-sm-center col-sm-6'>{`${conferenceTitle}`}</span>
      <span className='col-12 text-start text-sm-center col-sm-6'>{`${percentages[
        conference
      ].toFixed(2)}%`}</span>
    </h3>
  );
};

export const DivisionPercent = (division) => {
  return (
    <h2 className='row pb-sm-5 mb-sm-5'>
      <span className='col-5'>{`${division}`}</span>
      <span className='col-2'>{''}</span>
      <span className='col-5'>{`${percentages[division].toFixed(2)}%`}</span>
    </h2>
  );
};

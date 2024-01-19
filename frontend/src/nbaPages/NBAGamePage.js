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
import Check from '../logos/Check.png';
import XMark from '../logos/XMark.png';

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

  const correctWrongLogo = (value) => {
    console.log(value);
    return value === 100 ? (
      <img src={Check} alt='check' />
    ) : (
      <img src={XMark} alt='XMark' />
    );
  };

  const addPercentText = (text) => {
    return (
      <div>
        <span>{text}</span>
        <span className='timeText'>{'%'}</span>
      </div>
    );
  };

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
        <div className='col-sm-6'>
          <div className='pt-3 pb-3'>{awayTeamName}</div>
          <table class='table table-striped table-dark'>
            <thead>
              <tr>
                <th scope='col'>#</th>
                <th scope='col'>Spread</th>
                <th scope='col'>Over Under</th>
                <th scope='col'>Parlay</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th scope='row'>{`Team Overall`}</th>
                <td>{addPercentText(awayTeamSpreadPercent)}</td>
                <td>{addPercentText(awayTeamOverUnderPercent)}</td>
                <td>{addPercentText(awayTeamParlayPercent)}</td>
              </tr>
              <tr>
                <th scope='row'>{`At ${hour}PM`}</th>
                <td>{addPercentText(awayTeamTimeSpreadPercent)}</td>
                <td>{addPercentText(awayTeamTimeOverUnderPercent)}</td>
                <td>{addPercentText(awayTeamTimeParlayPercent)}</td>
              </tr>
              <tr>
                <th scope='row'>{`When ${todaysDayName}`}</th>
                <td>{addPercentText(awayTeamDaySpreadPercent)}</td>
                <td>{addPercentText(awayTeamDayOverUnderPercent)}</td>
                <td>{addPercentText(awayTeamDayParlayPercent)}</td>
              </tr>
              <tr>
                <th scope='row'>{'1 Game Ago'}</th>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_spread_1`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_overUnder_1`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_parlay_1`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row'>{'2 Games Ago'}</th>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_spread_2`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_overUnder_2`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_parlay_2`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row'>{'3 Games Ago'}</th>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_spread_3`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_overUnder_3`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_parlay_3`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row'>{'4 Games Ago'}</th>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_spread_4`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_overUnder_4`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_parlay_4`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row'>{'5 Games Ago'}</th>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_spread_5`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_overUnder_5`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_parlay_5`
                    ]
                  )}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div className='col-sm-6'>
          <div className='pt-3 pb-3'>{homeTeamName}</div>
          <table class='table table-striped table-dark'>
            <thead>
              <tr>
                <th scope='col'>#</th>
                <th scope='col'>Spread</th>
                <th scope='col'>Over Under</th>
                <th scope='col'>Parlay</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th scope='row'>{`Team Overall`}</th>
                <td>{addPercentText(homeTeamSpreadPercent)}</td>
                <td>{addPercentText(homeTeamOverUnderPercent)}</td>
                <td>{addPercentText(homeTeamParlayPercent)}</td>
              </tr>
              <tr>
                <th scope='row'>{`At ${hour}PM`}</th>
                <td>{addPercentText(homeTeamTimeSpreadPercent)}</td>
                <td>{addPercentText(homeTeamTimeOverUnderPercent)}</td>
                <td>{addPercentText(homeTeamTimeParlayPercent)}</td>
              </tr>
              <tr>
                <th scope='row'>{`When ${todaysDayName}`}</th>
                <td>{addPercentText(homeTeamDaySpreadPercent)}</td>
                <td>{addPercentText(homeTeamDayOverUnderPercent)}</td>
                <td>{addPercentText(homeTeamDayParlayPercent)}</td>
              </tr>
              <tr>
                <th scope='row'>{'1 Game Ago'}</th>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_spread_1`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_overUnder_1`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_parlay_1`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row'>{'2 Games Ago'}</th>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_spread_2`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_overUnder_2`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_parlay_2`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row'>{'3 Games Ago'}</th>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_spread_3`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_overUnder_3`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_parlay_3`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row'>{'4 Games Ago'}</th>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_spread_4`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_overUnder_4`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_parlay_4`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row'>{'5 Games Ago'}</th>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_spread_5`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_overUnder_5`
                    ]
                  )}
                </td>
                <td>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_parlay_5`
                    ]
                  )}
                </td>
              </tr>
            </tbody>
          </table>
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

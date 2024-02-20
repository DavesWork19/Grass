import { useLocation } from 'react-router-dom';
import '../Fonts.css';
import {
  teamStatsText,
  matchUpPageText1,
  matchUpPageText2,
  nbaTeamShortNames,
  legalNbaTeamLogos,
  convertLegalNbaTeamLogos,
} from '../constants';
import { useLayoutEffect } from 'react';
import { todaysGames } from './todaysGames';
import { percentages } from './percentages';
import Check from '../logos/Check.png';
import XMark from '../logos/XMark.png';
import NBAHeader from './Header';

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
  const awayTeamName =
    convertLegalNbaTeamLogos[awayTeam.split('%20').join(' ')];
  const homeTeamName =
    convertLegalNbaTeamLogos[homeTeam.split('%20').join(' ')];
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
    return value === 100 ? (
      <img src={Check} alt='check' />
    ) : (
      <img src={XMark} alt='XMark' />
    );
  };

  const addPercentText = (text) => {
    return <div>{`${text}%`}</div>;
  };

  return (
    <div className='text lightText pb-5 bg-black  container-fluid'>
      <NBAHeader
        title={`${legalNbaTeamLogos[awayTeamName]} at ${legalNbaTeamLogos[homeTeamName]}`}
        link={'gamePage'}
      />

      <div className='row mt-5'>
        <div className='col-12  fs-3'>
          {`${legalNbaTeamLogos[homeTeamName]} predicted to ${homeCover} ${homeTeamSpread}`}
        </div>
        <div className='col-12  fs-3'>
          {`Predicted ${overUnderCoverName} ${overUnder}`}
        </div>
      </div>

      <div className='row pt-5 mt-5 pb-3'>
        <div className='col-sm-6'>
          <table className='table table-striped table-dark'>
            <thead>
              <tr>
                <th scope='col' colSpan={4}>
                  {legalNbaTeamLogos[awayTeamName]}
                </th>
              </tr>
              <tr>
                <th scope='col'></th>
                <th scope='col' className='tableHeaderNormalWeight'>
                  Spread
                </th>
                <th scope='col' className='tableHeaderNormalWeight'>
                  Over Under
                </th>
                <th scope='col' className='tableHeaderNormalWeight'>
                  Parlay
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th
                  scope='row'
                  className='tableHeaderNormalWeight text-start'
                >{`Team Overall`}</th>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(awayTeamSpreadPercent)}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(awayTeamOverUnderPercent)}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(awayTeamParlayPercent)}
                </td>
              </tr>
              <tr>
                <th
                  scope='row'
                  className='tableHeaderNormalWeight text-start'
                >{`At ${hour}PM`}</th>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(awayTeamTimeSpreadPercent)}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(awayTeamTimeOverUnderPercent)}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(awayTeamTimeParlayPercent)}
                </td>
              </tr>
              <tr>
                <th scope='row' className='tableHeaderNormalWeight text-start'>
                  {todaysDayName}
                </th>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(awayTeamDaySpreadPercent)}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(awayTeamDayOverUnderPercent)}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(awayTeamDayParlayPercent)}
                </td>
              </tr>
              <tr>
                <th scope='row' className='tableHeaderNormalWeight text-start'>
                  {'1 Game Ago'}
                </th>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_spread_1`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_overUnder_1`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_parlay_1`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row' className='tableHeaderNormalWeight text-start'>
                  {'2 Games Ago'}
                </th>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_spread_2`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_overUnder_2`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_parlay_2`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row' className='tableHeaderNormalWeight text-start'>
                  {'3 Games Ago'}
                </th>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_spread_3`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_overUnder_3`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_parlay_3`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row' className='tableHeaderNormalWeight text-start'>
                  {'4 Games Ago'}
                </th>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_spread_4`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_overUnder_4`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_parlay_4`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row' className='tableHeaderNormalWeight text-start'>
                  {'5 Games Ago'}
                </th>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_spread_5`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[awayTeamName]}_last_games_overUnder_5`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
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
          <table className='table table-striped table-dark'>
            <thead>
              <tr>
                <th scope='col' colSpan={4}>
                  {legalNbaTeamLogos[homeTeamName]}
                </th>
              </tr>
              <tr>
                <th scope='col'></th>
                <th scope='col' className='tableHeaderNormalWeight'>
                  Spread
                </th>
                <th scope='col' className='tableHeaderNormalWeight'>
                  Over Under
                </th>
                <th scope='col' className='tableHeaderNormalWeight'>
                  Parlay
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th
                  scope='row'
                  className='tableHeaderNormalWeight'
                >{`Team Overall`}</th>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(homeTeamSpreadPercent)}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(homeTeamOverUnderPercent)}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(homeTeamParlayPercent)}
                </td>
              </tr>
              <tr>
                <th
                  scope='row'
                  className='tableHeaderNormalWeight'
                >{`At ${hour}PM`}</th>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(homeTeamTimeSpreadPercent)}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(homeTeamTimeOverUnderPercent)}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(homeTeamTimeParlayPercent)}
                </td>
              </tr>
              <tr>
                <th scope='row' className='tableHeaderNormalWeight'>
                  {todaysDayName}
                </th>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(homeTeamDaySpreadPercent)}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(homeTeamDayOverUnderPercent)}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {addPercentText(homeTeamDayParlayPercent)}
                </td>
              </tr>
              <tr>
                <th scope='row' className='tableHeaderNormalWeight'>
                  {'1 Game Ago'}
                </th>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_spread_1`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_overUnder_1`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_parlay_1`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row' className='tableHeaderNormalWeight'>
                  {'2 Games Ago'}
                </th>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_spread_2`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_overUnder_2`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_parlay_2`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row' className='tableHeaderNormalWeight'>
                  {'3 Games Ago'}
                </th>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_spread_3`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_overUnder_3`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_parlay_3`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row' className='tableHeaderNormalWeight'>
                  {'4 Games Ago'}
                </th>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_spread_4`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_overUnder_4`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_parlay_4`
                    ]
                  )}
                </td>
              </tr>
              <tr>
                <th scope='row' className='tableHeaderNormalWeight'>
                  {'5 Games Ago'}
                </th>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_spread_5`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
                  {correctWrongLogo(
                    percentages[
                      `${nbaTeamShortNames[homeTeamName]}_last_games_overUnder_5`
                    ]
                  )}
                </td>
                <td className='tableHeaderNormalWeight'>
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

      <div className='row pt-5  smallText'>
        <div className='col-12 pt-5'>{matchUpPageText1}</div>
        <div className='col-12'>{matchUpPageText2}</div>
      </div>
    </div>
  );
};

export default NBAGamePage;

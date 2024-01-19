import { useState } from 'react';
import { percentages } from './percentages';
import { todaysGames } from './todaysGames';
import '../Fonts.css';

const OverallPercents = (props) => {
  const [showPercentages, setShowPercentages] = useState(false);

  const spread = percentages['overall_spread'];
  const overUnder = percentages['overall_overUnder'];
  const parlay = percentages['overall_parlay'];
  const today = todaysGames.slice(0, 1)[0];

  const daySpread = percentages[`overall_${today}_spread`];
  const dayOverUnder = percentages[`overall_${today}_overUnder`];
  const dayParlay = percentages[`overall_${today}_parlay`];

  const spread1dayago = percentages[`overall_last_games_spread_1`];
  const overUnder1dayago = percentages[`overall_last_games_overUnder_1`];
  const parlay1dayago = percentages[`overall_last_games_parlay_1`];
  const spread2dayago = percentages[`overall_last_games_spread_2`];
  const overUnder2dayago = percentages[`overall_last_games_overUnder_2`];
  const parlay2dayago = percentages[`overall_last_games_parlay_2`];
  const spread3dayago = percentages[`overall_last_games_spread_3`];
  const overUnder3dayago = percentages[`overall_last_games_overUnder_3`];
  const parlay3dayago = percentages[`overall_last_games_parlay_3`];
  const spread4dayago = percentages[`overall_last_games_spread_4`];
  const overUnder4dayago = percentages[`overall_last_games_overUnder_4`];
  const parlay4dayago = percentages[`overall_last_games_parlay_4`];
  const spread5dayago = percentages[`overall_last_games_spread_5`];
  const overUnder5dayago = percentages[`overall_last_games_overUnder_5`];
  const parlay5dayago = percentages[`overall_last_games_parlay_5`];

  const hours = props.hours;
  const hoursArray = [...hours];

  const handleShowPercentages = () => {
    setShowPercentages(true);
  };

  const handleTooManyPercentages = () => {
    setShowPercentages(false);
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
    <div className='lightText me-2'>
      {showPercentages ? (
        <div className='row'>
          <div className='col-12'>
            <button
              className='btn btn-light mb-5'
              onClick={handleTooManyPercentages}
            >
              {'Too Many Percentages'}
            </button>
            <table class='table table-striped table-dark'>
              <thead>
                <tr>
                  <th scope='col'>Overall</th>
                  <th scope='col'>Spread</th>
                  <th scope='col'>Over Under</th>
                  <th scope='col'>Parlay</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope='row'>{`Overall`}</th>
                  <td>{addPercentText(spread)}</td>
                  <td>{addPercentText(overUnder)}</td>
                  <td>{addPercentText(parlay)}</td>
                </tr>
                <tr>
                  <th scope='row'>{`When ${today}`}</th>
                  <td>{addPercentText(daySpread)}</td>
                  <td>{addPercentText(dayOverUnder)}</td>
                  <td>{addPercentText(dayParlay)}</td>
                </tr>
                {hoursArray.map((hour) => (
                  <tr key={hour}>
                    <th scope='row'>{`At ${hour}PM`}</th>
                    <td>
                      {addPercentText(
                        percentages[`overall_Time_${hour}_${hour}59_spread`]
                      )}
                    </td>
                    <td>
                      {addPercentText(
                        percentages[`overall_Time_${hour}_${hour}59_overUnder`]
                      )}
                    </td>
                    <td>
                      {addPercentText(
                        percentages[`overall_Time_${hour}_${hour}59_parlay`]
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <table class='table table-striped table-dark'>
              <thead>
                <tr>
                  <th scope='col'>Overall</th>
                  <th scope='col'>Spread</th>
                  <th scope='col'>Over Under</th>
                  <th scope='col'>Parlay</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope='row'>{`1 Day Ago`}</th>
                  <td>{addPercentText(spread1dayago)}</td>
                  <td>{addPercentText(overUnder1dayago)}</td>
                  <td>{addPercentText(parlay1dayago)}</td>
                </tr>
                <tr>
                  <th scope='row'>{`2 Days Ago`}</th>
                  <td>{addPercentText(spread2dayago)}</td>
                  <td>{addPercentText(overUnder2dayago)}</td>
                  <td>{addPercentText(parlay2dayago)}</td>
                </tr>
                <tr>
                  <th scope='row'>{`3 Days Ago`}</th>
                  <td>{addPercentText(spread3dayago)}</td>
                  <td>{addPercentText(overUnder3dayago)}</td>
                  <td>{addPercentText(parlay3dayago)}</td>
                </tr>
                <tr>
                  <th scope='row'>{`4 Days Ago`}</th>
                  <td>{addPercentText(spread4dayago)}</td>
                  <td>{addPercentText(overUnder4dayago)}</td>
                  <td>{addPercentText(parlay4dayago)}</td>
                </tr>
                <tr>
                  <th scope='row'>{`5 Days Ago`}</th>
                  <td>{addPercentText(spread5dayago)}</td>
                  <td>{addPercentText(overUnder5dayago)}</td>
                  <td>{addPercentText(parlay5dayago)}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <button className='btn btn-light' onClick={handleShowPercentages}>
          {'Show Overall Percentages'}
        </button>
      )}
    </div>
  );
};

export default OverallPercents;

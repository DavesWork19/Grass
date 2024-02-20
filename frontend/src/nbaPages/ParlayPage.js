import '../Fonts.css';
import { useState } from 'react';
import NBAHeader from './Header';
import Parlays from './Parlays';
import ParlayPercents from './ParlayPercents';
import { smallParlay } from './smallParlay';
import { decentParlay } from './decentParlay';
import { largeParlay } from './largeParlay';
import { massiveParlay } from './massiveParlay';
import {
  parlay1Percentages,
  parlay2Percentages,
  parlay3Percentages,
  parlay4Percentages,
} from './parlayPercentages';
import { footerMessageParlayPage } from '../constants';

const ParlayPage = () => {
  const [showParlay1Percents, setShowParlay1Percents] = useState(false);
  const [showParlay2Percents, setShowParlay2Percents] = useState(false);
  const [showParlay3Percents, setShowParlay3Percents] = useState(false);
  const [showParlay4Percents, setShowParlay4Percents] = useState(false);

  const showSmallParlay = smallParlay.length > 0;
  const showDecentParlay = decentParlay.length > 0;
  const showLargeParlay = largeParlay.length > 0;
  const showMassiveParlay = massiveParlay.length > 0;
  const showP3 = parlay3Percentages.length > 0;
  const showP4 = parlay4Percentages.length > 0;

  const parlay1PCopy = [...parlay1Percentages];
  const parlay2PCopy = [...parlay2Percentages];
  const parlay3PCopy = [...parlay3Percentages];
  const parlay4PCopy = [...parlay4Percentages];

  const handleShowPercentages = (parlay, showOrHide) => {
    if (parlay === 1) {
      if (showOrHide === 1) {
        setShowParlay1Percents(true);
      } else {
        setShowParlay1Percents(false);
      }
    } else if (parlay === 2) {
      if (showOrHide === 1) {
        setShowParlay2Percents(true);
      } else {
        setShowParlay2Percents(false);
      }
    } else if (parlay === 3) {
      if (showOrHide === 1) {
        setShowParlay3Percents(true);
      } else {
        setShowParlay3Percents(false);
      }
    } else if (parlay === 4) {
      if (showOrHide === 1) {
        setShowParlay4Percents(true);
      } else {
        setShowParlay4Percents(false);
      }
    }
  };

  return (
    <div className='container-fluid bg-black text lightText'>
      <NBAHeader title={'Welcome Ése'} />

      <div className='pt-3'>
        <h2>{"Today's Parlays"}</h2>
        {showSmallParlay && (
          <div className='mt-5'>
            <h2>{'Parlay 1'}</h2>
            <Parlays parlay={smallParlay} />
          </div>
        )}
        {showDecentParlay && (
          <div className='mt-5'>
            <h2>{'Parlay 2'}</h2>
            <Parlays parlay={decentParlay} />
          </div>
        )}
        {showLargeParlay && (
          <div className='mt-5'>
            <h2>{'Parlay 3'}</h2>
            <Parlays parlay={largeParlay} />
          </div>
        )}
        {showMassiveParlay && (
          <div className='mt-5'>
            <h2>{'Other Parlay'}</h2>
            <Parlays parlay={massiveParlay} />
          </div>
        )}
      </div>

      <div className='mt-5 pt-5'>
        <h2>{'Parlay Hits'}</h2>
        <div className='my-3 py-3'>
          {showParlay1Percents ? (
            <div>
              <button
                className={'btn bg-dark lightText'}
                onClick={() => handleShowPercentages(1, 0)}
              >
                {'Hide Parlay 1'}
              </button>
              <ParlayPercents parlay={parlay1PCopy.reverse()} />
            </div>
          ) : (
            <button
              className={'btn bg-dark lightText'}
              onClick={() => handleShowPercentages(1, 1)}
            >
              {'Parlay 1'}
            </button>
          )}
        </div>
        <div className='my-3 py-3'>
          {showParlay2Percents ? (
            <div>
              <button
                className='btn bg-dark lightText'
                onClick={() => handleShowPercentages(2, 0)}
              >
                {'Hide Parlay 2'}
              </button>
              <ParlayPercents parlay={parlay2PCopy.reverse()} />
            </div>
          ) : (
            <button
              className='btn bg-dark lightText'
              onClick={() => handleShowPercentages(2, 1)}
            >
              {'Parlay 2'}
            </button>
          )}
        </div>
        {showP3 && (
          <div className='my-3 py-3'>
            {showParlay3Percents ? (
              <div>
                <button
                  className='btn bg-dark lightText'
                  onClick={() => handleShowPercentages(3, 0)}
                >
                  {'Hide Parlay 4'}
                </button>
                <ParlayPercents parlay={parlay3PCopy.reverse()} />
              </div>
            ) : (
              <button
                className='btn bg-dark lightText'
                onClick={() => handleShowPercentages(3, 1)}
              >
                {'Parlay 3'}
              </button>
            )}
          </div>
        )}
        {showP4 && (
          <div className='my-3 py-3'>
            {showParlay4Percents ? (
              <div>
                <button
                  className='btn bg-dark lightText'
                  onClick={() => handleShowPercentages(4, 0)}
                >
                  {'Hide Parlay 4'}
                </button>
                <ParlayPercents parlay={parlay4PCopy.reverse()} />
              </div>
            ) : (
              <button
                className='btn bg-dark lightText'
                onClick={() => handleShowPercentages(4, 1)}
              >
                {'Parlay 4'}
              </button>
            )}
          </div>
        )}
      </div>

      <footer className='row mt-5 pt-5'>
        <div className='col-12 lightText'>{footerMessageParlayPage}</div>
      </footer>
    </div>
  );
};

export default ParlayPage;

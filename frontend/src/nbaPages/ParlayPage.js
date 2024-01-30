import '../Fonts.css';
import { useLayoutEffect } from 'react';
import { smallParlay } from './smallParlay';
import { decentParlay } from './decentParlay';
import { largeParlay } from './largeParlay';
import { massiveParlay } from './massiveParlay';
import NBAHeader from './Header';
import Parlays from './Parlays';

const ParlayPage = () => {
  useLayoutEffect(() => {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth',
    });
  });

  const showSmallParlay = smallParlay.length > 0;
  const showDecentParlay = decentParlay.length > 0;
  const showLargeParlay = largeParlay.length > 0;
  const showMassiveParlay = massiveParlay.length > 0;

  return (
    <div className='container-fluid bg-black timeText lightText vh-100'>
      <NBAHeader title={'Welcome Ése'} />

      <div>
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
            <h2>{'Parlay 4'}</h2>
            <Parlays parlay={massiveParlay} />
          </div>
        )}
      </div>
    </div>
  );
};

export default ParlayPage;

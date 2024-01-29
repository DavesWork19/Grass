import '../Fonts.css';
import { useLayoutEffect } from 'react';
import SmallParlays from './SmallParlays';
import { smallParlay } from './smallParlay';
import DecentParlays from './DecentParlays';
import { decentParlay } from './decentParlay';
import LargeParlays from './LargeParlays';
import { largeParlay } from './largeParlay';
import MassiveParlays from './MassiveParlays';
import { massiveParlay } from './massiveParlay';

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
    <div className='container-fluid'>
      <h1 className=''>{'Whats good esse'}</h1>
      <div>
        {showSmallParlay && (
          <div className='mt-5'>
            <h2>{'Parlay 1'}</h2>
            <SmallParlays />
          </div>
        )}
        {showDecentParlay && (
          <div className='mt-5'>
            <h2>{'Parlay 2'}</h2>
            <DecentParlays />
          </div>
        )}
        {showLargeParlay && (
          <div className='mt-5'>
            <h2>{'Parlay 3'}</h2>
            <LargeParlays />
          </div>
        )}
        {showMassiveParlay && (
          <div className='mt-5'>
            <h2>{'Parlay 4'}</h2>
            <MassiveParlays />
          </div>
        )}
      </div>
    </div>
  );
};

export default ParlayPage;

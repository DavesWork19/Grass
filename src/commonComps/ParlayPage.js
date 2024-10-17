import '../Fonts.css';
import GamblingHeader from '../commonComps/GamblingHeader';
// import Parlays from '../commonComps/Parlays';
// import { smallParlay } from './smallParlay';
// import { decentParlay } from './decentParlay';
// import { largeParlay } from './largeParlay';
// import { massiveParlay } from './massiveParlay';
// import {
//   parlay1Percentages,
//   parlay2Percentages,
//   parlay3Percentages,
//   parlay4Percentages,
// } from './parlayPercentages';
import {
  footerMessageParlayPage,
  footerParlayHitMessageParlay,
} from '../constants';
// import ParlayHitsTable from '../commonComps/ParlayHitsTable';

const ParlayPage = (props) => {
  const sport = props.sport;
  //   const showSmallParlay = smallParlay.length > 0;
  //   const showDecentParlay = decentParlay.length > 0;
  //   const showLargeParlay = largeParlay.length > 0;
  //   const showMassiveParlay = massiveParlay.length > 0;
  //   const showP1 = parlay1Percentages.length > 0;
  //   const showP2 = parlay2Percentages.length > 0;
  //   const showP3 = parlay3Percentages.length > 0;
  //   const showP4 = parlay4Percentages.length > 0;

  //   const parlay1PCopy = [...parlay1Percentages];
  //   const parlay2PCopy = [...parlay2Percentages];
  //   const parlay3PCopy = [...parlay3Percentages];
  //   const parlay4PCopy = [...parlay4Percentages];

  return (
    <div className='container-fluid bg-black text lightText'>
      <GamblingHeader title={'Welcome Ése'} link={sport} />
      {/* 
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

      {showP1 && (
        <ParlayHitsTable
          title='Parlay 1 Hits'
          parlay={parlay1PCopy.reverse()}
        />
      )}
      {showP2 && (
        <ParlayHitsTable
          title='Parlay 2 Hits'
          parlay={parlay2PCopy.reverse()}
        />
      )}
      {showP3 && (
        <ParlayHitsTable
          title='Parlay 3 Hits'
          parlay={parlay3PCopy.reverse()}
        />
      )}
      {showP4 && (
        <ParlayHitsTable
          title='Parlay 4 Hits'
          parlay={parlay4PCopy.reverse()}
        />
      )} */}

      <footer className='row mt-5 pt-5'>
        <div className='col-12 lightText'>{footerMessageParlayPage}</div>
        <div className='col-12 lightText'>{footerParlayHitMessageParlay}</div>
      </footer>
    </div>
  );
};

export default ParlayPage;

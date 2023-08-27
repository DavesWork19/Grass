import { Link } from 'react-router-dom';
import './MatchupsPage.css';
import { upcomingWeekData } from './upcomingWeekData.js';
import {
  buf,
  mia,
  nwe,
  nyj,
  cin,
  cle,
  pit,
  rav,
  clt,
  htx,
  jax,
  oti,
  den,
  kan,
  rai,
  sdg,
  dal,
  nyg,
  phi,
  was,
  chi,
  det,
  gnb,
  min,
  atl,
  car,
  nor,
  tam,
  crd,
  ram,
  sea,
  sfo,
} from './constants';
import ATLogo from './logos/atLogo1.png';
import bufLogo from './logos/bufLogo.png';
import nweLogo from './logos/nweLogo.png';
import nyjLogo from './logos/nyjLogo.png';
import miaLogo from './logos/miaLogo.png';
import cinLogo from './logos/cinLogo.png';
import cleLogo from './logos/cleLogo.png';
import pitLogo from './logos/pitLogo.png';
import ravLogo from './logos/ravLogo.png';
import cltLogo from './logos/cltLogo.png';
import htxLogo from './logos/htxLogo.png';
import jaxLogo from './logos/jaxLogo.png';
import otiLogo from './logos/otiLogo.png';
import denLogo from './logos/denLogo.png';
import kanLogo from './logos/kanLogo.png';
import raiLogo from './logos/raiLogo.png';
import sdgLogo from './logos/sdgLogo.png';

import dalLogo from './logos/dalLogo.png';
import nygLogo from './logos/nygLogo.png';
import phiLogo from './logos/phiLogo.png';
import wasLogo from './logos/wasLogo.png';
import chiLogo from './logos/chiLogo.png';
import detLogo from './logos/detLogo.png';
import gnbLogo from './logos/gnbLogo.png';
import minLogo from './logos/minLogo.png';
import atlLogo from './logos/atlLogo.png';
import carLogo from './logos/carLogo.png';
import norLogo from './logos/norLogo.png';
import tamLogo from './logos/tamLogo.png';
import crdLogo from './logos/crdLogo.png';
import ramLogo from './logos/ramLogo.png';
import seaLogo from './logos/seaLogo.png';
import sfoLogo from './logos/sfoLogo.png';

const Matchups = () => {
  const setHomeTeam = (homeTeam) => {
    if (homeTeam === buf) {
      return <img src={bufLogo} alt='logo' />;
    } else if (homeTeam === mia) {
      return <img src={miaLogo} alt='logo' />;
    } else if (homeTeam === nwe) {
      return <img src={nweLogo} alt='logo' />;
    } else if (homeTeam === nyj) {
      return <img src={nyjLogo} alt='logo' />;
    } else if (homeTeam === cin) {
      return <img src={cinLogo} alt='logo' />;
    } else if (homeTeam === cle) {
      return <img src={cleLogo} alt='logo' />;
    } else if (homeTeam === pit) {
      return <img src={pitLogo} alt='logo' />;
    } else if (homeTeam === rav) {
      return <img src={ravLogo} alt='logo' />;
    } else if (homeTeam === clt) {
      return <img src={cltLogo} alt='logo' />;
    } else if (homeTeam === htx) {
      return <img src={htxLogo} alt='logo' />;
    } else if (homeTeam === jax) {
      return <img src={jaxLogo} alt='logo' />;
    } else if (homeTeam === oti) {
      return <img src={otiLogo} alt='logo' />;
    } else if (homeTeam === den) {
      return <img src={denLogo} alt='logo' />;
    } else if (homeTeam === kan) {
      return <img src={kanLogo} alt='logo' />;
    } else if (homeTeam === rai) {
      return <img src={raiLogo} alt='logo' />;
    } else if (homeTeam === sdg) {
      return <img src={sdgLogo} alt='logo' />;
    } else if (homeTeam === dal) {
      return <img src={dalLogo} alt='logo' />;
    } else if (homeTeam === nyg) {
      return <img src={nygLogo} alt='logo' />;
    } else if (homeTeam === phi) {
      return <img src={phiLogo} alt='logo' />;
    } else if (homeTeam === was) {
      return <img src={wasLogo} alt='logo' />;
    } else if (homeTeam === chi) {
      return <img src={chiLogo} alt='logo' />;
    } else if (homeTeam === det) {
      return <img src={detLogo} alt='logo' />;
    } else if (homeTeam === gnb) {
      return <img src={gnbLogo} alt='logo' />;
    } else if (homeTeam === min) {
      return <img src={minLogo} alt='logo' />;
    } else if (homeTeam === atl) {
      return <img src={atlLogo} alt='logo' />;
    } else if (homeTeam === car) {
      return <img src={carLogo} alt='logo' />;
    } else if (homeTeam === nor) {
      return <img src={norLogo} alt='logo' />;
    } else if (homeTeam === tam) {
      return <img src={tamLogo} alt='logo' />;
    } else if (homeTeam === crd) {
      return <img src={crdLogo} alt='logo' />;
    } else if (homeTeam === ram) {
      return <img src={ramLogo} alt='logo' />;
    } else if (homeTeam === sea) {
      return <img src={seaLogo} alt='logo' />;
    } else if (homeTeam === sfo) {
      return <img src={sfoLogo} alt='logo' />;
    }
  };

  const setAwayTeam = (awayTeam) => {
    if (awayTeam === buf) {
      return <img src={bufLogo} alt='logo' />;
    } else if (awayTeam === mia) {
      return <img src={miaLogo} alt='logo' />;
    } else if (awayTeam === nwe) {
      return <img src={nweLogo} alt='logo' />;
    } else if (awayTeam === nyj) {
      return <img src={nyjLogo} alt='logo' />;
    } else if (awayTeam === cin) {
      return <img src={cinLogo} alt='logo' />;
    } else if (awayTeam === cle) {
      return <img src={cleLogo} alt='logo' />;
    } else if (awayTeam === pit) {
      return <img src={pitLogo} alt='logo' />;
    } else if (awayTeam === rav) {
      return <img src={ravLogo} alt='logo' />;
    } else if (awayTeam === clt) {
      return <img src={cltLogo} alt='logo' />;
    } else if (awayTeam === htx) {
      return <img src={htxLogo} alt='logo' />;
    } else if (awayTeam === jax) {
      return <img src={jaxLogo} alt='logo' />;
    } else if (awayTeam === oti) {
      return <img src={otiLogo} alt='logo' />;
    } else if (awayTeam === den) {
      return <img src={denLogo} alt='logo' />;
    } else if (awayTeam === kan) {
      return <img src={kanLogo} alt='logo' />;
    } else if (awayTeam === rai) {
      return <img src={raiLogo} alt='logo' />;
    } else if (awayTeam === sdg) {
      return <img src={sdgLogo} alt='logo' />;
    } else if (awayTeam === dal) {
      return <img src={dalLogo} alt='logo' />;
    } else if (awayTeam === nyg) {
      return <img src={nygLogo} alt='logo' />;
    } else if (awayTeam === phi) {
      return <img src={phiLogo} alt='logo' />;
    } else if (awayTeam === was) {
      return <img src={wasLogo} alt='logo' />;
    } else if (awayTeam === chi) {
      return <img src={chiLogo} alt='logo' />;
    } else if (awayTeam === det) {
      return <img src={detLogo} alt='logo' />;
    } else if (awayTeam === gnb) {
      return <img src={gnbLogo} alt='logo' />;
    } else if (awayTeam === min) {
      return <img src={minLogo} alt='logo' />;
    } else if (awayTeam === atl) {
      return <img src={atlLogo} alt='logo' />;
    } else if (awayTeam === car) {
      return <img src={carLogo} alt='logo' />;
    } else if (awayTeam === nor) {
      return <img src={norLogo} alt='logo' />;
    } else if (awayTeam === tam) {
      return <img src={tamLogo} alt='logo' />;
    } else if (awayTeam === crd) {
      return <img src={crdLogo} alt='logo' />;
    } else if (awayTeam === ram) {
      return <img src={ramLogo} alt='logo' />;
    } else if (awayTeam === sea) {
      return <img src={seaLogo} alt='logo' />;
    } else if (awayTeam === sfo) {
      return <img src={sfoLogo} alt='logo' />;
    }
  };

  return upcomingWeekData.map((data) => {
    const [awayTeam, homeTeam, Day] = data.split('_');
    return (
      <Link to={`${awayTeam}At${homeTeam}`}>
        <button className='btn btn-light mt-1 mb-5'>
          <span>
            {setAwayTeam(awayTeam)}
            <img className='ps-1 pe-1' src={ATLogo} alt='atLogo' />
            {setHomeTeam(homeTeam)}
          </span>
        </button>
      </Link>
    );
  });
};

export default Matchups;

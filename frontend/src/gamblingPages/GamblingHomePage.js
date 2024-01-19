import '../Fonts.css';
import { Link } from 'react-router-dom';
import GamblingHeader from './GamblingHeader';
import { secretCode } from '../constants';

const GamblingHomePage = () => {
  return (
    <main className='container-fluid vh-100 nflSiteTextRaw lightText bg-black'>
      <GamblingHeader />
      <div className='pt-5'>
        <Link to={`/${secretCode}/Basketball`} className='pt-5 text-end'>
          <button className=' text-dark btn btn-outline-secondary btn-light gamblingButton'>
            {'Basketball'}
          </button>
        </Link>
      </div>
      <div className='pt-5'>
        <Link to={`/${secretCode}/Football`} className='pt-5 text-end'>
          <button className='nflSiteTextRaw btn btn-outline-secondary gamblingButton'>
            {'Football'}
          </button>
        </Link>
      </div>
      <div className='pt-5'>
        <Link to='/' className='pt-5 text-end'>
          <button className='nflSiteTextRaw btn btn-outline-secondary gamblingButton'>
            {'DIGITS'}
          </button>
        </Link>
      </div>
    </main>
  );
};

export default GamblingHomePage;

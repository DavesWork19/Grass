import '../Fonts.css';
import { Link } from 'react-router-dom';
import GamblingHeader from '../commonComps/GamblingHeader';
import { secretCode } from '../constants';

const GamblingHomePage = () => {
  return (
    <main className='container-fluid vh-100 boldText lightText bg-black'>
      <GamblingHeader link={'home'} />
      <div className='pt-5'>
        <Link to={`/${secretCode}/Football`} className='pt-5 text-end'>
          <button className='text-dark btn btn-outline-secondary btn-light gamblingButton'>
            {'FOOTBALL'}
          </button>
        </Link>
      </div>
      <div className='pt-5'>
        <Link to={`/${secretCode}/Basketball`} className='pt-5 text-end'>
          <button className='text-dark btn btn-outline-secondary btn-light gamblingButton'>
            {'BASKETBALL'}
          </button>
        </Link>
      </div>
      <div className='pt-5'>
        <Link to='/' className='pt-5 text-end'>
          <button className='boldText btn btn-outline-secondary gamblingButton'>
            {'DIGITS'}
          </button>
        </Link>
      </div>
    </main>
  );
};

export default GamblingHomePage;

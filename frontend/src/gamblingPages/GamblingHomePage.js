import '../Fonts.css';
import { Link } from 'react-router-dom';
import GamblingHeader from './GamblingHeader';

const GamblingHomePage = () => {
  return (
    <main className='container-fluid vh-100 nflSiteTextRaw lightText bg-black'>
      <GamblingHeader />
      <div className='pt-5'>
        <Link to='/2332220/Football' className='pt-5 text-end'>
          <button className='nflSiteTextRaw btn btn-outline-secondary'>
            {'NFL'}
          </button>
        </Link>
      </div>
      <div className='pt-5'>
        <Link to='/2332220/Basketball' className='pt-5 text-end'>
          <button className='nflSiteTextRaw btn btn-outline-secondary'>
            {'NBA'}
          </button>
        </Link>
      </div>
      <div className='pt-5'>
        <Link to='/' className='pt-5 text-end'>
          <button className='nflSiteTextRaw btn btn-outline-secondary'>
            {'DIGITS'}
          </button>
        </Link>
      </div>
    </main>
  );
};

export default GamblingHomePage;

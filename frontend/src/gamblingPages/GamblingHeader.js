import numbersLogo from './NumbersLogo.svg';
import '../Fonts.css';

const GamblingHeader = () => {
  return (
    <div
      className={'container text-center pb-4 pt-3 border-bottom border-dark'}
    >
      <div className='row'>
        <h1 className='col-9 fs-3 my-auto regularText'>
          {'Theeee Numbers Game ???'}
        </h1>
        <img
          className='col-3 gamblingLogo'
          src={numbersLogo}
          alt='NumberIcon'
        />
      </div>
    </div>
  );
};

export default GamblingHeader;

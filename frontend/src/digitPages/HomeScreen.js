import { useNavigate, useLocation } from 'react-router-dom';
import InfoButton from './InfoButton';
import { GREETINGS } from '../constants';
import numbersLogo from './NumbersLogo.svg';
import '../Fonts.css';
import './HomeScreen.css';

const HomeScreen = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const previousTime = location.state?.time;
  const randomGreeting =
    GREETINGS[Math.floor(Math.random() * GREETINGS.length)];

  const handleButtonClick = (navigation) => {
    navigate(navigation);
  };

  return (
    <>
      <div
        className={'container text-center pb-4 pt-3 border-bottom border-dark'}
      >
        <div className='row'>
          <h1 className='col-8 fs-3 my-auto regularText'>
            {'The Numbers Game'}
          </h1>
          <img className='col-2 pe-0 ms-4' src={numbersLogo} alt='NumberIcon' />
        </div>
      </div>
      <main className='container pt-5 mt-5 text-center'>
        <div className='row'>
          <div className='col-12 fs-1 pb-5 mb-5 regularText'>
            {randomGreeting}
          </div>
        </div>
        <div className='row'>
          <button
            type='button'
            onClick={() => handleButtonClick('/daGame')}
            className='btn btn-dark border col m-2 regularText'
          >
            <h2>Start!</h2>
          </button>
        </div>
        <div className='row'>
          <div className='col-12 fs-1 pt-2 regularText'>
            {previousTime ? (
              <div>
                Previous Time:<div className='fs-3'>{previousTime} seconds</div>
              </div>
            ) : null}
          </div>
        </div>
        <InfoButton />
      </main>
    </>
  );
};

export default HomeScreen;

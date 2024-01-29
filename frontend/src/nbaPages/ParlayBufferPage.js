import '../Fonts.css';
import { useLayoutEffect } from 'react';
import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { parlaySecretCode2, secretCode2 } from '../constants';

const ParlayBufferPage = () => {
  useLayoutEffect(() => {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth',
    });
  });
  const navigate = useNavigate();
  const [guess, setGuess] = useState('');
  const buttonRef = useRef(null);

  const handleGuess = (userGuess) => {
    if (userGuess === 'B') {
      const newGuess = guess.substring(0, guess.length - 1);
      setGuess(newGuess);
    } else {
      const newGuess = guess.concat(userGuess);
      setGuess(newGuess);
      const newGuessInt = parseInt(newGuess);

      if (newGuessInt === parseInt(secretCode2)) {
        setTimeout(() => {
          navigate(`${parlaySecretCode2}`);
        }, 10);
      }
    }
  };

  return (
    <div className='container-fluid pt-5 mt-5'>
      <div className='container pt-5'>
        <div className='row'>
          <div className='col-12 p-2 fs-3'>{!!guess ? guess : '_'}</div>
        </div>
        <div className='row border border-dark rounded-2'>
          <div className='col-12'>
            <div className='row'>
              <button
                onClick={(event) => handleGuess('1', event)}
                ref={buttonRef}
                className='btn btn-outline-dark col-4 p-2 fs-3'
              >
                {1}
              </button>
              <button
                onClick={(event) => handleGuess('2', event)}
                ref={buttonRef}
                className='btn btn-outline-dark col-4 p-2 fs-3'
              >
                {2}
              </button>
              <button
                onClick={(event) => handleGuess('3', event)}
                ref={buttonRef}
                className='btn btn-outline-dark col-4 p-2 fs-3'
              >
                {3}
              </button>
            </div>
            <div className='row'>
              <button
                onClick={(event) => handleGuess('4', event)}
                ref={buttonRef}
                className='btn btn-outline-dark col-4 p-2 fs-3'
              >
                {4}
              </button>
              <button
                onClick={(event) => handleGuess('5', event)}
                ref={buttonRef}
                className='btn btn-outline-dark col-4 p-2 fs-3'
              >
                {5}
              </button>
              <button
                onClick={(event) => handleGuess('6', event)}
                ref={buttonRef}
                className='btn btn-outline-dark col-4 p-2 fs-3'
              >
                {6}
              </button>
            </div>
            <div className='row'>
              <button
                onClick={(event) => handleGuess('7', event)}
                ref={buttonRef}
                className='btn btn-outline-dark col-4 p-2 fs-3'
              >
                {7}
              </button>
              <button
                onClick={(event) => handleGuess('8', event)}
                ref={buttonRef}
                className='btn btn-outline-dark col-4 p-2 fs-3'
              >
                {8}
              </button>
              <button
                onClick={(event) => handleGuess('9', event)}
                ref={buttonRef}
                className='btn btn-outline-dark col-4 p-2 fs-3'
              >
                {9}
              </button>
            </div>
            <div className='row'>
              <button
                onClick={(event) => handleGuess('0', event)}
                ref={buttonRef}
                className='btn btn-outline-dark col-12 p-2 fs-3'
              >
                {0}
              </button>
            </div>
            <div className='row'>
              <button
                onClick={(event) => handleGuess('B', event)}
                ref={buttonRef}
                className='btn btn-outline-dark col-12 p-2 fs-3'
              >
                {'BACK'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ParlayBufferPage;

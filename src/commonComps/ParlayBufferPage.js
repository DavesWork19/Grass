import '../Fonts.css';
import { useLayoutEffect } from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { parlaySecretCode2 } from '../constants';
import GamblingHeader from './GamblingHeader';

const ParlayBufferPage = () => {
  useLayoutEffect(() => {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth',
    });
  });
  const hoverButton = 'bg-dark';
  const regButton = 'bg-black text-secondary';
  const navigate = useNavigate();
  const [guess, setGuess] = useState('');
  const [btnHover1, setBtnHover1] = useState(regButton);
  const [btnHover2, setBtnHover2] = useState(regButton);
  const [btnHover3, setBtnHover3] = useState(regButton);
  const [btnHover4, setBtnHover4] = useState(regButton);
  const [btnHover5, setBtnHover5] = useState(regButton);
  const [btnHover6, setBtnHover6] = useState(regButton);
  const [btnHover7, setBtnHover7] = useState(regButton);
  const [btnHover8, setBtnHover8] = useState(regButton);
  const [btnHover9, setBtnHover9] = useState(regButton);
  const [btnHover0, setBtnHover0] = useState(regButton);
  const [btnHoverB, setBtnHoverB] = useState(regButton);

  const updateButtonHover = (button) => {
    if (button === 'B') {
      setBtnHoverB(hoverButton);
      setTimeout(() => {
        setBtnHoverB(regButton);
      }, 175);
    } else if (button === '1') {
      setBtnHover1(hoverButton);
      setTimeout(() => {
        setBtnHover1(regButton);
      }, 175);
    } else if (button === '2') {
      setBtnHover2(hoverButton);
      setTimeout(() => {
        setBtnHover2(regButton);
      }, 175);
    } else if (button === '3') {
      setBtnHover3(hoverButton);
      setTimeout(() => {
        setBtnHover3(regButton);
      }, 175);
    } else if (button === '4') {
      setBtnHover4(hoverButton);
      setTimeout(() => {
        setBtnHover4(regButton);
      }, 175);
    } else if (button === '5') {
      setBtnHover5(hoverButton);
      setTimeout(() => {
        setBtnHover5(regButton);
      }, 175);
    } else if (button === '6') {
      setBtnHover6(hoverButton);
      setTimeout(() => {
        setBtnHover6(regButton);
      }, 175);
    } else if (button === '7') {
      setBtnHover7(hoverButton);
      setTimeout(() => {
        setBtnHover7(regButton);
      }, 175);
    } else if (button === '8') {
      setBtnHover8(hoverButton);
      setTimeout(() => {
        setBtnHover8(regButton);
      }, 175);
    } else if (button === '9') {
      setBtnHover9(hoverButton);
      setTimeout(() => {
        setBtnHover9(regButton);
      }, 175);
    } else if (button === '0') {
      setBtnHover0(hoverButton);
      setTimeout(() => {
        setBtnHover0(regButton);
      }, 175);
    }
  };

  const handleGuess = (userGuess) => {
    if (userGuess === 'B') {
      const newGuess = guess.substring(0, guess.length - 1);
      setGuess(newGuess);
    } else {
      const newGuess = guess.concat(userGuess);
      setGuess(newGuess);
      const newGuessInt = parseInt(newGuess);

      if (newGuessInt === parseInt(parlaySecretCode2)) {
        setTimeout(() => {
          navigate(`${parlaySecretCode2}`);
        }, 10);
      }
    }
    updateButtonHover(userGuess);
  };

  return (
    <div className='bg-black py-5 lightText vh-100'>
      <GamblingHeader title={'Parlays'} link={'back'} />
      <div className='container pt-5'>
        <div className='row'>
          <div className='col-12 p-2 fs-3'>{!!guess ? guess : '_'}</div>
        </div>
        <div className='row border border-secondary rounded-2'>
          <div className='col-12'>
            <div className='row'>
              <button
                onClick={() => handleGuess('1')}
                className={`btn btn-outline-dark ${btnHover1} col-4 p-2 fs-3 border-secondary`}
              >
                {1}
              </button>
              <button
                onClick={() => handleGuess('2')}
                className={`btn btn-outline-dark ${btnHover2} col-4 p-2 fs-3 border-secondary`}
              >
                {2}
              </button>
              <button
                onClick={() => handleGuess('3')}
                className={`btn btn-outline-dark ${btnHover3} col-4 p-2 fs-3 border-secondary`}
              >
                {3}
              </button>
            </div>
            <div className='row'>
              <button
                onClick={() => handleGuess('4')}
                className={`btn btn-outline-dark ${btnHover4} col-4 p-2 fs-3 border-secondary`}
              >
                {4}
              </button>
              <button
                onClick={() => handleGuess('5')}
                className={`btn btn-outline-dark ${btnHover5} col-4 p-2 fs-3 border-secondary`}
              >
                {5}
              </button>
              <button
                onClick={() => handleGuess('6')}
                className={`btn btn-outline-dark ${btnHover6} col-4 p-2 fs-3 border-secondary`}
              >
                {6}
              </button>
            </div>
            <div className='row'>
              <button
                onClick={() => handleGuess('7')}
                className={`btn btn-outline-dark ${btnHover7} col-4 p-2 fs-3 border-secondary`}
              >
                {7}
              </button>
              <button
                onClick={() => handleGuess('8')}
                className={`btn btn-outline-dark ${btnHover8} col-4 p-2 fs-3 border-secondary`}
              >
                {8}
              </button>
              <button
                onClick={() => handleGuess('9')}
                className={`btn btn-outline-dark ${btnHover9} col-4 p-2 fs-3 border-secondary`}
              >
                {9}
              </button>
            </div>
            <div className='row'>
              <button
                onClick={() => handleGuess('0')}
                className={`btn btn-outline-dark ${btnHover0} col-12 p-2 fs-3 border-secondary`}
              >
                {0}
              </button>
            </div>
            <div className='row'>
              <button
                onClick={() => handleGuess('B')}
                className={`btn btn-outline-dark ${btnHoverB} col-12 p-2 fs-3 border-secondary`}
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

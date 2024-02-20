import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { secretCode } from '../constants';

const NumberPad = (props) => {
  const updateCount = props.data[0];
  const finalResult = props.data[1];
  const firstNumber = props.data[2];
  const operation = props.data[3];
  const secondNumber = props.data[4];
  const bgColor = props.data[5];

  const navigate = useNavigate();
  const [guess, setGuess] = useState('');
  const [mathQuestionBorder, setMathQuestionBorder] = useState(
    'border border-primary'
  );
  const [btnHover1, setBtnHover1] = useState(
    `btn btn-outline-dark ${bgColor} text-dark`
  );
  const [btnHover2, setBtnHover2] = useState(
    `btn btn-outline-dark ${bgColor} text-dark`
  );
  const [btnHover3, setBtnHover3] = useState(
    `btn btn-outline-dark ${bgColor} text-dark`
  );
  const [btnHover4, setBtnHover4] = useState(
    `btn btn-outline-dark ${bgColor} text-dark`
  );
  const [btnHover5, setBtnHover5] = useState(
    `btn btn-outline-dark ${bgColor} text-dark`
  );
  const [btnHover6, setBtnHover6] = useState(
    `btn btn-outline-dark ${bgColor} text-dark`
  );
  const [btnHover7, setBtnHover7] = useState(
    `btn btn-outline-dark ${bgColor} text-dark`
  );
  const [btnHover8, setBtnHover8] = useState(
    `btn btn-outline-dark ${bgColor} text-dark`
  );
  const [btnHover9, setBtnHover9] = useState(
    `btn btn-outline-dark ${bgColor} text-dark`
  );
  const [btnHover0, setBtnHover0] = useState(
    `btn btn-outline-dark ${bgColor} text-dark`
  );
  const [btnHoverB, setBtnHoverB] = useState(
    `btn btn-outline-dark ${bgColor} text-dark`
  );

  useEffect(() => {
    setBtnHoverB(`btn btn-outline-dark ${bgColor} text-dark`);
    setBtnHover1(`btn btn-outline-dark ${bgColor} text-dark`);
    setBtnHover2(`btn btn-outline-dark ${bgColor} text-dark`);
    setBtnHover3(`btn btn-outline-dark ${bgColor} text-dark`);
    setBtnHover4(`btn btn-outline-dark ${bgColor} text-dark`);
    setBtnHover5(`btn btn-outline-dark ${bgColor} text-dark`);
    setBtnHover6(`btn btn-outline-dark ${bgColor} text-dark`);
    setBtnHover7(`btn btn-outline-dark ${bgColor} text-dark`);
    setBtnHover8(`btn btn-outline-dark ${bgColor} text-dark`);
    setBtnHover9(`btn btn-outline-dark ${bgColor} text-dark`);
    setBtnHover0(`btn btn-outline-dark ${bgColor} text-dark`);
  }, [bgColor]);

  const updateButtonHover = (button) => {
    if (button === 'B') {
      setBtnHoverB(`btn btn-outline-dark bg-dark`);
      setTimeout(() => {
        setBtnHoverB(`btn btn-outline-dark ${bgColor} text-dark`);
      }, 175);
    } else if (button === '1') {
      setBtnHover1(`btn btn-outline-dark bg-dark`);
      setTimeout(() => {
        setBtnHover1(`btn btn-outline-dark ${bgColor} text-dark`);
      }, 175);
    } else if (button === '2') {
      setBtnHover2(`btn btn-outline-dark bg-dark`);
      setTimeout(() => {
        setBtnHover2(`btn btn-outline-dark ${bgColor} text-dark`);
      }, 175);
    } else if (button === '3') {
      setBtnHover3(`btn btn-outline-dark bg-dark`);
      setTimeout(() => {
        setBtnHover3(`btn btn-outline-dark ${bgColor} text-dark`);
      }, 175);
    } else if (button === '4') {
      setBtnHover4(`btn btn-outline-dark bg-dark`);
      setTimeout(() => {
        setBtnHover4(`btn btn-outline-dark ${bgColor} text-dark`);
      }, 175);
    } else if (button === '5') {
      setBtnHover5(`btn btn-outline-dark bg-dark`);
      setTimeout(() => {
        setBtnHover5(`btn btn-outline-dark ${bgColor} text-dark`);
      }, 175);
    } else if (button === '6') {
      setBtnHover6(`btn btn-outline-dark bg-dark`);
      setTimeout(() => {
        setBtnHover6(`btn btn-outline-dark ${bgColor} text-dark`);
      }, 175);
    } else if (button === '7') {
      setBtnHover7(`btn btn-outline-dark bg-dark`);
      setTimeout(() => {
        setBtnHover7(`btn btn-outline-dark ${bgColor} text-dark`);
      }, 175);
    } else if (button === '8') {
      setBtnHover8(`btn btn-outline-dark bg-dark`);
      setTimeout(() => {
        setBtnHover8(`btn btn-outline-dark ${bgColor} text-dark`);
      }, 175);
    } else if (button === '9') {
      setBtnHover9(`btn btn-outline-dark bg-dark`);
      setTimeout(() => {
        setBtnHover9(`btn btn-outline-dark ${bgColor} text-dark`);
      }, 175);
    } else if (button === '0') {
      setBtnHover0(`btn btn-outline-dark bg-dark`);
      setTimeout(() => {
        setBtnHover0(`btn btn-outline-dark ${bgColor} text-dark`);
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

      if (newGuessInt === finalResult) {
        setTimeout(() => {
          setMathQuestionBorder('border border-primary');
          updateCount();
          setGuess('');
        }, 500);
        setTimeout(() => {
          setMathQuestionBorder('border border-success border-5');
        }, 100);
      } else if (newGuessInt === parseInt(secretCode)) {
        setTimeout(() => {
          navigate(`/${secretCode}`);
        }, 10);
      }
    }
    updateButtonHover(userGuess);
  };

  return (
    <div className='container'>
      <div className={`row w-50 mx-auto my-2 ${mathQuestionBorder} rounded-3`}>
        <div className='ps-4 fs-3'>{firstNumber}</div>
        <div className='fs-3'>
          <span className='me-3'>{operation}</span>
          <span>{secondNumber}</span>
        </div>
      </div>
      <div className='row'>
        <div className='col-12 p-2 fs-3'>{!!guess ? guess : '_'}</div>
      </div>
      <div className='row border border-dark rounded-2'>
        <div className='col-12'>
          <div className='row'>
            <button
              onClick={() => handleGuess('1')}
              className={`${btnHover1} col-4 p-2 fs-3`}
            >
              {1}
            </button>
            <button
              onClick={() => handleGuess('2')}
              className={`${btnHover2} col-4 p-2 fs-3`}
            >
              {2}
            </button>
            <button
              onClick={() => handleGuess('3')}
              className={`${btnHover3} col-4 p-2 fs-3`}
            >
              {3}
            </button>
          </div>
          <div className='row'>
            <button
              onClick={() => handleGuess('4')}
              className={`${btnHover4} col-4 p-2 fs-3`}
            >
              {4}
            </button>
            <button
              onClick={() => handleGuess('5')}
              className={`${btnHover5} col-4 p-2 fs-3`}
            >
              {5}
            </button>
            <button
              onClick={() => handleGuess('6')}
              className={`${btnHover6} col-4 p-2 fs-3`}
            >
              {6}
            </button>
          </div>
          <div className='row'>
            <button
              onClick={() => handleGuess('7')}
              className={`${btnHover7} col-4 p-2 fs-3`}
            >
              {7}
            </button>
            <button
              onClick={() => handleGuess('8')}
              className={`${btnHover8} col-4 p-2 fs-3`}
            >
              {8}
            </button>
            <button
              onClick={() => handleGuess('9')}
              className={`${btnHover9} col-4 p-2 fs-3`}
            >
              {9}
            </button>
          </div>
          <div className='row'>
            <button
              onClick={() => handleGuess('0')}
              className={`${btnHover0} col-12 p-2 fs-3`}
            >
              {0}
            </button>
          </div>
          <div className='row'>
            <button
              onClick={() => handleGuess('B')}
              className={`${btnHoverB} col-12 p-2 fs-3`}
            >
              {'BACK'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NumberPad;

import { useState } from 'react';
import NumberPad from './NumberPad';
import { LEVEL_1, LEVEL_2 } from '../constants';

const TheGame = (props) => {
  const [correctMathQuestions, setCorrectMathQuestions] = useState(0);
  const level = props.level;
  const changeLevel = props.changeLevel;

  const level1MaxNumber = 20;
  const level2MaxNumber = 30;
  const level2MaxNumberMultiplication = 9;
  const level3MaxNumber = 40;
  const level3MaxNumberMultiplication = 13;
  const level1Operations = ['+', '-'];
  const level2Operations = ['+', '-', 'X'];
  const level3Operations = ['+', '-', 'X', '%'];

  let firstNumber = 0;
  let secondNumber = 0;
  let operation;
  let finalResult = 0;

  if (level === LEVEL_1) {
    operation =
      level1Operations[Math.floor(Math.random() * level1Operations.length)];
    if (operation === '+') {
      firstNumber = Math.floor(Math.random() * level1MaxNumber) + 1;
      secondNumber = Math.floor(Math.random() * level1MaxNumber) + 1;
      finalResult = firstNumber + secondNumber;
    } else {
      firstNumber = Math.floor(Math.random() * level1MaxNumber) + 1;
      secondNumber = Math.floor(Math.random() * level1MaxNumber) + 1;
      if (firstNumber < secondNumber) {
        const holder = firstNumber;
        firstNumber = secondNumber;
        secondNumber = holder;
      }
      finalResult = firstNumber - secondNumber;
    }
  } else if (level === LEVEL_2) {
    operation =
      level2Operations[Math.floor(Math.random() * level2Operations.length)];
    if (operation === '+') {
      firstNumber = Math.floor(Math.random() * level2MaxNumber) + 1;
      secondNumber = Math.floor(Math.random() * level2MaxNumber) + 1;
      finalResult = firstNumber + secondNumber;
    } else if (operation === '-') {
      firstNumber = Math.floor(Math.random() * level2MaxNumber) + 1;
      secondNumber = Math.floor(Math.random() * level2MaxNumber) + 1;
      if (firstNumber < secondNumber) {
        const holder = firstNumber;
        firstNumber = secondNumber;
        secondNumber = holder;
      }
      finalResult = firstNumber - secondNumber;
    } else {
      firstNumber =
        Math.floor(Math.random() * level2MaxNumberMultiplication) + 1;
      secondNumber =
        Math.floor(Math.random() * level2MaxNumberMultiplication) + 1;
      finalResult = firstNumber * secondNumber;
    }
  } else {
    operation =
      level3Operations[Math.floor(Math.random() * level3Operations.length)];
    if (operation === '+') {
      firstNumber = Math.floor(Math.random() * level3MaxNumber) + 1;
      secondNumber = Math.floor(Math.random() * level3MaxNumber) + 1;
      finalResult = firstNumber + secondNumber;
    } else if (operation === '-') {
      firstNumber = Math.floor(Math.random() * level3MaxNumber) + 1;
      secondNumber = Math.floor(Math.random() * level3MaxNumber) + 1;
      if (firstNumber < secondNumber) {
        const holder = firstNumber;
        firstNumber = secondNumber;
        secondNumber = holder;
      }
      finalResult = firstNumber - secondNumber;
    } else if (operation === 'X') {
      firstNumber =
        Math.floor(Math.random() * level3MaxNumberMultiplication) + 1;
      secondNumber =
        Math.floor(Math.random() * level3MaxNumberMultiplication) + 1;
      finalResult = firstNumber * secondNumber;
    } else {
      while (firstNumber % secondNumber !== 0) {
        firstNumber = Math.floor(Math.random() * level3MaxNumber) + 1;
        secondNumber = Math.floor(Math.random() * level3MaxNumber) + 1;
      }
      finalResult = firstNumber / secondNumber;
    }
  }

  const handleMathQuestions = () => {
    if (correctMathQuestions === 4) {
      changeLevel();
      setCorrectMathQuestions(0);
    } else {
      setCorrectMathQuestions((current) => current + 1);
    }
  };

  return (
    <div className='container text-center regularText'>
      <div className='row'>
        <div className='col-12 fs-3'>
          {correctMathQuestions}
          {'   Correct'}
        </div>
      </div>
      <div className='container'>
        <div className='row'>
          <NumberPad
            data={[
              handleMathQuestions,
              finalResult,
              firstNumber,
              operation,
              secondNumber,
            ]}
          />
        </div>
      </div>
    </div>
  );
};

export default TheGame;

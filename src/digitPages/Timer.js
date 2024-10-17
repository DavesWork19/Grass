import { useState, useEffect } from 'react';
import { STOP_GAME } from '../constants';
import '../Fonts.css';

const Timer = (props) => {
  const [timer, setTimer] = useState(0);
  const updateTimer = props.updateTimer;
  const handleTimerUpdate = props.handleTimerUpdate;

  useEffect(() => {
    setInterval(() => {
      setTimer((oldTime) => oldTime + 1);
    }, 1000);
  }, []);

  if (updateTimer === STOP_GAME) {
    handleTimerUpdate(timer);
  }

  return (
    <div>
      <div
        className='progress bg-dark'
        style={{ height: '50px' }}
        role='progressbar'
        aria-label='Info striped example'
        aria-valuenow='50'
        aria-valuemin='0'
        aria-valuemax='100'
      >
        <div
          className='progress-bar progress-bar-striped bg-info fs-3 text-dark regularText'
          style={{ width: `${timer}%` }}
        >
          {timer}
        </div>
      </div>
    </div>
  );
};

export default Timer;

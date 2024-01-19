import TheGame from './TheGame';
import Header from './Header';
import Timer from './Timer';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  LEVEL_1_TIMER,
  LEVEL_1,
  LEVEL_2,
  LEVEL_3,
  STOP_GAME,
} from '../constants';
import '../Fonts.css';

const GameContainer = () => {
  const navigate = useNavigate();
  const [countingDown, setCountingDown] = useState(true);
  const [countDownTimer, setCountDownTimer] = useState(LEVEL_1_TIMER);
  const [updateTimer, setUpdateTimer] = useState('');
  const [currentLevel, setCurrentLevel] = useState({
    level: 1,
    color: 'bg-success-subtle',
  });

  useEffect(() => {
    let timesRun = LEVEL_1_TIMER;
    const timerInterval = setInterval(() => {
      timesRun = timesRun - 1;
      if (timesRun === 0) {
        clearInterval(timerInterval);
        setCountingDown(false);
      } else {
        setCountDownTimer((oldTime) => oldTime - 1);
      }
    }, 1000);
  }, []);

  const handleTimerUpdate = (time) => {
    setTimeout(() => {
      navigate('/', { state: { time: time } });
    }, 10);
  };

  const handleChangeLevel = () => {
    if (currentLevel.level === LEVEL_1) {
      setCurrentLevel({ level: 2, color: 'bg-primary-subtle' });
    } else if (currentLevel.level === LEVEL_2) {
      setCurrentLevel({ level: 3, color: 'bg-danger-subtle' });
    } else if (currentLevel.level === LEVEL_3) {
      setUpdateTimer(STOP_GAME);
    }
  };

  return countingDown ? (
    <div className='vw-100'>
      <Header level={1} />
      <main className='text-center bg-success-subtle regularText vh-100 fs-1 pt-5'>
        {countDownTimer}
      </main>
    </div>
  ) : (
    <div className='vw-100'>
      <Header level={currentLevel.level} />
      <main className={`text-center ${currentLevel.color} pb-5 vh-100`}>
        <Timer
          updateTimer={updateTimer}
          handleTimerUpdate={handleTimerUpdate}
        />
        <TheGame level={currentLevel.level} changeLevel={handleChangeLevel} />
      </main>
    </div>
  );
};

export default GameContainer;

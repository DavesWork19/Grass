import { useNavigate } from 'react-router-dom';
import { LEVEL_1, LEVEL_2 } from '../constants';
import HomeIcon from '../HomeIcon';
import '../Fonts.css';

const Header = (props) => {
  const navigate = useNavigate();
  const currentLevel = props.level;
  let homeButtonColor = '';

  if (currentLevel === LEVEL_1) {
    homeButtonColor = 'bg-success-subtle';
  } else if (currentLevel === LEVEL_2) {
    homeButtonColor = 'bg-primary-subtle';
  } else {
    homeButtonColor = 'bg-danger-subtle';
  }

  const handleHomeClick = (navigation) => {
    navigate(navigation);
  };

  return (
    <div className={`container-fluid text-center ${homeButtonColor}`}>
      <div className={'row pb-4 pt-3 border-bottom border-dark'}>
        <h1 className='col-8 fs-3 my-auto regularText'>{'The Numbers Game'}</h1>
        <div
          className={`col-4 ${homeButtonColor}`}
          onClick={() => handleHomeClick('/')}
        >
          <HomeIcon />
        </div>
      </div>
      <div className={'row'}>
        <div className='col-12 fs-2 regularText'>{`Level ${currentLevel}`}</div>
      </div>
    </div>
  );
};

export default Header;

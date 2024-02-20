import { useNavigate } from 'react-router-dom';
import HomeIcon from '../HomeIcon';
import '../Fonts.css';
import { secretCode, sportNumbersGameHeading } from '../constants';

const NFLHeader = (props) => {
  const navigate = useNavigate();

  const handleHomeClick = (navigation) => {
    navigate(navigation);
  };

  return (
    <div className={'container-fluid text-center '}>
      <div className={'row pb-4 pt-3 border-bottom border-dark'}>
        <h1 className='col-9 fs-5 my-auto regularText'>
          {sportNumbersGameHeading}
        </h1>
        <div
          className={'col-3'}
          onClick={() => handleHomeClick(`/${secretCode}`)}
        >
          <HomeIcon color='slategray' />
        </div>
      </div>
      <div className={'row'}>
        <div className='col-12 fs-2 regularText'>{`Week ${props.week}`}</div>
      </div>
    </div>
  );
};

export default NFLHeader;

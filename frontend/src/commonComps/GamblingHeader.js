import { useNavigate } from 'react-router-dom';
import HomeIcon from '../HomeIcon';
import '../Fonts.css';
import { secretCode, sportNumbersGameHeading } from '../constants';

const GamblingHeader = (props) => {
  const navigate = useNavigate();

  const title = props.title;
  const subTitle = props.subTitle;

  const handleHomeClick = (event) => {
    event.preventDefault();
    if (props.link === 'back') {
      navigate(-1);
    } else if (props.link === 'home') {
      navigate(`/`);
    } else if (props.link === 'Football') {
      navigate(`/${secretCode}/Football`);
    } else if (props.link === 'Basketball') {
      navigate(`/${secretCode}/Basketball`);
    } else if (props.link === 'gamblingHomePage') {
      navigate(`/${secretCode}`);
    }
  };

  return (
    <div className={'container-fluid text-center pb-5'}>
      <div className={'row pb-4 pt-3 border-bottom border-dark'}>
        <h1 className='col-9 fs-5 my-auto'>{sportNumbersGameHeading}</h1>
        <div className={'col-3'} onClick={handleHomeClick}>
          <HomeIcon color='slategray' />
        </div>
      </div>
      <div className={'row py-3'}>
        <div className='col-12 fs-2'>{title}</div>
        <div className='col-12 fs-3'>{subTitle}</div>
      </div>
    </div>
  );
};

export default GamblingHeader;

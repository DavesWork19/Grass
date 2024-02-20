import { useNavigate } from 'react-router-dom';
import HomeIcon from '../HomeIcon';
import '../Fonts.css';
import { secretCode, sportNumbersGameHeading } from '../constants';

const NBAHeader = (props) => {
  const navigate = useNavigate();

  const title = props.title;

  const handleHomeClick = (event) => {
    event.preventDefault();
    if (props.link === 'gamePage') {
      navigate(-1);
    } else {
      const navLink =
        props.link === 'home' ? `/${secretCode}` : `/${secretCode}/Basketball`;
      navigate(navLink);
    }
  };

  return (
    <div className={'container-fluid text-center regularText'}>
      <div className={'row pb-4 pt-3 border-bottom border-dark'}>
        <h1 className='col-9 fs-5 my-auto'>{sportNumbersGameHeading}</h1>
        <div className={'col-3'} onClick={handleHomeClick}>
          <HomeIcon color='slategray' />
        </div>
      </div>
      <div className={'row py-3'}>
        <div className='col-12 fs-2'>{title}</div>
      </div>
    </div>
  );
};

export default NBAHeader;

import { useNavigate } from 'react-router-dom';
import HomeIcon from '../HomeIcon';
import '../Fonts.css';

const NBAHeader = (props) => {
  const navigate = useNavigate();

  const handleHomeClick = (navigation) => {
    navigate(navigation);
  };

  return (
    <div className={'container-fluid text-center '}>
      <div className={'row pb-4 pt-3 border-bottom border-dark'}>
        <h1 className='col-9 fs-5 my-auto regularText'>
          {'The Numbers Game???'}
        </h1>
        <div className={'col-3'} onClick={() => handleHomeClick('/2332220')}>
          <HomeIcon color='slategray' />
        </div>
      </div>
      <div className={'row'}>
        <div className='col-12 fs-2 regularText'>{props.date}</div>
      </div>
    </div>
  );
};

export default NBAHeader;

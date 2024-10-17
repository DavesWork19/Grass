import '../Fonts.css';

const TeamInfo = (props) => {
  let { title, percent } = props.info;
  let showPercent = true;

  if (percent === -1) {
    percent = 'NA';
    showPercent = false;
  }

  return (
    <div className='row mt-3 teamStats pb-3'>
      <div className='col-8'>{title}</div>
      <div className='col-2 ps-0'>
        {percent}
        {showPercent && <span>{'%'}</span>}
      </div>
    </div>
  );
};

export default TeamInfo;

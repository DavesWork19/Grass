const TeamInfo = (props) => {
  const { title, percent } = props.info;

  return (
    <div className='row my-3 '>
      <div className='col-7'>{title}</div>
      <div className='col-2'>
        {percent}
        <span className='timeText'>{'%'}</span>
      </div>
    </div>
  );
};

export default TeamInfo;

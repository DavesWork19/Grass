import '../Fonts.css';

const PercentDataTableGameDayRow = (props) => {
  const { title, spread, overUnder, parlay, checksAndXs } = props.data;

  const borderTopAdj = title[0] === '1' && 'rounded-top';
  const borderBottomAdj = title[0] === '5' && 'rounded-bottom';

  const correctWrongLogo = (value, category) => {
    if (checksAndXs) {
      const spreadCSS = 'fs-3 me-3 pe-3';
      const overUnderCSS = 'fs-3 me-3';
      const parlayCSS = 'fs-3 ms-2';

      let cssAdj;
      if (category === 'spread') {
        cssAdj = spreadCSS;
      } else if (category === 'overUnder') {
        cssAdj = overUnderCSS;
      } else if (category === 'parlay') {
        cssAdj = parlayCSS;
      }

      if (value === '100.00%') {
        return <div className={cssAdj}>☑</div>;
      } else {
        return <div className={cssAdj}>☐</div>;
      }
    } else {
    }
    const spreadCSS = 'text-start ms-2 text-sm-center ms-sm-0';
    const overUnderCSS = 'me-2';
    const parlayCSS = 'text-end text-sm-center';

    let cssAdj;
    if (category === 'spread') {
      cssAdj = spreadCSS;
    } else if (category === 'overUnder') {
      cssAdj = overUnderCSS;
    } else if (category === 'parlay') {
      cssAdj = parlayCSS;
    }

    return <div className={cssAdj}>{value}</div>;
  };

  const spreadAdj = correctWrongLogo(spread, 'spread');
  const overUnderAdj = correctWrongLogo(overUnder, 'overUnder');
  const parlayAdj = correctWrongLogo(parlay, 'parlay');

  return (
    <div
      className={`row bg-black py-1 border-bottom border-dark ${borderTopAdj} ${borderBottomAdj}`}
    >
      <div className='col-4 tableHeaderNormalWeight text-start text-sm-center ps-1 pt-1 pt-sm-0 pe-0'>
        {title}
      </div>
      <div className='col-3 p-0'>{spreadAdj}</div>
      <div className='col-2 p-0'>{overUnderAdj}</div>
      <div className='col-3'>{parlayAdj}</div>
    </div>
  );
};

export default PercentDataTableGameDayRow;

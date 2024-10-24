import '../Fonts.css';

const ParlayHitsTable = (props) => {
  const parlayTitle = props.title;
  const parlayID = parlayTitle.split(' ').join('_');
  const parlayPercentages = props.parlay;

  return (
    <div className='accordion bg-black pt-5' id={`${parlayID}Accordion`}>
      <div className='accordion-item border-black'>
        <h2 className='accordion-header'>
          <button
            className='accordion-button collapsed slateGrayBackground boldText text-black'
            type='button'
            data-bs-toggle='collapse'
            data-bs-target={`#${parlayID}`}
            aria-expanded='false'
            aria-controls={parlayID}
          >
            {parlayTitle}
          </button>
        </h2>
        <div
          id={parlayID}
          className='accordion-collapse collapse bg-black'
          data-bs-parent={`#${parlayID}Accordion`}
        >
          <div className='accordion-body p-0 lightText'>
            <div className='container bg-dark p-3 pt-0'>
              <div className='row'>
                <div className='col-12 p-3'></div>
              </div>
              <div className='row bg-black rounded py-1'>
                <div className='col-4 tableHeaderNormalWeight'>
                  {'Category'}
                </div>
                <div className='col-4 tableHeaderNormalWeight'>{'Legs'}</div>
                <div className='col-4 tableHeaderNormalWeight'>{'Date'}</div>
              </div>
              <div className='row'>
                <div className='col-12 p-3'></div>
              </div>
              {parlayPercentages.map((data) => {
                const [category, date, totalCalls] = data.split(',').slice(1);

                const updatedCategory =
                  category === 'Overall' ? 'All' : category;

                return (
                  <div
                    className='row bg-black py-1 border-bottom border-dark rounded'
                    key={data}
                  >
                    <div className='col-4 text-start'>{updatedCategory}</div>
                    <div className='col-4'>{totalCalls}</div>
                    <div className='col-4'>
                      {date.slice(0, date.length - 5)}
                    </div>
                  </div>
                );
              })}

              <div className='row'>
                <div className='col-12 p-3'></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ParlayHitsTable;

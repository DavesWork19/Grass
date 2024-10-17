import '../Fonts.css';
import PercentOverallDataTable from './PercentOverallDataTable';

const OverallPercents = () => {
  return (
    <div className='accordion bg-black' id='overallAccordion'>
      <div className='accordion-item border-black'>
        <h2 className='accordion-header'>
          <button
            className='accordion-button collapsed slateGrayBackground boldText text-black'
            type='button'
            data-bs-toggle='collapse'
            data-bs-target='#overallStats'
            aria-expanded='false'
            aria-controls='overallStats'
          >
            {'Overall Stats'}
          </button>
        </h2>
        <div
          id='overallStats'
          className='accordion-collapse collapse bg-black'
          data-bs-parent='#overallAccordion'
        >
          <div className='accordion-body p-0 lightText'>
            <PercentOverallDataTable />
          </div>
        </div>
      </div>
    </div>
  );
};

export default OverallPercents;

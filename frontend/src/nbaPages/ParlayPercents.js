import '../Fonts.css';

const ParlayPercents = (props) => {
  const parlayPercentages = props.parlay;

  return (
    <table className='table table-dark '>
      <thead className='thead-dark'>
        <tr>
          <th scope='col'>Category</th>
          <th scope='col'>Date</th>
          <th scope='col'>Legs</th>
        </tr>
      </thead>
      <tbody>
        {parlayPercentages.map((data) => {
          const [parlay, category, date, totalCalls] = data.split(',');

          return (
            <tr key={data}>
              <td>{category}</td>
              <td>{date.slice(0, date.length - 5)}</td>
              <td>{totalCalls}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default ParlayPercents;

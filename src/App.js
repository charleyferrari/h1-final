import React from 'react';
import Plot from 'react-plotly.js';

const data = [{ x: 1, y: 2 }, { x: 2, y: 1 }, { x: 3, y: 2 }];

class App extends React.Component {
  // componentDidUpdate() {
  //   this.MyPlot();
  // }
  //
  // componentDidMount() {
  //   fetch(URL).then(response => {
  //     this.setState({
  //       data: response.json()
  //     });
  //   });
  //   this.MyPlot();
  // }

  render() {
    return <MyPlot data={data} />;
  }
}

// eslint-disable-next-line
const URL = 'http://localhost:5000/api/lending_api';

function MyPlot({ data }) {
  return (
    <Plot
      data={[
        {
          x: data.map(i => i.x),
          y: data.map(i => i.y),
          type: 'scatter',
          mode: 'lines+points'
        }
      ]}
    />
  );
}

export default App;

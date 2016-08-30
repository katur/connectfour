import React from 'react';
import { connect } from 'react-redux';

import GameSquare from './GameSquare';


function mapStateToProps(state) {
  return {
    numRows: state.numRows,
    numColumns: state.numColumns,
    grid: state.grid,
    blinkingSquares: state.blinkingSquares,
  }
}


let GameGrid = React.createClass({
  propTypes: {
    numRows: React.PropTypes.number.isRequired,
    numColumns: React.PropTypes.number.isRequired,
    grid: React.PropTypes.arrayOf(React.PropTypes.array).isRequired,
    blinkingSquares: React.PropTypes.array.isRequired,
  },

  render: function() {
    const percentage = 80.0 / Math.max(this.props.numRows,
                                       this.props.numColumns);
    const size = `${percentage}vmin`;

    const rows = [];

    for (let i = 0; i < this.props.numRows; i++) {
      let row = [];

      for (let j = 0; j < this.props.numColumns; j++) {
        const clear = (j === 0) ? 'left' : 'none';

        // TODO: restructure blinking to not require this iteration (set?)
        let blinking = false;

        for (let b of this.props.blinkingSquares) {
          if (b[0] == i && b[1] == j) {
            blinking = true;
            break;
          }
        }

        row.push(
          <GameSquare
            key={`${i}-${j}`}
            color={this.props.grid[i][j]}
            blinking={blinking}
            style={{
              width: size,
              height: size,
              clear: clear,
            }}
          />
        );
      }

      rows.push(row);
    }

    return (
      <div id='game-grid'>
        {rows}
      </div>
    );
  },
});


GameGrid = connect(
  mapStateToProps
)(GameGrid);


export default GameGrid;

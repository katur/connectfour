import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import GameSquare from './GameSquare';


function mapStateToProps({ numRows, numColumns, grid, blinkingSquares }) {
  return {
    numRows,
    numColumns,
    grid,
    blinkingSquares,
  };
}


const propTypes = {
  numRows: PropTypes.number.isRequired,
  numColumns: PropTypes.number.isRequired,
  grid: PropTypes.arrayOf(PropTypes.array).isRequired,
  blinkingSquares: PropTypes.array.isRequired,
};


function GameGrid({ numRows, numColumns, grid, blinkingSquares }) {
  const percentage = 80.0 / Math.max(numRows, numColumns);
  const size = `${percentage}vmin`;
  const rows = [];

  for (let i = 0; i < numRows; i++) {
    let row = [];

    for (let j = 0; j < numColumns; j++) {
      let clear = (j === 0) ? 'left' : 'none';

      // TODO: restructure blinking to not require this iteration (set?)
      let blinking = false;

      for (let b of blinkingSquares) {
        if (b[0] == i && b[1] == j) {
          blinking = true;
          break;
        }
      }

      row.push(
        <GameSquare
          key={`${i}-${j}`}
          color={grid[i][j]}
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
    <div id="game-grid">
      {rows}
    </div>
  );
}


GameGrid.propTypes = propTypes;

export default connect(mapStateToProps)(GameGrid);

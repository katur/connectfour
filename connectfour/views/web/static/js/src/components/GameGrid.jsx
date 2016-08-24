import React from "react";
import { connect } from "react-redux";
import GameSquare from "./GameSquare";


function mapStateToProps(state) {
  return {
    grid: state.grid,
    blinkingSquares: state.blinkingSquares,
    numRows: state.numRows,
    numColumns: state.numColumns,
  }
}


let GameGrid = React.createClass({
  render: function() {
    const percentage = 90.0 / Math.max(this.props.numRows,
                                       this.props.numColumns);
    const size = percentage + "vmin";

    let rows = [];

    for (let i = 0; i < this.props.numRows; i++) {
      let row = [];

      for (let j = 0; j < this.props.numColumns; j++) {
        const clear = (j === 0) ? "left" : "none";
        let blinking = false;

        for (var item of this.props.blinkingSquares) {
          if (item[0] == i && item[1] == j) {
            blinking = true;
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
      <div id="game-grid">
        {rows}
      </div>
    );
  },
});


GameGrid = connect(
  mapStateToProps
)(GameGrid);


export default GameGrid;

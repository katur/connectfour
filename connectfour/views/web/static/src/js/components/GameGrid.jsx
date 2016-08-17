import React from "react";
import { connect } from "react-redux";
import GameSquare from "./GameSquare";


function mapStateToProps(state) {
  return {
    grid: state.grid,
    numRows: state.numRows,
    numColumns: state.numColumns,
  }
}


let GameGrid = React.createClass({
  render: function() {
    const percentage = 80.0 / Math.max(this.props.numRows,
                                       this.props.numColumns);
    const styleRoot = "width:" + percentage + "vmin; " +
                      "height:" + percentage + "vmin; ";

    const grid = this.props.grid;

    let rows = [];

    grid.forEach(function(row, i) {
      let currentRow = [];
      row.forEach(function(column, j) {
        let clear = (j === 0) ? "left" : "none";

        currentRow.push(
          <GameSquare
            key={`${i}-${j}`}
            color={grid[i][j]}
            style={{
              width: percentage + "vmin",
              height: percentage + "vmin",
              clear: clear,
            }}
          />
        );
      });
      rows.push(currentRow);
    });

    return (
      <div id="game-grid">{rows}</div>
    );
  },
});


GameGrid = connect(
  mapStateToProps
)(GameGrid);


export default GameGrid;

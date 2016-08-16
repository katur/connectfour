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

    return (
      <div id="game-grid">
        {this.props.grid.map(function(row, i) {
          return
            {row.map(function(column, j) {
              let styleExtra = (j === 0) ? "clear: left; " : "";

              return (
                <GameSquare
                  key={`${i}-${j}`}
                  color={this.props.board[row][column]}
                  style={`${styleRoot} ${styleExtra}`}
                />
              );
            })}
          ;
        })}
      </div>
    );
  },
});


GameGrid = connect(
  mapStateToProps
)(GameGrid);


export default GameGrid;

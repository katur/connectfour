import React from "react";
import { connect } from "react-redux";
import GameSquare from "./GameSquare";


function mapStateToProps(state) {
  return {
    numRows: state.numRows,
    numColumns: state.numColumns,
  }
}


let GameGrid = React.createClass({
  propTypes: {
    numRows: React.PropTypes.number.isRequired,
    numColumns: React.PropTypes.number.isRequired,
  },

  render: function() {
    const percentage = 90.0 / Math.max(this.props.numRows,
                                       this.props.numColumns);
    const size = percentage + "vmin";

    let rows = [];

    for (let i = 0; i < this.props.numRows; i++) {
      let row = [];

      for (let j = 0; j < this.props.numColumns; j++) {
        const clear = (j === 0) ? "left" : "none";

        row.push(
          <GameSquare
            key={`${i}-${j}`}
            row={i}
            col={j}
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
)(GameGrid)


export default GameGrid;

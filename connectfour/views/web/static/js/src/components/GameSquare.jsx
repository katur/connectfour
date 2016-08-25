import React from "react";
import { connect } from "react-redux";


function mapStateToProps(state) {
  return {
    grid: state.grid,
    blinkingSquares: state.blinkingSquares,
  }
}


let GameSquare = React.createClass({
  propTypes: {
    grid: React.PropTypes.arrayOf(React.PropTypes.array).isRequired,
    blinkingSquares: React.PropTypes.array.isRequired,
  },

  render: function() {
    const color = this.props.grid[this.props.row][this.props.col]
    let innerClassName = `game-square color-${color}`;

    // TODO: restructure blinking to not require this iteration
    // (instead index into 2D blink array)
    for (let b of this.props.blinkingSquares) {
      if (b[0] == this.props.row && b[1] == this.props.col) {
        innerClassName += " blinking";
        break;
      }
    }

    return (
      <div
        className="game-square-wrapper"
        style={this.props.style}
      >
        <div
          className={innerClassName}
        >
        </div>
      </div>
    );
  },
});


GameSquare = connect(
  mapStateToProps
)(GameSquare)


export default GameSquare;

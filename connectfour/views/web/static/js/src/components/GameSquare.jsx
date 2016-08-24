import React from "react";
import { connect } from "react-redux";


let GameSquare = React.createClass({
  render: function() {
    let innerClassName = `game-square color-${this.props.color}`;

    if (this.props.blinking) {
      innerClassName += " blinking";
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


export default GameSquare;

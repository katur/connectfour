import React from "react";
import { connect } from "react-redux";


let GameSquare = React.createClass({
  render: function() {
    return (
      <div
        className="game-square-wrapper"
        style={this.props.style}
      >
        <div
          className={`game-square color-${this.props.color}`}
        >
        </div>
      </div>
    );
  },
});


export default GameSquare;

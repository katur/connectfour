import React from "react";
import { connect } from "react-redux";


let GameSquare = React.createClass({
  render: function() {
    return (
      <div
        className={`game-square game-square-${this.props.color}`}
        style={this.props.style}
      >
      </div>
    );
  },
});


export default GameSquare;

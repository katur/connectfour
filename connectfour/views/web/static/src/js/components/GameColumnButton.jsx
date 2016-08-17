import React from "react";
import { connect } from "react-redux";


let GameColumnButton = React.createClass({
  render: function() {
    return (
      <button
        className="game-column-button"
        style={this.props.style}
      >
        Play here
      </button>
    );
  },
});


export default GameColumnButton;

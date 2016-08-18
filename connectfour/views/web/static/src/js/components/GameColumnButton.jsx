import React from "react";
import Emitters from "../emitters";


const GameColumnButton = React.createClass({
  _handleSubmit: function(e) {
    e.preventDefault();
    Emitters.play({
      column: this.props.column,
    });
  },

  render: function() {
    return (
      <form
        action=""
        method="post"
        onSubmit={this._handleSubmit}
      >
        <button
          className="game-column-button"
          style={this.props.style}
          disabled={this.props.disabled}
        >
          Play here
        </button>
      </form>
    );
  },
});


export default GameColumnButton;

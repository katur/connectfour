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
        <div
          className="game-column-button-wrapper"
          style={this.props.style}
        >
          <button
            className="game-column-button"
            disabled={this.props.disabled}
          >
            Play here
          </button>
        </div>
      </form>
    );
  },
});


export default GameColumnButton;

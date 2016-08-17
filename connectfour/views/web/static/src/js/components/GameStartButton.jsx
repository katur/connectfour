import React from "react";
import Emitters from "../emitters";


const GameStartButton = React.createClass({
  _handleSubmit: function(e) {
    e.preventDefault();
    Emitters.startGame();
  },

  render: function() {
    return (
      <form
        id="game-start"
        action=""
        method="post"
        onSubmit={this._handleSubmit}
      >
        <button type="submit">
          Start Game
        </button>
      </form>
    );
  },
});


export default GameStartButton;

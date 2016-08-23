import React from "react";
import GameInfo from "./GameInfo";
import GamePlayers from "./GamePlayers";
import GameStartButton from "./GameStartButton";
import GameFeedback from "./GameFeedback";


let GameControl = React.createClass({
  render: function() {
    return (
      <div id="game-control">
        <GameInfo />
        <GamePlayers />
        <GameFeedback />
        <GameStartButton />
      </div>
    );
  },
});


export default GameControl;

import React from "react";
import GameStartButton from "./GameStartButton";
import GamePlayers from "./GamePlayers";
import ChangeBoardForm from "./ChangeBoardForm";


let GameControl = React.createClass({
  render: function() {
    return (
      <div id="game-control">
        <GameStartButton />
        <GamePlayers />
        <ChangeBoardForm />
      </div>
    );
  },
});


export default GameControl;

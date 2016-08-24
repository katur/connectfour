import React from "react";
import GameNumber from "./GameNumber";
import GamePlayers from "./GamePlayers";
import GameStartButton from "./GameStartButton";
import ChangeBoardForm from "./ChangeBoardForm";


let GameControl = React.createClass({
  render: function() {
    return (
      <div id="game-control">
        <GameStartButton />
        <GameNumber />
        <GamePlayers />
        <ChangeBoardForm />
      </div>
    );
  },
});


export default GameControl;

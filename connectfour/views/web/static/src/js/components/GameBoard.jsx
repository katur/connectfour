import React from "react";
import { connect } from "react-redux";
import GameColumnButtons from "./GameColumnButtons";
import GameGrid from "./GameGrid";


let GameBoard = React.createClass({
  render: function() {
    return (
      <div id="game-board" className="section">
        <GameColumnButtons />
        <GameGrid />
      </div>
    );
  },
});


export default GameBoard;

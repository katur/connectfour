import React from "react";
import { connect } from "react-redux";
import GameGrid from "./GameGrid";


let GameBoard = React.createClass({
  render: function() {
    return (
      <GameGrid />
    );
  },
});


export default GameBoard;

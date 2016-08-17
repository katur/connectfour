import React from "react";
import { connect } from "react-redux";
import GameTitle from "./GameTitle";
import GamePlayers from "./GamePlayers";
import GameStartButton from "./GameStartButton";
import GameFeedback from "./GameFeedback";
import GameBoard from "./GameBoard";


function mapStateToProps(state) {
  return {
    show: state.username ? true : false,
  }
}


let GameScreen = React.createClass({
  render: function() {
    if (!this.props.show) {
      return null;
    }

    return (
      <div id="game-screen">
        <GameTitle />
        <GamePlayers />
        <GameStartButton />
        <GameFeedback />
        <GameBoard />
      </div>
    );
  },
});


GameScreen = connect(
  mapStateToProps
)(GameScreen);


export default GameScreen;

import React from "react";
import { connect } from "react-redux";
import GameTitle from "./GameTitle";
import GameRoomInfo from "./GameRoomInfo";
import GameFeedback from "./GameFeedback";
import GameControl from "./GameControl";
import GameBoard from "./GameBoard";


function mapStateToProps(state) {
  return {
    show: state.room ? true : false,
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
        <GameRoomInfo />
        <GameFeedback />
        <GameBoard />
        <GameControl />
      </div>
    );
  },
});


GameScreen = connect(
  mapStateToProps
)(GameScreen);


export default GameScreen;

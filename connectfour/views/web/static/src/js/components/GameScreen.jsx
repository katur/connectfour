import React from "react";
import FeedbackBarWrapper from "../containers/FeedbackBarWrapper";
import PlayerListWrapper from "../containers/PlayerListWrapper";


const GameScreen = React.createClass({
  render: function() {
    if (!this.props.show) {
      return null;
    }

    return (
      <div id="game-screen">
        <FeedbackBarWrapper />
        <PlayerListWrapper />
      </div>
    );
  },
});


export default GameScreen;

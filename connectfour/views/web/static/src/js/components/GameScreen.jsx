import React from "react";
import { connect } from "react-redux";
import FeedbackBar from "./FeedbackBar";
import PlayerList from "./PlayerList";


function mapStateToProps(state) {
  return {
    show: state.username ? true : false,
  }
}


var GameScreen = React.createClass({
  render: function() {
    if (!this.props.show) {
      return null;
    }

    return (
      <div id="game-screen">
        <FeedbackBar />
        <PlayerList />
      </div>
    );
  },
});


GameScreen = connect(
  mapStateToProps
)(GameScreen);


export default GameScreen;

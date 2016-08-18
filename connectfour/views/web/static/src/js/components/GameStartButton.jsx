import React from "react";
import { connect } from "react-redux";
import Emitters from "../emitters";


function mapStateToProps(state) {
  return {
    gameInProgress: state.gameInProgress,
  }
}


let GameStartButton = React.createClass({
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
        <button
          type="submit"
          disabled={this.props.gameInProgress}
        >
          Start Game
        </button>
      </form>
    );
  },
});


GameStartButton = connect(
  mapStateToProps
)(GameStartButton);


export default GameStartButton;

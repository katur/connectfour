import React from "react";
import { connect } from 'react-redux'


function mapStateToProps(state) {
  return {
    username: state.username,
    room: state.room,
    numToWin: state.numToWin,
    gameNumber: state.gameNumber,
  }
}


let GameTitle = React.createClass({
  render: function() {
    let gameNumberFeedback = ``;

    if (this.props.gameNumber) {
      gameNumberFeedback = `| Game ${this.props.gameNumber}`
    }

    return (
      <div>
        <h1>
          Connect {this.props.numToWin}
        </h1>

        <h3>
          Welcome, {this.props.username}
          | Room {this.props.room}
          {gameNumberFeedback}
        </h3>
      </div>
    );
  },
});


GameTitle = connect(
  mapStateToProps
)(GameTitle);


export default GameTitle;

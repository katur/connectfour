import React from "react";
import { connect } from 'react-redux'


function mapStateToProps(state) {
  return {
    username: state.username,
    room: state.room,
    gameNumber: state.gameNumber,
  }
}


let GameInfo = React.createClass({
  render: function() {
    return (
      <div id="game-info">
        <span>Your user: {this.props.username}</span>
        <span>Room: {this.props.room}</span>
        <span>Game: {this.props.gameNumber}</span>
      </div>
    );
  },
});


GameInfo = connect(
  mapStateToProps
)(GameInfo);


export default GameInfo;

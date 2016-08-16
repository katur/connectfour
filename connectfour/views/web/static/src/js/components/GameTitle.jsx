import React from "react";
import { connect } from 'react-redux'


function mapStateToProps(state) {
  return {
    numToWin: state.numToWin,
    room: state.room,
  }
}


let GameTitle = React.createClass({
  render: function() {
    return (
      <h1 id="game-title">
        Connect {this.props.numToWin} | Room {this.props.room}
      </h1>
    );
  },
});


GameTitle = connect(
  mapStateToProps
)(GameTitle);


export default GameTitle;

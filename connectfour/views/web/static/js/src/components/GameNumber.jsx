import React from "react";
import { connect } from "react-redux";


function mapStateToProps(state) {
  return {
    gameNumber: state.gameNumber,
  }
}


let GameNumber = React.createClass({
  render: function() {
    return (
      <span id="game-number">Game {this.props.gameNumber}</span>
    );
  },
});


GameNumber = connect(
  mapStateToProps
)(GameNumber);


export default GameNumber;

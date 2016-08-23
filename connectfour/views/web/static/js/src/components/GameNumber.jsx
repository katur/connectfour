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
      <div id="game-number">Game {this.props.gameNumber}</div>
    );
  },
});


GameNumber = connect(
  mapStateToProps
)(GameNumber);


export default GameNumber;

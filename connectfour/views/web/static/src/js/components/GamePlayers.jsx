import React from "react";
import { connect } from "react-redux";


function mapStateToProps(state) {
  return {
    players: state.players,
  }
}


let GamePlayers = React.createClass({
  render: function() {
    return (
      <ul id="player-list">
        {this.props.players.map(function(player, i) {
          return (
            <li key={i}>{player.name}</li>
          );
        })}
      </ul>
    );
  },
});


GamePlayers = connect(
  mapStateToProps
)(GamePlayers);


export default GamePlayers;

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
      <div id="game-players">
        <h3>Players</h3>
        <ul>
          {this.props.players.map(function(player, i) {
            return (
              <li key={i}>{player.name}</li>
            );
          })}
        </ul>
      </div>
    );
  },
});


GamePlayers = connect(
  mapStateToProps
)(GamePlayers);


export default GamePlayers;

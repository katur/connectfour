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
      <div id="game-players" className="section">
        <h3>Players</h3>
        <table>
          <tbody>
            {this.props.players.map(function(player, i) {
              return (
                <tr key={player.pk}>
                  <td className={`player-key player-key-${player.color}`}>
                    {player.color}
                  </td>

                  <td>{player.name}</td>

                  <td>{player.numWins} wins</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  },
});


GamePlayers = connect(
  mapStateToProps
)(GamePlayers);


export default GamePlayers;

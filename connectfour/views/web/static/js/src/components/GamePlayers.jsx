import React from "react";
import { connect } from "react-redux";


function mapStateToProps(state) {
  return {
    players: state.players,
    nextPlayer: state.nextPlayer,
  }
}


let GamePlayers = React.createClass({
  render: function() {
    const nextPk = this.props.nextPlayer ? this.props.nextPlayer.pk : '';
    const arrow = String.fromCharCode("8592");

    return (
      <div id="game-players">
        <table>
          <tbody>
            {this.props.players.map(function(player, i) {
              return (
                <tr key={player.pk}>
                  <td className={`color-key color-${player.color}`}>
                  </td>

                  <td>
                    {player.name}
                  </td>

                  <td>{player.numWins} wins</td>

                  <td>
                    {player.pk === nextPk ? arrow : ''}
                  </td>
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

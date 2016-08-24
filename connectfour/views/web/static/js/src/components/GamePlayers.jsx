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

    return (
      <div id="game-players">
        <table>
          <tbody>
            {this.props.players.map(function(player, i) {
              return (
                <tr
                  key={player.pk}
                  className={
                    `${(player.pk === nextPk) ? 'current' : 'not-current'}`
                  }
                >

                  <td>
                    <div className={`color-key color-${player.color}`}>
                    </div>
                  </td>

                  <td>
                    {player.name}
                  </td>

                  <td>
                    {player.numWins} wins
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

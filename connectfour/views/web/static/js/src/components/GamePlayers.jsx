import React from 'react';
import { connect } from 'react-redux';


function mapStateToProps(state) {
  return {
    pk: state.pk,
    players: state.players,
    nextPlayer: state.nextPlayer,
  }
}


let GamePlayers = React.createClass({
  render: function() {
    const you = this.props.pk;
    const next = this.props.nextPlayer ? this.props.nextPlayer.pk : '';

    return (
      <div id='game-players'>
        <table>
          <tbody>
            {this.props.players.map(function(player, i) {
              return (
                <tr
                  key={player.pk}
                  className={
                    `${(player.pk !== next) ? 'current' : 'not-current'}`
                  }
                >

                  <td>
                    <div className={`color-key color-${player.color}`}>
                    </div>
                  </td>

                  <td>
                    {player.name}
                    {(player.pk === you) && ' (you)'}
                  </td>

                  <td>
                    {player.numWins} wins / {player.numGames} games
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

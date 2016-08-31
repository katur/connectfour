import React, { PropTypes } from 'react';
import { connect } from 'react-redux';


function mapStateToProps({ pk, players, nextPlayer }) {
  return {
    pk,
    players,
    nextPlayer,
  };
}


const propTypes = {
  pk: PropTypes.string.isRequired,
  players: PropTypes.array.isRequired,
  nextPlayer: PropTypes.object,
};


function GamePlayers({ pk, players, nextPlayer }) {
  const nextPk = nextPlayer ? nextPlayer.pk : '';

  return (
    <div id="game-players">
      <table>
        <tbody>
          {players.map((player, i) => (
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
                {(player.pk === pk) && ' (you)'}
              </td>

              <td>
                {player.numWins} wins / {player.numGames} games
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}


GamePlayers.propTypes = propTypes;

export default connect(mapStateToProps)(GamePlayers);

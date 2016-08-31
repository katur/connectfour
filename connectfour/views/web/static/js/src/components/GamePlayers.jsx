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
  const youPk = pk;
  const nextPk = nextPlayer ? nextPlayer.pk : '';

  return (
    <div id="game-players">
      {players.map((player, i) => (
        <div
          key={player.pk}
          className={
            `player ${(player.pk === nextPk) ? 'current' : 'not-current'}`
          }
        >
          <div className="name">
            {player.name}
            {(player.pk === youPk) && ' (you)'}
            <div className={`color-key color-${player.color}`} />
          </div>

          <div className="stats">
            {player.numWins} wins / {player.numGames}
          </div>
        </div>
      ))}
    </div>
  );
}


GamePlayers.propTypes = propTypes;

export default connect(mapStateToProps)(GamePlayers);

import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import GameColumnButton from './GameColumnButton';


function mapStateToProps(state) {
  const { numRows, numColumns, gameInProgress, nextPlayer, pk } = state;

  return {
    numRows,
    numColumns,
    gameInProgress,
    nextPlayer,
    pk,
  };
}


const propTypes = {
  numRows: PropTypes.number.isRequired,
  numColumns: PropTypes.number.isRequired,
  gameInProgress: PropTypes.bool.isRequired,
  nextPlayer: PropTypes.object,
  pk: PropTypes.string.isRequired,
};


function GameColumnButtons({ numRows, numColumns, gameInProgress, nextPlayer, pk }) {
  const percentage = 70.0 / Math.max(numRows, numColumns);
  const size = `${percentage}vmin`;
  const enabled = gameInProgress && nextPlayer && pk === nextPlayer.pk;
  const row = [];

  for (let i = 0; i < numColumns; i++) {
    row.push(
      <GameColumnButton
        key={i}
        column={i}
        style={{
          width: size,
        }}
        disabled={!enabled}
      />
    );
  }

  return (
    <div id="game-column-buttons">{row}</div>
  );
}


GameColumnButtons.propTypes = propTypes;

export default connect(mapStateToProps)(GameColumnButtons);

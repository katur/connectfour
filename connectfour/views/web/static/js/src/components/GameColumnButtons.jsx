import React from 'react';
import { connect } from 'react-redux';

import GameColumnButton from './GameColumnButton';


function mapStateToProps(state) {
  return {
    numRows: state.numRows,
    numColumns: state.numColumns,
    gameInProgress: state.gameInProgress,
    pk: state.pk,
    nextPlayer: state.nextPlayer,
  }
}

let GameColumnButtons = React.createClass({
  propTypes: {
    numRows: React.PropTypes.number.isRequired,
    numColumns: React.PropTypes.number.isRequired,
    gameInProgress: React.PropTypes.bool.isRequired,
    pk: React.PropTypes.string.isRequired,
    nextPlayer: React.PropTypes.object,
  },

  render: function() {
    const percentage = 80.0 / Math.max(this.props.numRows,
                                       this.props.numColumns);
    const size = `${percentage}vmin`;

    const enabled = this.props.gameInProgress
      && this.props.nextPlayer
      && this.props.pk === this.props.nextPlayer.pk;

    const row = [];

    for (let i = 0; i < this.props.numColumns; i++) {
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
  },
});


GameColumnButtons = connect(
  mapStateToProps
)(GameColumnButtons);


export default GameColumnButtons;

import React from "react";
import { connect } from "react-redux";
import GameColumnButton from "./GameColumnButton";


function mapStateToProps(state) {
  return {
    numRows: state.numRows,
    numColumns: state.numColumns,
    gameInProgress: state.gameInProgress,
    username: state.username,
    nextPlayer: state.nextPlayer,
  }
}


let GameColumnButtons = React.createClass({
  render: function() {
    const percentage = 80.0 / Math.max(this.props.numRows,
                                       this.props.numColumns);
    const size = percentage + "vmin";

    let row = [];
    let enabled = this.props.gameInProgress &&
        this.props.username === this.props.nextPlayer.name;

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

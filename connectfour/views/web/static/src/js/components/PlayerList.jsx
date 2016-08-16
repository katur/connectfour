import React from "react";
import { connect } from "react-redux";


function mapStateToProps(state) {
  return {
    players: state.players,
  }
}


var PlayerList = React.createClass({
  render: function() {
    return (
      <ul id="player-list">
        {this.props.players.map(function(player, i) {
          return (
            <li key={i}>{player.name}</li>
          );
        })}
      </ul>
    );
  },
});


PlayerList = connect(
  mapStateToProps
)(PlayerList);


export default PlayerList;

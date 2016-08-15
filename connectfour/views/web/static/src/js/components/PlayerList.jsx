import React from "react";


const PlayerList = React.createClass({
  render: function() {
    return (
      <ul id="player-list">
        {this.props.players.forEach(function(player) {
          console.log(player.name);
          return (
            <li>{player.name}</li>
          );
        })}
      </ul>
    );
  },
});


export default PlayerList;

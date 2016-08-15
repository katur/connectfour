import React from "react";


const GameScreen = React.createClass({
  render: function() {
    if (!this.props.show) {
      return null;
    }

    return (
      <div>Hi we are playing the game</div>
    );
  },
});


export default GameScreen;

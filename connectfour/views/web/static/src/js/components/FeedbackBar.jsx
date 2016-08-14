import React from "react";


const FeedbackBar = React.createClass({
  getInitialState: function() {
    return {
      text: ``,
    };
  },

  render: function() {
    return (
      <div id="game-feedback">{this.state.text}</div>
    );
  },
});


module.exports = FeedbackBar;

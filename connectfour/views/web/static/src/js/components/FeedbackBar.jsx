import React from "react";


const FeedbackBar = React.createClass({
  render: function() {
    return (
      <div id="feedback-bar">{this.props.text}</div>
    );
  },
});


export default FeedbackBar;

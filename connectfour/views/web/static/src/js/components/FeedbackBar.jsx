import React from "react";
import { connect } from 'react-redux'


function mapStateToProps(state) {
  return {
    text: state.feedback,
    room: state.room,
  }
}


let FeedbackBar = React.createClass({
  render: function() {
    return (
      <div id="feedback-bar">{this.props.text} | {this.props.room}</div>
    );
  },
});


FeedbackBar = connect(
  mapStateToProps
)(FeedbackBar);


export default FeedbackBar;

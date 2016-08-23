import React from "react";
import { connect } from 'react-redux'


function mapStateToProps(state) {
  return {
    text: state.feedback,
  }
}


let GameFeedback = React.createClass({
  render: function() {
    return (
      <div id="game-feedback">
        {this.props.text}
      </div>
    );
  },
});


GameFeedback = connect(
  mapStateToProps
)(GameFeedback);


export default GameFeedback;

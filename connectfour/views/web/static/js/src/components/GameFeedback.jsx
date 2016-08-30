import React from 'react';
import { connect } from 'react-redux';


function mapStateToProps(state) {
  return {
    feedback: state.feedback,
  }
}


let GameFeedback = React.createClass({
  propTypes: {
    feedback: React.PropTypes.string.isRequired,
  },

  render: function() {
    return (
      <div id="game-feedback">
        {this.props.feedback}
      </div>
    );
  },
});


GameFeedback = connect(
  mapStateToProps
)(GameFeedback);


export default GameFeedback;

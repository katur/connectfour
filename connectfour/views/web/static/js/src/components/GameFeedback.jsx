import React, { PropTypes } from 'react';
import { connect } from 'react-redux';


function mapStateToProps({ feedback }) {
  return {
    feedback,
  };
}


const propTypes = {
  feedback: PropTypes.string.isRequired,
};


function GameFeedback({ feedback }) {
  return (
    <div id="game-feedback">
      {feedback}
    </div>
  );
}


GameFeedback.propTypes = propTypes;

export default connect(mapStateToProps)(GameFeedback);

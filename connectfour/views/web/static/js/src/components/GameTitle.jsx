import React, { PropTypes } from 'react';
import { connect } from 'react-redux';


function mapStateToProps({ numToWin }) {
  return {
    numToWin,
  };
}


const propTypes = {
  numToWin: PropTypes.number,
};


function GameTitle({ numToWin }) {
  return (
    <div>
      <h1>
        Connect {numToWin || 'X'}
      </h1>
    </div>
  );
}


GameTitle.propTypes = propTypes;

export default connect(mapStateToProps)(GameTitle);

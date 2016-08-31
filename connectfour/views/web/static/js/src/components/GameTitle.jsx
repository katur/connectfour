import React, { PropTypes } from 'react';
import { connect } from 'react-redux';


const NUMBER_WORDS = [
  'Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
  'Nine', 'Ten',
];


function mapStateToProps({ numToWin }) {
  return {
    numToWin,
  };
}


const propTypes = {
  numToWin: PropTypes.number,
};


function GameTitle({ numToWin }) {
  if (numToWin < NUMBER_WORDS.length) {
    numToWin = NUMBER_WORDS[numToWin];
  }
  return <h1>Connect {numToWin || 'X'}</h1>;
}


GameTitle.propTypes = propTypes;

export default connect(mapStateToProps)(GameTitle);

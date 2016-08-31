import React, { PropTypes } from 'react';
import { connect } from 'react-redux';


function mapStateToProps({ room }) {
  return {
    room,
  };
}


const propTypes = {
  room: PropTypes.string.isRequired,
};


function GameRoom({ room }) {
  return (
    <span id="game-room">Room: {room}</span>
  );
}


GameRoom.propTypes = propTypes;

export default connect(mapStateToProps)(GameRoom);

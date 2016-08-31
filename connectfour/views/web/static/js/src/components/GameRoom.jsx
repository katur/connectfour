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
    <div id="game-room">
      <table>
        <tbody>
          <tr>
            <td>Room:</td>
            <td>{room}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}


GameRoom.propTypes = propTypes;

export default connect(mapStateToProps)(GameRoom);

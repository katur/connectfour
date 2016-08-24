import React from "react";
import { connect } from 'react-redux'


function mapStateToProps(state) {
  return {
    room: state.room,
  }
}


let GameRoomInfo = React.createClass({
  render: function() {
    return (
      <div id="game-info">
        <table>
          <tbody>
            <tr>
              <td>Room:</td>
              <td>{this.props.room}</td>
            </tr>
          </tbody>
        </table>
      </div>
    );
  },
});


GameRoomInfo = connect(
  mapStateToProps
)(GameRoomInfo);


export default GameRoomInfo;

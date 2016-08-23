import React from "react";
import { connect } from 'react-redux'


function mapStateToProps(state) {
  return {
    username: state.username,
    room: state.room,
  }
}


let GameInfo = React.createClass({
  render: function() {
    return (
      <div id="game-info">
        <table>
          <tbody>
            <tr>
              <td>User:</td>
              <td>{this.props.username}</td>
            </tr>

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


GameInfo = connect(
  mapStateToProps
)(GameInfo);


export default GameInfo;

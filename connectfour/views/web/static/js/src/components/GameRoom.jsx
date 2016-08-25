import React from "react";
import { connect } from "react-redux";


function mapStateToProps(state) {
  return {
    room: state.room,
  }
}


let GameRoom = React.createClass({
  propTypes: {
    room: React.PropTypes.string.isRequired,
  },

  render: function() {
    return (
      <div id="game-room">
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


GameRoom = connect(
  mapStateToProps
)(GameRoom);


export default GameRoom;

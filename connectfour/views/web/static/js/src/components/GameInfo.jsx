import React from "react";
import { connect } from 'react-redux'


function mapStateToProps(state) {
  return {
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

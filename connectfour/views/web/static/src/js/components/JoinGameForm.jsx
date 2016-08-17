import React from "react";
import Emitters from "../emitters";


const JoinGameForm = React.createClass({
  getInitialState: function() {
    return {
      room: ``,
      username: ``,
    };
  },

  _handleInput: function(e) {
    this.setState({
      [e.target.name]: e.target.value,
    });
  },

  _handleSubmit: function(e) {
    e.preventDefault();
    Emitters.addUser({
      username: this.state.username,
      room: this.state.room,
    });
  },

  render: function() {
    return (
      <div>
        <h2>Join a game room?</h2>

        <form
          id="join-game-form"
          action=""
          method="post"
          onSubmit={this._handleSubmit}
        >
          <dl>
            <dt>Room ID</dt>
            <dd>
              <input
                type="text"
                name="room"
                value={this.state.room}
                onChange={this._handleInput}
              />
            </dd>

            <dt>Your username</dt>
            <dd>
              <input
                type="text"
                name="username"
                value={this.state.username}
                onChange={this._handleInput}
              />
            </dd>
          </dl>

          <button type="submit">Submit</button>
        </form>
      </div>
    );
  },
});


export default JoinGameForm;

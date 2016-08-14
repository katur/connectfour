const React = require("react");

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

  render: function() {
    return (
      <div>
        <h2>Join a game room?</h2>

        <form id="join-game-form" action="" method="post">
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

          <input type="submit" value="Submit" />
        </form>
      </div>
    );
  },
});

module.exports = JoinGameForm;

const React = require("react");

const JoinGameForm = React.createClass({
  render: function() {
    return (
      <div>
        <h2>Join a game room?</h2>

        <form id="join-game-form" action="" method="post">
          <dl>
            <dt>Room ID</dt>
            <dd>
              <input type="text" name="room" />
            </dd>

            <dt>Your username</dt>
            <dd>
              <input type="text" name="join-username" />
            </dd>
          </dl>

          <input type="submit" value="Submit" />
        </form>
      </div>
    );
  },
});

module.exports = JoinGameForm;

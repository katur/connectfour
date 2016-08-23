import React from "react";
import Emitters from "../emitters";


let CreateRoomForm = React.createClass({
  getInitialState: function() {
    return {
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
    });

    Emitters.createBoard({
      numRows: window.DEFAULT_ROWS,
      numColumns: window.DEFAULT_COLUMNS,
      numToWin: window.DEFAULT_TO_WIN,
    });
  },

  render: function() {
    return (
      <div>
        <h3>Create a game room?</h3>

        <form
          id="create-room-form"
          action=""
          method="post"
          onSubmit={this._handleSubmit}
        >
          <dl>
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


export default CreateRoomForm;

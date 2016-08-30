import React from 'react';

import { emitAddUser, emitCreateBoard } from '../emitters';


const CreateRoomForm = React.createClass({
  getInitialState: () => {
    return {
      username: ``,
      usernameError: null,
    };
  },

  _handleInput: function(e) {
    this.setState({
      [e.target.name]: e.target.value,
    });
  },

  _handleSubmit: function(e) {
    e.preventDefault();

    if (!this.state.username) {
      this.setState({
        usernameError: 'Username required',
      });

      return;
    }

    this.setState({
      usernameError: null,
    });

    /*
    this.setState({
      usernameError: this.state.username ? null : 'Username required',
    });

    if (this.state.usernameError) {
      return;
    }
    */

    emitAddUser({
      username: this.state.username,
    });

    emitCreateBoard({
      numRows: window.DEFAULT_ROWS,
      numColumns: window.DEFAULT_COLUMNS,
      numToWin: window.DEFAULT_TO_WIN,
    });
  },

  render: function() {
    let usernameError;

    if (this.state.usernameError) {
      usernameError = <span className="error">Username required</span>;
    }

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
            <dt>
              <label htmlFor="username">
                Your username
              </label>
            </dt>

            <dd>
              <input
                type="text"
                id="username"
                name="username"
                value={this.state.username}
                onChange={this._handleInput}
              />

              {usernameError}
            </dd>
          </dl>

          <button type="submit">Submit</button>
        </form>
      </div>
    );
  },
});


export default CreateRoomForm;

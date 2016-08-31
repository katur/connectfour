import React from 'react';
import { emitAddUser, emitCreateBoard } from '../emitters';


class CreateRoomForm extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      username: '',
      usernameError: null,
    }

    // Bind callbacks to make `this` the correct context
    this._handleInput = this._handleInput.bind(this);
    this._handleSubmit = this._handleSubmit.bind(this);
  }

  _handleInput(e) {
    this.setState({
      [e.target.name]: e.target.value,
    });
  }

  _handleSubmit(e) {
    e.preventDefault();

    // Reset error state, in case there was a previous error
    this.setState({
      usernameError: null,
    });

    if (!this.state.username) {
      this.setState({
        usernameError: 'Username required',
      });

      return;
    }

    emitAddUser({
      username: this.state.username,
    });

    emitCreateBoard({
      numRows: window.DEFAULT_ROWS,
      numColumns: window.DEFAULT_COLUMNS,
      numToWin: window.DEFAULT_TO_WIN,
    });
  }

  render() {
    const { username, usernameError } = this.state;

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
                value={username}
                onChange={this._handleInput}
              />

              {usernameError &&
                <span className="error">{usernameError}</span>
              }
            </dd>
          </dl>

          <button type="submit">Submit</button>
        </form>
      </div>
    );
  }
}


export default CreateRoomForm;

import React, { PropTypes } from 'react';
import { connect } from 'react-redux';
import { emitAddUser } from '../emitters';


function mapStateToProps({ roomDoesNotExist }) {
  return {
    roomDoesNotExist,
  };
}


const propTypes = {
  roomDoesNotExist: PropTypes.bool.isRequired,
};


class JoinRoomForm extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      roomDoesNotExist: props.roomDoesNotExist,
      username: '',
      usernameError: '',
      room: '',
      roomError: '',
    }

    // Bind callbacks to make `this` the correct context
    this._handleInput = this._handleInput.bind(this);
    this._handleSubmit = this._handleSubmit.bind(this);
  }

  componentWillReceiveProps({ roomDoesNotExist }) {
    this.setState({
      roomDoesNotExist,
    });
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
      roomError: '',
      usernameError: '',
    });

    const { room, username, roomDoesNotExist } = this.state;

    if (!username) {
      this.setState({
        usernameError: 'Username required',
      });
    }

    if (!room) {
      this.setState({
        roomError: 'Room required',
      });
    }

    if (roomDoesNotExist) {
      this.setState({
        roomError: 'Room does not exist',
      });
    }

    if (!username || !room || roomDoesNotExist) {
      return;
    }

    emitAddUser({
      username: this.state.username,
      room: this.state.room,
    });
  }

  render() {
    const { username, room, usernameError, roomError } = this.state;

    return (
      <div>
        <h3>Join a game room?</h3>

        <form
          id="join-room-form"
          action=""
          method="post"
          onSubmit={this._handleSubmit}
        >
          <dl>
            <dt>
              <label htmlFor="room">
                Room ID
              </label>
            </dt>

            <dd>
              <input
                type="text"
                id="room"
                name="room"
                value={room}
                onChange={this._handleInput}
              />

              {roomError &&
                <span className="error">{roomError}</span>
              }
            </dd>

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


JoinRoomForm.propTypes = propTypes;

export default connect(mapStateToProps)(JoinRoomForm);

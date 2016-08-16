import React from "react";
import Emitters from "../emitters";


const NewGameForm = React.createClass({
  getInitialState: function() {
    return {
      numRows: `${this.props.defaultRows}`,
      numColumns: `${this.props.defaultColumns}`,
      numToWin: `${this.props.defaultToWin}`,
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

    // could this signal be received before the previous on the server?
    Emitters.createBoard({
      numRows: this.state.numRows,
      numColumns: this.state.numColumns,
      numToWin: this.state.numToWin,
    });
  },

  render: function() {
    return (
      <div>
        <h2>Set up a new game?</h2>

        <form
          id="new-game-form"
          action=""
          method="post"
          onSubmit={this._handleSubmit}
        >
          <dl>
            <dt>Num rows</dt>
            <dd>
              <input
                type="text"
                name="numRows"
                value={this.state.numRows}
                onChange={this._handleInput}
              />
            </dd>

            <dt>Num columns</dt>
            <dd>
              <input
                type="text"
                name="numColumns"
                value={this.state.numColumns}
                onChange={this._handleInput}
              />
            </dd>

            <dt>Num to win</dt>
            <dd>
              <input
                type="text"
                name="numToWin"
                value={this.state.numToWin}
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


export default NewGameForm;

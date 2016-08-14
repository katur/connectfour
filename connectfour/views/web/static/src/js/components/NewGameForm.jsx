import React from "react";
import Emitters from "../emitters";


const NewGameForm = React.createClass({
  getInitialState: function() {
    return {
      numRows: `${this.props.DEFAULT_ROWS}`,
      numColumns: `${this.props.DEFAULT_COLUMNS}`,
      numToWin: `${this.props.DEFAULT_TO_WIN}`,
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
    Emitters.addFirstPlayer({
      username: this.state.username,
    });
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


module.exports = NewGameForm;
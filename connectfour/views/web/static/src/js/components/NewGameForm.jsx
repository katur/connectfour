const React = require("react");

const NewGameForm = React.createClass({
  render: function() {
    return (
      <div>
        <h2>Set up a new game?</h2>

        <form id="new-game-form" action="" method="post">
          <dl>
            <dt>Num rows</dt>
            <dd>
              <input
                type="text"
                name="num-rows"
                defaultValue={this.props.DEFAULT_ROWS}
              />
            </dd>

            <dt>Num columns</dt>
            <dd>
              <input
                type="text"
                name="num-columns"
                defaultValue={this.props.DEFAULT_COLUMNS}
              />
            </dd>

            <dt>Num to win</dt>
            <dd>
              <input
                type="text"
                name="num-to-win"
                defaultValue={this.props.DEFAULT_TO_WIN}
              />
            </dd>

            <dt>Your username</dt>
            <dd>
              <input type="text" name="first-username" />
            </dd>
          </dl>

          <input type="submit" value="Submit" />
        </form>
      </div>
    );
  },
});

module.exports = NewGameForm;

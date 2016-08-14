import React from "react";
import NewGameForm from "./NewGameForm.jsx";
import JoinGameForm from "./JoinGameForm.jsx";


const App = React.createClass({
  render: function() {
    return (
      <div id="setup-content">
        <NewGameForm
          DEFAULT_ROWS={window.DEFAULT_ROWS}
          DEFAULT_COLUMNS={window.DEFAULT_COLUMNS}
          DEFAULT_TO_WIN={window.DEFAULT_TO_WIN}
        />

        <JoinGameForm />
      </div>
    );
  },
});


module.exports = App;

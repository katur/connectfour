import React from 'react';

import CreateRoomForm from './CreateRoomForm';
import JoinRoomForm from './JoinRoomForm';


const SetupScreen = React.createClass({
  render: function() {
    return (
      <div id='setup-screen'>
        <h1>Connect X</h1>
        <CreateRoomForm />
        <JoinRoomForm />
      </div>
    );
  },
});


export default SetupScreen;

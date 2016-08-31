import React from 'react';
import CreateRoomForm from './CreateRoomForm';
import JoinRoomForm from './JoinRoomForm';


function SetupScreen() {
  return (
    <div id="setup-screen">
      <h1 id="top-bar">Connect X</h1>
      <CreateRoomForm />
      <JoinRoomForm />
    </div>
  );
}


export default SetupScreen;

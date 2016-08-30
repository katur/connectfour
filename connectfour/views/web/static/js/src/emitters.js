export function emitAddUser(data) {
  window.ws.emit('addUser', data);
}

export function emitCreateBoard(data) {
  window.ws.emit('createBoard', data);
}

export function emitStartGame(data) {
  window.ws.emit('startGame', {});
}

export function emitPlay(data) {
  window.ws.emit('play', data);
}

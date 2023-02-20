const io = require('socket.io-client');

// connect to the socket.io server
const socket = io('http://localhost:3000');


// listen for the 'randomNumber' event and handle the incoming data
socket.on('index', (data) => {
    console.log('normalIndex:', data.normalIndex, 'jumpIndex:', data.jumpIndex);
    // update your UI or do any other processing with the received index values here
  });
  
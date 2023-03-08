const io = require("socket.io-client");

// connect to the socket.io server
const socket = io("http://localhost:3000");

socket.on("index", (data) => {
  console.log(
    "normalIndex:",
    data.normalIndex.toFixed(2),
    " | ",
    "jumpIndex:",
    data.jumpIndex.toFixed(2),
    " | ",
    "driftIndex",
    data.driftIndex.toFixed(2),
    " | ",
    "stepIndex",
    data.stepIndex.toFixed(2),
    " | ",
    "boomIndex",
    data.boomIndex.toFixed(2)
  );
});

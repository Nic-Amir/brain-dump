const WebSocket = require("ws");

const ws = new WebSocket("ws://localhost:8080");

ws.on("open", function open() {
  console.log("Connected to server");

  // Send a message to the server
  ws.send(JSON.stringify({ message: "Hello, server!" }));
});

ws.on("message", function incoming(data) {
  console.log("Received message:", data);
});

ws.on("close", function close() {
  console.log("Disconnected from server");
});

ws.on("error", function error(err) {
  console.error("WebSocket error:", err);
});

const express = require("express");
const { createServer } = require("http");
const { Server } = require("socket.io");

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
    credentials: false,
  },
});

io.on("connection", (socket) => {
  console.log(socket.id);
  socket.on("create-homework", function (data) {
    socket.broadcast.emit("create-homework", data);
  });

  socket.on("submit-homework", function (data) {
    socket.broadcast.emit("submit-homework", data);
  });
});

httpServer.listen(3000);

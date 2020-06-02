document.addEventListener('DOMContentLoaded', () => {

  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // When connected, configure buttons
  socket.on('connect', () => {
    
    socket.emit("join");

    document.querySelector('#send-button').addEventListener("click", (e) => {
      e.preventDefault();
      let message = document.getElementById("message").value;
      var date = new Date();
      var localeTimeString = date.toLocaleTimeString();
      document.getElementById("message").value = '';
      socket.emit("send message", message,  localeTimeString);
    });

    document.querySelector("#leave-button").addEventListener("click", () => {
      socket.emit("leave")
    });

  });

  // When a new message is announced, add to message list
  socket.on('announce message', data => {
      const li = document.createElement('li');
      li.innerHTML = `${data.username},  ${data.message}, ${data.timestamp}`;
      document.querySelector('#message_list').append(li);
  });

  // When a new message is announced, add to message list
  socket.on('announce join', data => {
      const li = document.createElement('li');
      li.innerHTML = `${data.username} has entered the room.`;
      document.querySelector('#message_list').append(li);
  });

  // When a new message is announced, add to message list
  socket.on('announce leave', data => {
      const li = document.createElement('li');
      li.innerHTML = `${data.username} has left the room.`;
      document.querySelector('#message_list').append(li);
  });

  // By default, submit button is disabled
  document.querySelector('#send-button').disabled = true;

  // Enable button only if there is text in the input field
  document.querySelector('#message').onkeyup = () => {
      if (document.querySelector('#message').value.length > 0)
          document.querySelector('#send-button').disabled = false;
      else
          document.querySelector('#send-button').disabled = true;
  };

});


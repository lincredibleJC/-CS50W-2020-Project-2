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

      // Remove from localStorage when you leave it
      localStorage.removeItem("last_channel")
    });

  });

  // When a new message is announced, add to message list
  socket.on('announce message', data => {
      const div = document.createElement('div');
      div.className += "message"
      div.innerHTML = `<a class="message_profile-pic" href=""></a> \
                      <a class="message_username" href="">${data.username}</a> \
                      <span class="message_timestamp">${data.timestamp}</span> \
                      <span class="message_content">${data.message}</span>`
      document.querySelector('#message_list').append(div);
  });

  // When a new message is announced, add to message list
  socket.on('announce user', data => {
      const div = document.createElement('div');
      div.className += "notification"
      div.innerHTML = `<span class="notification_text">${data.message}</span>`
      document.querySelector('#message_list').append(div);

      // Save the current channel in local storage
      // will trigger when entering a channel because of user's own entry announcement
      localStorage.setItem("last_channel", data.channel)
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


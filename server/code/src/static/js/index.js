function drawStaffMessage(text) {
  let message = document.createElement('div');
  message.classList.add('staff-message');
  message.textContent = text;
  let messagesBox = document.getElementById('messages-box');
  messagesBox.appendChild(message);
}

function drawUserMessage(sender, text) {
    let messageBox = document.createElement('div');
    messageBox.classList.add('message-box');
    let messageSender = document.createElement('div');
    messageSender.classList.add('message-sender');
    messageSender.textContent = sender;
    messageBox.appendChild(messageSender);
    let message = document.createElement('div');
    message.classList.add('user-message');
    message.textContent = text;
    messageBox.appendChild(message);
    let messagesBox = document.getElementById('messages-box');
    messagesBox.appendChild(messageBox);
}

function drawMessage(data) {
  if (data.sender == 'staff') {
    drawStaffMessage(data.text);
  } else {
    drawUserMessage(data.sender, data.text);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const socket = new WebSocket('ws://localhost:8080/ws');

  socket.addEventListener('open', function(e) {
    console.log('socket server connection has been opened');
  });

  socket.addEventListener('message', function(e) {
    let data = JSON.parse(e.data);
    drawMessage(data);
  });

  socket.addEventListener('close', function(e) {
    console.log('socket server connection has been closed');
  });

  socket.addEventListener('error', function(e) {
    console.log('socket server connection error', e);
  });

  let textInput = document.getElementById('text-input');
  textInput.addEventListener('keypress', (e) => {
    if (e.charCode == 13 && e.ctrlKey) {
      let value = textInput.value.trim();
      if (value.length > 0) {
        socket.send(textInput.value);
        textInput.value = '';
      }
    }
  });
});

// Initialize a Socket.IO connection
var socket = io();

// Get the chat button element
var chatButton = document.getElementById("chat-button");

// Get the chat window element
var chatWindow = document.getElementById("chat-window");

// Get the chat messages element
var chatMessages = document.getElementById("chat-messages");

// Get the chat form element
var chatForm = document.getElementById("chat-form");

// Get the chat input element
var chatInput = document.getElementById("chat-input");

// Get the chat send button element
var chatSend = document.getElementById("chat-send");

// Add a click event listener to the chat button
chatButton.addEventListener("click", function() {
  // Toggle the visibility of the chat window
  if (chatWindow.style.display === "none") {
    chatWindow.style.display = "block";
  } else {
    chatWindow.style.display = "none";
  }
  // Scroll to the bottom of the chat messages
  chatMessages.scrollTop = chatMessages.scrollHeight;
  // Focus on the chat input
  chatInput.focus();
});

// Add a submit event listener to the chat form
chatForm.addEventListener("submit", function(event) {
  // Prevent the default behavior of the form
  event.preventDefault();
  // Get the value of the chat input
  var message = chatInput.value;
  // If the message is not empty
  if (message) {
    // Emit a "chat message" event to the server with the message
    socket.emit("chat message", message);
    // Clear the chat input
    chatInput.value = "";
    // Append the message to the chat messages as a sender
    var senderMessage = document.createElement("div");
    senderMessage.style.textAlign = "right";
    senderMessage.style.margin = "10px";
    senderMessage.style.backgroundColor = "lightblue";
    senderMessage.style.padding = "10px";
    senderMessage.style.borderRadius = "10px";
    senderMessage.textContent = message;
    chatMessages.appendChild(senderMessage);
    // Scroll to the bottom of the chat messages
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});

// Add a listener for the "chat message" event from the server
socket.on("chat message", function(message) {
  // Append the message to the chat messages as a receiver
  var receiverMessage = document.createElement("div");
  receiverMessage.style.textAlign = "left";
  receiverMessage.style.margin = "10px";
  receiverMessage.style.backgroundColor = "lightgreen";
  receiverMessage.style.padding = "10px";
  receiverMessage.style.borderRadius = "10px";
  receiverMessage.textContent = message;
  chatMessages.appendChild(receiverMessage);
  // Scroll to the bottom of the chat messages
  chatMessages.scrollTop = chatMessages.scrollHeight;
});

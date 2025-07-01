document.addEventListener("DOMContentLoaded", function () {
  if (
    !document.getElementById("receiverId") ||
    !document.getElementById("currentUserId") ||
    !document.getElementById("currentUsername")
  ) {
    console.warn("Chat DOM elements not found.");
    return;
  }
  const receiverId = parseInt(
    document.getElementById("receiverId").textContent
  );
  const currentUserId = parseInt(
    document.getElementById("currentUserId").textContent
  );
  const currentUsername =
    document.getElementById("currentUsername").textContent;
  const chatLog = document.getElementById("chatLog");
  const messageInput = document.getElementById("messageInput");

  chatLog.scrollTop = chatLog.scrollHeight;

  const chatSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/chat/" + receiverId + "/"
  );

  function escapeHTML(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  function addMessageToLog(
    senderName,
    messageContent,
    senderId,
    timestamp = new Date()
  ) {
    const messageBubble = document.createElement("div");
    messageBubble.classList.add("message-bubble");
    messageBubble.classList.add(
      senderId === currentUserId ? "sent" : "received"
    );

    let formattedTime = timestamp;
    if (typeof timestamp === "string") {
      try {
        const dateObj = new Date(timestamp);
        formattedTime = dateObj.toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        });
      } catch {
        formattedTime = new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        });
      }
    } else {
      formattedTime = timestamp.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
    }

    if (senderId !== currentUserId) {
      const senderNameSpan = document.createElement("span");
      senderNameSpan.classList.add("sender-name");
      senderNameSpan.innerHTML = escapeHTML(senderName);
      messageBubble.appendChild(senderNameSpan);
    }

    const messageContentSpan = document.createElement("span");
    messageContentSpan.classList.add("message-content");
    messageContentSpan.innerHTML = escapeHTML(messageContent);
    messageBubble.appendChild(messageContentSpan);

    const timestampSpan = document.createElement("span");
    timestampSpan.classList.add("timestamp");
    timestampSpan.textContent = formattedTime;
    messageBubble.appendChild(timestampSpan);

    chatLog.appendChild(messageBubble);
    chatLog.scrollTop = chatLog.scrollHeight;
  }

  chatSocket.onopen = function () {
    console.log("WebSocket connection established.");
  };

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const { sender, message, sender_id, timestamp } = data;
    addMessageToLog(sender, message, sender_id, timestamp);
  };

  chatSocket.onclose = function () {
    console.error("Chat socket closed unexpectedly. Reloading in 3s...");
    setTimeout(() => location.reload(), 3000);
  };

  chatSocket.onerror = function (e) {
    console.error("WebSocket error:", e);
  };

  function sendMessage() {
    const messageText = messageInput.value.trim();
    if (messageText === "") return;

    chatSocket.send(JSON.stringify({ message: messageText }));
    messageInput.value = "";
  }

  messageInput.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }
  });
});

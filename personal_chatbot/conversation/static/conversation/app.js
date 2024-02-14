const frmChatForm = document.querySelector(".frmChat-inputarea");
const frmChatInput = document.querySelector(".frmChat-input");
const frmChatChat = document.querySelector(".frmChat-chat");
const cmdEnableInputChecks = document.getElementById("cmdEnableInputChecks");
const cmdEnableOutputChecks = document.getElementById("cmdEnableOutputChecks");

const BOT_NAME = "Bot";
const PERSON_NAME = "User";

appendMessage(BOT_NAME, "bot", "left", "Welcome");

frmChatForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const msgText = frmChatInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, "user", "right", msgText);
  frmChatInput.value = "";

  botResponse(msgText);
});

function appendMessage(name, persona, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img ${persona}"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  frmChatChat.insertAdjacentHTML("beforeend", msgHTML);
  frmChatChat.scrollTop += 500;
}

function botResponse(userInput) {
  

  // Invoke the API/chat endpoint with user input and flags
  // Replace the API_URL with the actual endpoint URL
  fetch("/conversation/api/data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt: userInput,
      
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      const botResponse = data.response;
      appendMessage(BOT_NAME, "bot", "left", botResponse);
    })
    .catch((error) => {
      appendMessage(BOT_NAME, "bot", "left", "UI Error:" + error);
    });
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

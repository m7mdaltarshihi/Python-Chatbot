const userQueryInput = document.getElementById("user-query");
const chatMessagesDiv = document.getElementById("chat-messages");
const sendMessageButton = document.getElementById("send-message");
const newChatButton = document.getElementById("new-chat");

const api_url = "http://127.0.0.1:8000/api/query";

let messages = JSON.parse(localStorage.getItem("chatMessages")) || [];

function saveMessagesToLocalStorage() {
    localStorage.setItem("chatMessages", JSON.stringify(messages));
}

function addDefaultMessage() {

    const messageWrapper = document.createElement("div");
    messageWrapper.innerHTML = ` 
        <div class="chat-content">
            <div class="chat-details">
                <p><i class="fa-solid fa-robot" style="color: #00BFFF;"></i>  Hello! I'm here to help you. Ask me anything about Python!</p>
            </div>
        </div>
    `;
    messageWrapper.classList.add("chat", "incoming");
    chatMessagesDiv.appendChild(messageWrapper);
    chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight; 
}

function addTypingAnimation() {
    const typingWrapper = document.createElement("div");

    typingWrapper.innerHTML = `
        <div class="chat-content">
            <div class="chat-details">
                <div class="typing-animation">
                    <span class="typing-dot" style="--delay: 0s"></span>
                    <span class="typing-dot" style="--delay: 0.2s"></span>
                    <span class="typing-dot" style="--delay: 0.4s"></span>
                </div>
            </div>
        </div>
    `;
    typingWrapper.classList.add("chat", "incoming", "typing-animation");
    chatMessagesDiv.appendChild(typingWrapper);
    // chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight;

    return typingWrapper; 
}

function removeTypingAnimation(typingIndicator) {
    if (typingIndicator) {
        chatMessagesDiv.removeChild(typingIndicator);
    }
}

function addMessageToChat(sender, messageContent, messageClass, source = "") {
    const messageWrapper = document.createElement("div");

    let senderIcon = '';
    if (sender === "You") {
        senderIcon = '<i class="fa-solid fa-user" style="color: #32CD32;"></i>';
    } else if (sender === "AI") {
        senderIcon = '<i class="fa-solid fa-robot" style="color: #00BFFF;"></i>';
    }
    
    messageWrapper.innerHTML = `
        <div class="chat-content">
            <div class="chat-details">
                <p>${senderIcon}  ${messageContent}</p>
                ${source ? `<p class="message-source">Sources: ${source}</p>` : ""}
            </div>
        </div>
    `;
    
    messageWrapper.classList.add("chat", messageClass);
    chatMessagesDiv.appendChild(messageWrapper);
    chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight; 
}

async function sendMessage() {
    const userQuery = userQueryInput.value;

    if (!userQuery) {
        alert("Please enter a message.");
        return;
    }

    messages.push({ role: "user", content: userQuery });
    addMessageToChat("You", userQuery, "outgoing");

    userQueryInput.value = ""

    const typingIndicator = addTypingAnimation();

    const options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: messages.slice(-3) }),
    };

    try {
        const response = await fetch(api_url, options);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const assistantResponse = data.content;
        let source = data.source || "Unknown source";

        if (source !== "Unknown source") {
            const uniqueSources = [...new Set(source.split(/\s+/))];
            source = uniqueSources.join("\n");
        }

        removeTypingAnimation(typingIndicator);

        messages.push({ role: "assistant", content: assistantResponse, source });
        addMessageToChat("AI", assistantResponse, "incoming", source);

        saveMessagesToLocalStorage(); 

    } catch (error) {
        console.error("Error querying documents:", error);
        removeTypingAnimation(typingIndicator); 
        alert("An error occurred while processing your request.");
    }
}

function loadChatHistory() {
    messages.forEach(message => {
        const sender = message.role === "user" ? "You" : "AI";
        const messageClass = message.role === "user" ? "outgoing" : "incoming";
        const source = message.source || ""; 
        addMessageToChat(sender, message.content, messageClass, source);
    });
}

function startNewChat() {
    localStorage.removeItem("chatMessages");
    messages = [];
    chatMessagesDiv.innerHTML = ""; 
    addDefaultMessage(); 
}

userQueryInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault(); 
        sendMessage(); 
    }
});

sendMessageButton.addEventListener("click", sendMessage);
newChatButton.addEventListener("click", startNewChat); 

addDefaultMessage();
loadChatHistory(); 
// Modern Chat Widget with Enhanced Blue UI
(() => {
  // Get the base URL of the chat server (set via a data attribute on the script tag)
  const scriptTag = document.currentScript;
  const baseUrl = scriptTag.getAttribute("data-base-url") || "";

  // Helper: create an element with classes or id
  function createEl(tag, attrs) {
    const el = document.createElement(tag);
    for (const key in attrs) {
      if (key === "text") {
        el.textContent = attrs[key];
      } else if (key === "html") {
        el.innerHTML = attrs[key];
      } else {
        el.setAttribute(key, attrs[key]);
      }
    }
    return el;
  }

  // Inject CSS styles for the chat widget into the page
  const style = document.createElement("style");
  style.textContent = `
    /* --- Modern Blue Chat Widget Styles --- */
    #django-chat-widget {
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 10000;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    #django-chat-widget .chat-button {
      width: 64px;
      height: 64px;
      border-radius: 32px;
      background: linear-gradient(135deg, #0078ff, #00a2ff);
      color: #fff;
      text-align: center;
      line-height: 64px;
      font-size: 26px;
      cursor: pointer;
      box-shadow: 0 6px 16px rgba(0, 120, 255, 0.4);
      transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
      0% {
        box-shadow: 0 0 0 0 rgba(0, 120, 255, 0.4);
      }
      70% {
        box-shadow: 0 0 0 10px rgba(0, 120, 255, 0);
      }
      100% {
        box-shadow: 0 0 0 0 rgba(0, 120, 255, 0);
      }
    }
    
    #django-chat-widget .chat-button:hover {
      transform: scale(1.1) translateY(-5px);
      box-shadow: 0 10px 20px rgba(0, 120, 255, 0.5);
    }
    
    #django-chat-widget .chat-box {
      width: 360px;
      height: 500px;
      background: #fff;
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.2);
      overflow: hidden;
      transition: all 0.4s cubic-bezier(0.19, 1, 0.22, 1);
      transform-origin: bottom right;
      animation: slideIn 0.4s cubic-bezier(0.19, 1, 0.22, 1);
    }
    
    @keyframes slideIn {
      0% {
        opacity: 0;
        transform: translateY(20px) scale(0.9);
      }
      100% {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
    }
    
    #django-chat-widget .chat-header {
      background: linear-gradient(135deg, #0078ff, #00a2ff);
      color: #fff;
      padding: 18px 20px;
      font-size: 18px;
      font-weight: 600;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    #django-chat-widget .chat-header .chat-title {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    
    #django-chat-widget .chat-header .chat-title-icon {
      font-size: 20px;
    }
    
    #django-chat-widget .chat-header .chat-user-email {
      font-weight: normal;
      font-size: 13px;
      opacity: 0.9;
      margin-left: 5px;
    }
    
    #django-chat-widget .chat-header .chat-close-btn {
      background: rgba(255, 255, 255, 0.2);
      border: none;
      color: #fff;
      font-size: 18px;
      width: 28px;
      height: 28px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
    }
    
    #django-chat-widget .chat-header .chat-close-btn:hover {
      background: rgba(255, 255, 255, 0.3);
      transform: rotate(90deg);
    }
    
    #django-chat-widget .chat-body {
      flex: 1;
      display: flex;
      flex-direction: column;
      padding: 20px;
      overflow: hidden;
      background-color: #f0f7ff;
      background-image: linear-gradient(rgba(255, 255, 255, 0.8) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(255, 255, 255, 0.8) 1px, transparent 1px);
      background-size: 20px 20px;
    }
    
    #django-chat-widget .email-form {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      padding: 30px;
      background-color: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0, 120, 255, 0.1);
      animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    #django-chat-widget .email-form h3 {
      margin-bottom: 16px;
      color: #0078ff;
      font-size: 22px;
      font-weight: 600;
    }
    
    #django-chat-widget .email-form p {
      margin-bottom: 24px;
      color: #64748b;
      text-align: center;
      font-size: 15px;
      line-height: 1.5;
    }
    
    #django-chat-widget .email-form input[type="email"] {
      width: 100%;
      padding: 12px 16px;
      margin-bottom: 20px;
      border: 2px solid #e2e8f0;
      border-radius: 10px;
      font-size: 15px;
      transition: all 0.3s ease;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    
    #django-chat-widget .email-form input[type="email"]:focus {
      border-color: #0078ff;
      outline: none;
      box-shadow: 0 0 0 3px rgba(0, 120, 255, 0.2);
    }
    
    #django-chat-widget .email-form button {
      width: 100%;
      padding: 12px 20px;
      border: none;
      border-radius: 10px;
      background: linear-gradient(135deg, #0078ff, #00a2ff);
      color: #fff;
      font-size: 16px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.3s ease;
      box-shadow: 0 4px 10px rgba(0, 120, 255, 0.3);
    }
    
    #django-chat-widget .email-form button:hover {
      background: linear-gradient(135deg, #0069e0, #0091e0);
      transform: translateY(-2px);
      box-shadow: 0 6px 15px rgba(0, 120, 255, 0.4);
    }
    
    #django-chat-widget .email-form button:active {
      transform: translateY(1px);
    }
    
    #django-chat-widget .chat-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      height: 100%;
    }
    
    #django-chat-widget .message-list {
      flex: 1;
      overflow-y: auto;
      padding: 10px 0;
      display: flex;
      flex-direction: column;
      gap: 16px;
      scroll-behavior: smooth;
    }
    
    #django-chat-widget .message-list::-webkit-scrollbar {
      width: 6px;
    }
    
    #django-chat-widget .message-list::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.05);
      border-radius: 3px;
    }
    
    #django-chat-widget .message-list::-webkit-scrollbar-thumb {
      background: rgba(0, 120, 255, 0.3);
      border-radius: 3px;
    }
    
    #django-chat-widget .message-list::-webkit-scrollbar-thumb:hover {
      background: rgba(0, 120, 255, 0.5);
    }
    
    #django-chat-widget .message {
      padding: 12px 16px;
      border-radius: 18px;
      max-width: 80%;
      word-wrap: break-word;
      position: relative;
      line-height: 1.5;
      font-size: 15px;
      transition: all 0.3s ease;
      animation: messageIn 0.3s ease;
    }
    
    @keyframes messageIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    #django-chat-widget .message.visitor {
      background: linear-gradient(135deg, #0078ff, #00a2ff);
      color: #fff;
      align-self: flex-end;
      border-bottom-right-radius: 4px;
      margin-left: 20%;
      box-shadow: 0 2px 8px rgba(0, 120, 255, 0.3);
    }
    
    #django-chat-widget .message.admin {
      background: #fff;
      color: #1e293b;
      align-self: flex-start;
      border-bottom-left-radius: 4px;
      margin-right: 20%;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
      border-left: 3px solid #0078ff;
    }
    
    #django-chat-widget .message:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    #django-chat-widget .message-sender {
      font-size: 13px;
      margin-bottom: 6px;
      font-weight: 600;
      display: flex;
      align-items: center;
    }
    
    #django-chat-widget .message.admin .message-sender {
      color: #0078ff;
    }
    
    #django-chat-widget .message.visitor .message-sender {
      color: rgba(255, 255, 255, 0.95);
    }
    
    #django-chat-widget .message-content {
      margin-bottom: 4px;
    }
    
    #django-chat-widget .message-time {
      font-size: 11px;
      opacity: 0.7;
      margin-top: 4px;
      text-align: right;
    }
    
    #django-chat-widget .message-input-area {
      display: flex;
      margin-top: 20px;
      background: #fff;
      border-radius: 12px;
      padding: 10px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease;
      border: 2px solid transparent;
    }
    
    #django-chat-widget .message-input-area:focus-within {
      border-color: #0078ff;
      box-shadow: 0 4px 15px rgba(0, 120, 255, 0.15);
    }
    
    #django-chat-widget .message-input-area input {
      flex: 1;
      padding: 10px 14px;
      border: none;
      font-size: 15px;
      background: transparent;
      color: #1e293b;
    }
    
    #django-chat-widget .message-input-area input::placeholder {
      color: #94a3b8;
    }
    
    #django-chat-widget .message-input-area input:focus {
      outline: none;
    }
    
    #django-chat-widget .message-input-area button {
      padding: 10px 20px;
      background: linear-gradient(135deg, #0078ff, #00a2ff);
      border: none;
      border-radius: 10px;
      color: #fff;
      font-size: 15px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.3s ease;
      box-shadow: 0 2px 6px rgba(0, 120, 255, 0.3);
      display: flex;
      align-items: center;
      gap: 6px;
    }
    
    #django-chat-widget .message-input-area button:hover {
      background: linear-gradient(135deg, #0069e0, #0091e0);
      transform: translateY(-2px);
      box-shadow: 0 4px 10px rgba(0, 120, 255, 0.4);
    }
    
    #django-chat-widget .message-input-area button:active {
      transform: translateY(1px);
    }
    
    /* Status indicator */
    #django-chat-widget .status-indicator {
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      margin-right: 8px;
      position: relative;
    }
    
    #django-chat-widget .status-indicator.online {
      background-color: #10b981;
      box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
    }
    
    #django-chat-widget .status-indicator.online::after {
      content: '';
      position: absolute;
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background-color: #10b981;
      opacity: 0.4;
      animation: pulse-green 2s infinite;
    }
    
    @keyframes pulse-green {
      0% {
        transform: scale(1);
        opacity: 0.4;
      }
      70% {
        transform: scale(2);
        opacity: 0;
      }
      100% {
        transform: scale(1);
        opacity: 0;
      }
    }
    
    #django-chat-widget .status-indicator.offline {
      background-color: #94a3b8;
    }
    
    /* Role badges */
    #django-chat-widget .role-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 3px 8px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 600;
      margin-left: 8px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    #django-chat-widget .role-badge.admin {
      background-color: #0078ff;
      color: white;
      box-shadow: 0 2px 4px rgba(0, 120, 255, 0.3);
    }
    
    #django-chat-widget .role-badge.customer {
      background-color: rgba(255, 255, 255, 0.25);
      color: white;
      backdrop-filter: blur(4px);
    }
    
    /* Hide the chat-box by default (when minimized) */
    #django-chat-widget .chat-box {
      display: none;
    }
    
    /* Typing indicator */
    #django-chat-widget .typing-indicator {
      display: none;
      padding: 10px 14px;
      background: rgba(255, 255, 255, 0.9);
      border-radius: 18px;
      font-size: 13px;
      color: #64748b;
      align-self: flex-start;
      margin-top: 8px;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
      animation: fadeIn 0.3s ease;
    }
    
    #django-chat-widget .typing-dots {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      margin-left: 6px;
    }
    
    #django-chat-widget .typing-dot {
      width: 4px;
      height: 4px;
      border-radius: 50%;
      background-color: #64748b;
      margin: 0 2px;
      animation: typingDot 1.4s infinite ease-in-out;
    }
    
    #django-chat-widget .typing-dot:nth-child(1) {
      animation-delay: 0s;
    }
    
    #django-chat-widget .typing-dot:nth-child(2) {
      animation-delay: 0.2s;
    }
    
    #django-chat-widget .typing-dot:nth-child(3) {
      animation-delay: 0.4s;
    }
    
    @keyframes typingDot {
      0%, 60%, 100% {
        transform: translateY(0);
      }
      30% {
        transform: translateY(-4px);
      }
    }
    
    /* Empty state */
    #django-chat-widget .empty-state {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      color: #64748b;
      text-align: center;
      padding: 30px;
      animation: fadeIn 0.5s ease;
    }
    
    #django-chat-widget .empty-state-icon {
      font-size: 56px;
      margin-bottom: 20px;
      color: #0078ff;
      opacity: 0.7;
      animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
      0%, 100% {
        transform: translateY(0);
      }
      50% {
        transform: translateY(-10px);
      }
    }
    
    #django-chat-widget .empty-state-text {
      font-size: 15px;
      max-width: 260px;
      line-height: 1.6;
    }
    
    /* Responsive adjustments */
    @media (max-width: 480px) {
      #django-chat-widget .chat-box {
        width: calc(100vw - 40px);
        height: 450px;
        bottom: 80px;
        right: 20px;
      }
      
      #django-chat-widget .chat-button {
        width: 56px;
        height: 56px;
        line-height: 56px;
        font-size: 22px;
      }
    }
  `;
  document.head.appendChild(style);

  // Create main container
  const container = createEl("div", { id: "django-chat-widget" });

  // Create chat toggle button
  const chatButton = createEl("div", {
    id: "chat-button",
    class: "chat-button",
    text: "💬",
  });

  // Create chat box (hidden by default)
  const chatBox = createEl("div", { id: "chat-box", class: "chat-box" });

  // Header inside chat box
  const header = createEl("div", { class: "chat-header" });
  const titleDiv = createEl("div", { class: "chat-title" });
  const titleIcon = createEl("span", { class: "chat-title-icon", text: "💬" });
  const titleText = createEl("span", { text: "Live Support" });
  titleDiv.appendChild(titleIcon);
  titleDiv.appendChild(titleText);

  // Status indicator
  const statusIndicator = createEl("span", {
    class: "status-indicator online",
  });
  titleDiv.insertBefore(statusIndicator, titleIcon);

  const emailSpan = createEl("span", { class: "chat-user-email" }); // will hold user email
  titleDiv.appendChild(emailSpan);
  header.appendChild(titleDiv);

  const closeBtn = createEl("button", { class: "chat-close-btn" });
  closeBtn.innerHTML = "&times;"; // '×' close icon
  header.appendChild(closeBtn);
  chatBox.appendChild(header);

  // Body inside chat box
  const body = createEl("div", { class: "chat-body" });

  // Email form (initial state)
  const emailForm = createEl("div", { id: "email-form", class: "email-form" });
  const formTitle = createEl("h3", { text: "Start a Conversation" });
  const formDesc = createEl("p", {
    text: "Enter your email to begin chatting with our support team. We're here to help you with any questions you might have.",
  });
  const emailInput = createEl("input", {
    id: "chat-email-input",
    type: "email",
    placeholder: "Your email address",
  });
  const startBtn = createEl("button", {
    id: "start-chat-btn",
    text: "Start Chat",
  });

  emailForm.appendChild(formTitle);
  emailForm.appendChild(formDesc);
  emailForm.appendChild(emailInput);
  emailForm.appendChild(startBtn);
  body.appendChild(emailForm);

  // Chat content (hidden until email entered)
  const chatContent = createEl("div", {
    id: "chat-content",
    class: "chat-content",
  });
  chatContent.style.display = "none"; // hide initially

  // Empty state for new chats
  const emptyState = createEl("div", { class: "empty-state" });
  const emptyIcon = createEl("div", { class: "empty-state-icon", text: "💬" });
  const emptyText = createEl("div", {
    class: "empty-state-text",
    text: "Send a message to start the conversation. Our support team is ready to assist you!",
  });
  emptyState.appendChild(emptyIcon);
  emptyState.appendChild(emptyText);

  const messageList = createEl("div", {
    id: "message-list",
    class: "message-list",
  });
  messageList.appendChild(emptyState);

  // Typing indicator with animated dots
  const typingIndicator = createEl("div", { class: "typing-indicator" });
  typingIndicator.textContent = "Support agent is typing";
  const typingDots = createEl("span", { class: "typing-dots" });
  for (let i = 0; i < 3; i++) {
    typingDots.appendChild(createEl("span", { class: "typing-dot" }));
  }
  typingIndicator.appendChild(typingDots);
  messageList.appendChild(typingIndicator);

  const inputArea = createEl("div", { class: "message-input-area" });
  const messageInput = createEl("input", {
    id: "chat-message-input",
    type: "text",
    placeholder: "Type your message here...",
  });
  const sendBtn = createEl("button", { id: "send-message-btn" });
  sendBtn.innerHTML = "Send <span>&#10148;</span>"; // Arrow symbol

  inputArea.appendChild(messageInput);
  inputArea.appendChild(sendBtn);
  chatContent.appendChild(messageList);
  chatContent.appendChild(inputArea);
  body.appendChild(chatContent);
  chatBox.appendChild(body);

  // Append chatButton and chatBox to main container, and container to page
  container.appendChild(chatButton);
  container.appendChild(chatBox);
  document.body.appendChild(container);

  // State variables
  let sessionId = null;
  let lastMessageId = 0;
  let userEmail = null;
  let pollingInterval = null;
  let isAdmin = false; // Flag to track if the current user is an admin
  const processedMessageIds = new Set(); // Track processed message IDs to prevent duplicates
  let adminDisplayName = "Support Agent";

  // Function to format the current time
  function formatTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  // Function to append a message to the message list
  function appendMessage(sender, text, isAdminMessage = false) {
    // Remove empty state if it exists
    const emptyStateEl = messageList.querySelector(".empty-state");
    if (emptyStateEl) {
      emptyStateEl.remove();
    }

    const msgDiv = createEl("div", { class: "message " + sender });

    console.log("ADMIN", adminDisplayName);

    // Add sender label with role badge
    const senderLabel = createEl("div", { class: "message-sender" });
    if (sender === "admin") {
      senderLabel.textContent = adminDisplayName;
      const badge = createEl("span", {
        class: "role-badge admin",
        text: "STAFF",
      });
      senderLabel.appendChild(badge);
    } else {
      senderLabel.textContent = "You";
      const badge = createEl("span", {
        class: "role-badge customer",
        text: "YOU",
      });
      senderLabel.appendChild(badge);
    }
    msgDiv.appendChild(senderLabel);

    // Add message content
    const contentSpan = createEl("div", {
      class: "message-content",
      text: text,
    });
    msgDiv.appendChild(contentSpan);

    // Add timestamp
    const timeSpan = createEl("div", {
      class: "message-time",
      text: formatTime(),
    });
    msgDiv.appendChild(timeSpan);

    // Append and scroll to bottom
    messageList.appendChild(msgDiv);
    messageList.scrollTop = messageList.scrollHeight;
  }

  // Function to show typing indicator
  function showTypingIndicator(show = true) {
    const indicator = document.querySelector(
      "#django-chat-widget .typing-indicator"
    );
    if (indicator) {
      indicator.style.display = show ? "block" : "none";
    }
  }

  // Function to start polling for admin replies
  function startPolling() {
    if (pollingInterval) return;
    pollingInterval = window.setInterval(() => {
      if (!sessionId) return; // nothing to poll if no session
      const url =
        baseUrl +
        "/api/chat/messages/?session_id=" +
        sessionId +
        "&last_id=" +
        lastMessageId;
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          if (data.messages && data.messages.length > 0) {
            console.log("MESSAGES", data);

            // Filter out messages we've already processed
            const newMessages = data.messages.filter(
              (msg) => !processedMessageIds.has(msg.id)
            );

            // If we have new admin messages, show typing indicator first
            const hasNewAdminMessages = newMessages.some(
              (msg) => msg.sender === "admin"
            );

            if (hasNewAdminMessages) {
              showTypingIndicator(true);
              setTimeout(() => {
                showTypingIndicator(false);

                // Process messages after typing indicator
                newMessages.forEach((msg) => {
                  // Add to processed set to prevent duplicates
                  processedMessageIds.add(msg.id);

                  // Display the message
                  if (msg.sender === "admin") {
                    appendMessage("admin", msg.content, true);
                  } else if (msg.sender === "visitor") {
                    appendMessage("visitor", msg.content);
                  }

                  // Update lastMessageId to the latest
                  if (msg.id > lastMessageId) {
                    lastMessageId = msg.id;
                  }
                });
              }, 1000); // Show typing for 1 second
            } else if (newMessages.length > 0) {
              // No admin messages, just process normally
              newMessages.forEach((msg) => {
                processedMessageIds.add(msg.id);

                if (msg.sender === "visitor") {
                  appendMessage("visitor", msg.content);
                }

                if (msg.id > lastMessageId) {
                  lastMessageId = msg.id;
                }
              });
            }
          }

          // Check if user is admin (if the server provides this info)
          if (data.admin_display_name) {
            adminDisplayName = data.admin_display_name;
          }
          if (data.is_admin !== undefined) {
            console.log("IS ADMIN", data);
            isAdmin = data.is_admin;
            updateUIForRole();
          }
        })
        .catch((err) => {
          console.error("Polling error:", err);
        });
    }, 3000); // poll every 3 seconds (adjust as needed)
  }

  // Function to update UI based on user role
  function updateUIForRole() {
    if (isAdmin) {
      // Update UI for admin users
      titleText.textContent = "Admin Dashboard";
      const adminBadge = createEl("span", {
        class: "role-badge admin",
        text: "ADMIN",
      });
      if (!titleDiv.querySelector(".role-badge.admin")) {
        titleDiv.appendChild(adminBadge);
      }

      // Change color scheme for admin
      header.style.background = "linear-gradient(135deg, #0f766e, #0d9488)";
      document
        .querySelectorAll("#django-chat-widget .message-input-area button")
        .forEach((el) => {
          el.style.background = "linear-gradient(135deg, #0f766e, #0d9488)";
        });

      // Change chat button color
      chatButton.style.background = "linear-gradient(135deg, #0f766e, #0d9488)";
    }
  }

  // Event: Click chat bubble to open chat window
  chatButton.addEventListener("click", () => {
    chatButton.style.display = "none";
    chatBox.style.display = "flex"; // show chat window
  });

  // Event: Click close button to minimize chat
  closeBtn.addEventListener("click", () => {
    chatBox.style.display = "none";
    chatButton.style.display = "block";

    // Add a nice animation when closing
    chatBox.style.transform = "scale(0.95)";
    chatBox.style.opacity = "0";

    // Reset animation after closing
    setTimeout(() => {
      chatBox.style.transform = "";
      chatBox.style.opacity = "";
    }, 400);
  });

  // Event: Start Chat (after entering email)
  startBtn.addEventListener("click", () => {
    const emailVal = emailInput.value.trim();
    if (!emailVal) {
      alert("Please enter your email to start the chat.");
      emailInput.focus();
      return;
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailVal)) {
      alert("Please enter a valid email address.");
      emailInput.focus();
      return;
    }

    userEmail = emailVal;
    emailSpan.textContent = ` (${userEmail})`;

    // Show chat content UI and hide email form with animation
    emailForm.style.opacity = "0";
    emailForm.style.transform = "translateY(-10px)";

    setTimeout(() => {
      emailForm.style.display = "none";
      chatContent.style.display = "flex";
      chatContent.style.opacity = "0";
      chatContent.style.transform = "translateY(10px)";

      setTimeout(() => {
        chatContent.style.opacity = "1";
        chatContent.style.transform = "translateY(0)";
      }, 50);
    }, 300);

    // Add welcome message with slight delay for better UX
    setTimeout(() => {
      appendMessage(
        "admin",
        "Welcome to our chat support! How can we help you today?",
        true
      );
    }, 500);

    // Start polling in case admin sends a message
    startPolling();

    // Focus on message input
    setTimeout(() => {
      messageInput.focus();
    }, 800);
  });

  // Event: Send message
  sendBtn.addEventListener("click", () => {
    sendMessage();
  });

  // Function to send message
  function sendMessage() {
    const text = messageInput.value.trim();
    if (!text) return;
    if (!userEmail) {
      alert("Please provide your email first.");
      return;
    }

    // Append message optimistically to the UI as visitor
    appendMessage("visitor", text);
    messageInput.value = ""; // clear input
    messageInput.focus(); // keep focus on input for continuous typing

    // Prepare payload for sending
    const payload = { content: text };
    if (sessionId) {
      payload.session_id = sessionId;
    } else {
      payload.email = userEmail;
    }

    // Send to server
    fetch(baseUrl + "/api/chat/messages/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          console.error("Error from server:", data.error);
          return;
        }

        // If a new session was created, store the sessionId
        if (!sessionId && data.session_id) {
          sessionId = data.session_id;
        }

        // Update lastMessageId to at least the message we just sent
        if (data.message_id) {
          lastMessageId = data.message_id;
          // Add to processed set to prevent duplicates
          processedMessageIds.add(data.message_id);
        }

        // Check if user is admin (if the server provides this info)
        if (data.is_admin !== undefined) {
          isAdmin = data.is_admin;
          updateUIForRole();
        }

        // Show typing indicator briefly after sending a message
        showTypingIndicator(true);
        setTimeout(() => {
          showTypingIndicator(false);
        }, 2000);

        // Ensure polling is running
        startPolling();
      })
      .catch((err) => {
        console.error("Message send error:", err);
      });
  }

  // Send message on Enter key in the message input
  messageInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });

  // Focus email input when chat is opened
  chatButton.addEventListener("click", () => {
    setTimeout(() => {
      emailInput.focus();
    }, 300);
  });

  // Add smooth transition when focusing inputs
  emailInput.addEventListener("focus", () => {
    emailInput.style.boxShadow = "0 0 0 3px rgba(0, 120, 255, 0.2)";
  });

  emailInput.addEventListener("blur", () => {
    emailInput.style.boxShadow = "";
  });

  messageInput.addEventListener("focus", () => {
    inputArea.style.borderColor = "#0078ff";
    inputArea.style.boxShadow = "0 4px 15px rgba(0, 120, 255, 0.15)";
  });

  messageInput.addEventListener("blur", () => {
    inputArea.style.borderColor = "transparent";
    inputArea.style.boxShadow = "0 2px 10px rgba(0, 0, 0, 0.1)";
  });
})();

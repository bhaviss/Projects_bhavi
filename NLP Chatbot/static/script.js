// Function to send a message to the backend
function sendMessage() {
    var userInput = document.getElementById("user-input").value;

    // Display user's message in the chatbox
    const chatbox = document.getElementById("chatbox");
    const userMessage = document.createElement("div");
    userMessage.classList.add("message", "user-message");
    userMessage.innerHTML = "<p>" + userInput + "</p>";
    chatbox.appendChild(userMessage);

    // Clear the input field
    document.getElementById("user-input").value = "";

    // Send user input to the backend using AJAX
    $.ajax({
        url: "http://127.0.0.1:5000/chat",  // Ensure this matches the backend URL
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ message: userInput }),
        success: function(response) {
            const botMessage = document.createElement("div");
            botMessage.classList.add("message", "bot-message");
            botMessage.innerHTML = "<p>" + response.response + "</p>";
            chatbox.appendChild(botMessage);

            // Scroll to the bottom of the chatbox to show the latest message
            chatbox.scrollTop = chatbox.scrollHeight;
        },
        error: function() {
            const botMessage = document.createElement("div");
            botMessage.classList.add("message", "bot-message");
            botMessage.innerHTML = "<p>Sorry, there was an error. Please try again.</p>";
            chatbox.appendChild(botMessage);
        }
    });
}

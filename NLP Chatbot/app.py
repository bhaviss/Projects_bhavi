import nltk
from nltk.chat.util import Chat, reflections
from flask import Flask, jsonify, request, render_template
import random

app = Flask(__name__)

# Predefined jokes
jokes = [
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the bicycle fall over? It was two-tired!"
]

# Sample pairs of input-output patterns
pairs = [
    (r"hi|hello|hey", ["Hello! How can I assist you today?", "Hi there! How can I help?"]),
    (r"what can you do?", ["I can chat with you, answer some questions, tell you jokes, or help with simple tasks."]),
    (r"what is your name?", ["I am a chatbot created using NLTK!", "I am an AI assistant."]),
    (r"how are you?", ["I'm doing well, thank you!", "I'm great! How can I help you?"]),
    (r"tell me a joke|joke|make me laugh", [lambda: random.choice(jokes)]),
    (r"quit", ["Goodbye! Have a great day!"]),
]

chatbot = Chat(pairs, reflections)

@app.route("/")
def home():
    return render_template("index.html")  # Ensure index.html is in the templates folder

# API endpoint for receiving user input
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    
    # Check if the user asked for a joke
    if "joke" in user_input.lower():
        response = random.choice(jokes)  # Randomly select a joke
    # Check if the user asked for the bot's capabilities
    elif "what can you do" in user_input.lower():
        response = "I can chat with you, answer some questions, tell you jokes, or help with simple tasks."
    # Check if the user is quitting
    elif "quit" in user_input.lower():
        response = "Goodbye! Have a great day!"
    else:
        response = chatbot.respond(user_input)
        if not response:
            response = "Sorry, I didn’t get that. Can you rephrase?"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

import tkinter as tk
from datetime import datetime
import random



def gui_chatbot():
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Interactive Chatbot")
    root.geometry("600x700")
    root.resizable(False, False)

    # Chat display area
    chat_display = tk.Text(root, height=30, width=70, state=tk.DISABLED, wrap=tk.WORD)
    chat_display.pack(pady=10)

    # User input field
    user_input = tk.Entry(root, width=50)
    user_input.pack(pady=10)

    # State tracking
    state = {"age_step": 0, "rem3": 0, "rem5": 0, "rem7": 0, "confirm_age": False, "quiz_question": 0, "emotion": "", "name": ""}

    # Predefined jokes
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the bicycle fall over? It was two-tired!"
    ]

    # Quiz questions and answers
    quiz_questions = [
        {"question": "What is the capital of France?", "answer": "paris"},
        {"question": "Who wrote 'Romeo and Juliet'?", "answer": "shakespeare"},
        {"question": "What is the largest planet in our solar system?", "answer": "jupiter"}
    ]

    # Function to display the bot's response in the chat
    def bot_response(message):
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"Bot: {message}\n")
        chat_display.config(state=tk.DISABLED)

    # Function to handle user input
    def get_response():
        user_message = user_input.get().strip().lower()
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You: {user_message}\n")

        # If name hasn't been set yet
        if not state["name"]:
            set_name(user_message)
            return

        # Handle emotion input (respond based on user's emotion)
        emotions = ["happy", "good", "sad", "angry", "excited", "tired", "bored"]
        if any(emotion in user_message for emotion in emotions):
            state["emotion"] = user_message
            # More empathetic response based on emotion
            if "tired" in user_message:
                bot_response(f"Oh no, {state['name']}! It seems like you're feeling tired. Maybe a joke or a quick chat could help brighten your day! 😊 What would you like to guess me your age ?")
            elif "happy" in user_message:
                bot_response(f"That's wonderful, {state['name']}! 😊 I'm so glad you're feeling happy. Would you like to hear a joke or maybe take a quiz? , or guess age")
            elif "sad" in user_message:
                bot_response(f"I'm sorry to hear that you're feeling sad, {state['name']} 😔. Would you like me to tell you a fun fact or perhaps guess age or cheer you up with a joke?")
            elif "excited" in user_message:
                bot_response(f"Yay, {state['name']}! 😄 It's great to hear you're feeling excited. Want to play a quiz or hear a joke or guess your age to keep the excitement going?")
            elif "good" in user_message:
                bot_response(f"Aw, {state['name']}! 😄 It's great to hear you're feeling good. Want to play a quiz or hear a joke or guess your age to keep the excitement going?")
            else:
                bot_response(f"Oops!, {state['name']}! You're feeling {state['emotion']}.  Would you like to hear a joke or maybe take a quiz or guess age ?")
            user_input.delete(0, tk.END)  # Clear the input box
            return

        # Handle "just chat" input
        if "just chat" in user_message:
            bot_response(f"Sure, {state['name']}! Let's chat casually. What's on your mind?")
            user_input.delete(0, tk.END)  # Clear the input box
            return

        # Handle age confirmation
        if state["confirm_age"]:
            if user_message in ["yes", "y"]:
                bot_response(f"Yay, {state['name']}! I got it right! 🎉 Do you wanna continue? (a joke/ take a quiz/ wanna re guess age/exit)")
            elif user_message in ["no", "n"]:
                bot_response(f"Oh no, {state['name']}! Maybe I need to improve my guessing skills. Do you need any further assistance?")
            state["confirm_age"] = False
            user_input.delete(0, tk.END)
            return

        # Handle specific states (age guessing)
        if state["age_step"] == 1:
            state["rem3"] = int(user_message)
            bot_response(f"Enter the remainder when your age is divided by 5, {state['name']}:")
            state["age_step"] = 2
        elif state["age_step"] == 2:
            state["rem5"] = int(user_message)
            bot_response(f"Enter the remainder when your age is divided by 7, {state['name']}:")
            state["age_step"] = 3
        elif state["age_step"] == 3:
            state["rem7"] = int(user_message)
            age = (state["rem3"] * 70 + state["rem5"] * 21 + state["rem7"] * 15) % 105
            bot_response(f"Your age is {age}, {state['name']}! Am I right? (yes/no)")
            state["age_step"] = 0
            state["confirm_age"] = True

        # General chatbot logic
        elif "hello" in user_message or "hi" in user_message:
            bot_response(f"Hi {state['name']}! How can I assist you today?")
        elif "joke" in user_message:
            bot_response(random.choice(jokes))
        elif "age" in user_message:
            bot_response(f"Let me guess your age, {state['name']}! Enter the remainder when your age is divided by 3:")
            state["age_step"] = 1
        elif "quiz" in user_message:
            bot_response(f"Let's play a trivia quiz, {state['name']}! Answer the following questions.")
            bot_response(f"{quiz_questions[0]['question']}")
            state["quiz_question"] = 1
        elif state["quiz_question"] > 0:
            current_question = quiz_questions[state["quiz_question"] - 1]
            if user_message == current_question["answer"]:
                bot_response(f"Correct, {state['name']}!")
            else:
                bot_response(f"Oops, {state['name']}, the correct answer is {current_question['answer']}.")
            if state["quiz_question"] < len(quiz_questions):
                next_question = quiz_questions[state["quiz_question"]]
                bot_response(next_question["question"])
                state["quiz_question"] += 1
            else:
                bot_response(f"Quiz finished, {state['name']}! Great job!")
                state["quiz_question"] = 0
        elif "exit" in user_message:
            show_end_message()
        else:
            bot_response(f"I didn't understand that, {state['name']}. Try saying 'hello', 'age', 'joke', or 'quiz'.")

        user_input.delete(0, tk.END)  # Clear the input box after each message

    # Function for greeting based on time
    def time_based_greeting():
        current_hour = datetime.now().hour
        if current_hour < 12:
            return "Good morning!"
        elif 12 <= current_hour < 18:
            return "Good afternoon!"
        else:
            return "Good evening!"

    # Set initial greeting message
    bot_response(time_based_greeting() + " Welcome to ChatBot.")
    bot_response("What's your name?")

    # Name entry handler
    def set_name(name):
        if name:
            state["name"] = name.capitalize()  # Capitalize first letter of the name
            bot_response(f"Hi {state['name']}! How are you feeling today? Feel free to share your mood (happy/sad/good/angry/excited/tired/bored), and we can chat about it! 😊  ")
        else:
            bot_response("I didn't catch your name. Please type your name again.")
        user_input.delete(0, tk.END)

    # Show ending message with credits and version number
    def show_end_message():
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"Bot: Thank you, {state['name']}, for chatting! 😊\n")
        chat_display.insert(tk.END, "Bot: Goodbye! See you next time!\n")
        chat_display.insert(tk.END, "Bot: Version 1.0 | Created by Bhavithra & Sindhuja \n")
        chat_display.config(state=tk.DISABLED)

    # Send button
    send_button = tk.Button(root, text="Send", command=get_response, width=20, bg="lightblue")
    send_button.pack(pady=10)

    root.mainloop()

# Run the chatbot GUI
gui_chatbot()


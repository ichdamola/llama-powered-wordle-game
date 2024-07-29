# Building a Fun and Interactive Wordle Game with Generative AI 🎮
Welcome to our journey of building an engaging Wordle game using generative AI! In this blog, we'll explore how to harness the power of generative AI to create a Wordle game that is both fun and educational. We'll guide you through the entire process, from setting up your environment to implementing and running the game. Whether you're a seasoned developer or a curious beginner, this guide will help you get started.

# What is Wordle? 🤔
Wordle is a popular word-guessing game where players attempt to guess a hidden word within a limited number of tries. After each guess, feedback is provided in the form of colored tiles indicating how close the guess was to the hidden word.


# Watch the Tutorial Video 🎥

[![Watch the video](https://github.com/user-attachments/assets/a8f4f87a-f206-41be-9e30-d79e8964335e)](https://github.com/user-attachments/assets/6810f753-48ad-44be-a5eb-b05d949ca91a)

Click on the image above to watch a detailed video tutorial on how to build this Wordle game step-by-step.


# Project Overview 📋

In this tutorial, we will walk through the process of building a Wordle game. We will cover the following topics:

1. Setting up the project environment
2. Generating word patterns and lists
3. Fetching word patterns using generative AI
4. Implementing the game logic
5. Creating the user interface with Streamlit

# 1. Setting Up the Project Environment 🛠️
First, we need to set up our project environment. We will use Python and Streamlit for this project. Begin by creating a virtual environment and installing the necessary dependencies.

```
python -m venv venv
source venv/bin/activate
pip install streamlit
```
After activating the virtual environment, you should see a (venv) prefix in your terminal prompt. Install the required packages using pip:

```
pip install -r requirements.txt
```

# Generating Word Patterns and Lists 📝
We will start by defining a dictionary of word patterns and their associated words. This will be the pool from which the game will select words for the player to guess.

```
static_word_dict = {
    "5-letter": ["house", "table", "horse", "mouse", "cloud"],
    "6-letter": ["orange", "yellow", "purple", "brown", "green"]
}
```

- Install the required packages using pip:
  
# 3. Fetching Word Patterns Using Generative AI 🧠
We use a generative AI model to create word patterns and their corresponding words. This is achieved through prompt engineering.

Prompt for the Model:
```
prompt = """
below , are key pair in the entry in the JSON follow a pattern
{"5-letter": ["house", "table", "horse", "mouse", "cloud"],
"6-letter": ["orange", "yellow", "purple", "brown", "green"]
}

Generate 4 more patterns and their 5 words list associated, similar to the above example in the JSON format. Do not reuse any of the examples . Do not return anything besides the example. Do not return 
'Here are four additional patterns with 5-word lists:' in the response.
"""
```

Function to Fetch Word Patterns:
```
import json
from openai import OpenAI

def word_dict_from_llama(prompt):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    try:
        completion = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        content = completion.choices[0].message.content
        response_json = json.loads(content)
        return response_json

    except Exception as e:
        print(f"Error fetching or decoding response from OpenAI: {e}")
        return None

```


# 4. Implementing the Game Logic 🔄
Next, let's implement the game logic. This includes selecting a random word, handling user guesses, and providing feedback.

```python

import random
import streamlit as st

def initialize_game_state(word_dict):
    word_length = random.choice(list(word_dict.keys()))
    word = random.choice(word_dict[word_length])
    current_state = ["_" for _ in range(len(word))]
    return word, current_state

def get_colored_guess(guess, word):
    colored_guess = []
    for i, letter in enumerate(guess):
        if letter == word[i]:
            color = "green"
        elif letter in word:
            color = "yellow"
        else:
            color = "grey"
        colored_guess.append(
            f'<span style="background-color:{color}; color:white; border:2px solid black; '
            f'padding:10px; margin:2px; display:inline-flex; justify-content:center; align-items:center; '
            f'width:30px; height:30px; text-align:center; font-size:20px; line-height:30px;">{letter}</span>'
        )
    return " ".join(colored_guess)

def reset_game():
    st.session_state.word_dict = static_word_dict
    st.session_state.word, st.session_state.current_state = initialize_game_state(st.session_state.word_dict)
    st.session_state.attempts_left = 6
    st.session_state.failed_attempts = 0
    st.session_state.guesses = []

def wordle_game():
    st.title("Wordle Game")

    if 'word_dict' not in st.session_state:
        reset_game()

    col1, col2 = st.columns([3, 1])

    with col2:
        if st.button("New Game"):
            reset_game()

        guess = st.text_input("Enter your guess:", key="guess_input")

        if st.button("Submit Guess"):
            if 'word' not in st.session_state:
                reset_game()

            word = st.session_state.word
            current_state = st.session_state.current_state
            attempts_left = st.session_state.attempts_left
            failed_attempts = st.session_state.failed_attempts
            guesses = st.session_state.guesses

            if len(guess) != len(word):
                st.warning(f"Please enter a {len(word)}-letter word.")
            else:
                guesses.append(guess)
                correct_guess = False
                for i, letter in enumerate(guess):
                    if letter == word[i]:
                        current_state[i] = letter
                        correct_guess = True

                if not correct_guess:
                    failed_attempts += 1
                    st.error("Incorrect guess. Try again!")

                if "_" not in current_state:
                    st.success(f"Congratulations! You won! The word was {word}.")
                    st.stop()

                if failed_attempts >= 4:
                    hint_word = word[:-1]
                    st.info(f"Hint: The word is '{hint_word}' followed by one more letter.")

                if failed_attempts >= 2:
                    hint_letter = random.choice([ch for ch in word if ch not in current_state])
                    st.info(f"Hint: One of the letters in the word is '{hint_letter}'.")

                attempts_left -= 1
                st.session_state.attempts_left = attempts_left
                st.session_state.failed_attempts = failed_attempts
                st.session_state.current_state = current_state

                if attempts_left == 0:
                    st.error(f"Game Over! The word was {word}.")
                    st.stop()

                st.write(f"You have {attempts_left} attempts left.")
                st.session_state.guesses = guesses

    with col1:
        if 'word' in st.session_state:
            word = st.session_state.word
            current_state = st.session_state.current_state
            guesses = st.session_state.guesses

            st.write("Current state:")
            st.markdown(" ".join([
                f'<span style="background-color:white; border:2px solid black; padding:10px; '
                f'margin:2px; display:inline-flex; justify-content:center; align-items:center; '
                f'width:30px; height:30px; text-align:center; font-size:20px; line-height:30px;">{letter}</span>' 
                for letter in current_state
            ]), unsafe_allow_html=True)

            st.write("Previous guesses:")
            for g in guesses:
                st.markdown(f'<div style="display: flex;">{get_colored_guess(g, word)}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    wordle_game()
```
5. Creating the User Interface with Streamlit 🌐
Streamlit makes it easy to create an interactive web app. Here’s how we set up the user interface for our Wordle game:

The main game area displays the current state of the word and previous guesses.
A sidebar allows users to start a new game or submit their guesses.

# Conclusion 🌟
In this tutorial, we built a simple yet engaging Wordle game using Python and Streamlit. This project is a great way to practice your Python skills and learn about creating interactive web applications. Happy coding!

Feel free to customize and expand the game with more features and word lists. Enjoy!


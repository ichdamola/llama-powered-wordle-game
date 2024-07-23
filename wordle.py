import random
import json
from openai import OpenAI
import streamlit as st

static_word_dict = {
        "5-letter": ["house", "table", "horse", "mouse", "cloud"],
        "6-letter": ["orange", "yellow", "purple", "brown", "green"]
    }

# Function to fetch word patterns and their words from OpenAI
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

        # Extract the content from completion message
        content = completion.choices[0].message.content

        # Parse the JSON response
        response_json = json.loads(content)
        return response_json

    except Exception as e:
        print(f"Error fetching or decoding response from OpenAI: {e}")
        return None


# Example usage with your provided prompt
prompt = """
below , are key pair in the entry in the JSON follow a pattern
{"5-letter": ["house", "table", "horse", "mouse", "cloud"],
"6-letter": ["orange", "yellow", "purple", "brown", "green"]
}

Generate 4 more patterns and their 5 words list associated, similar to the above example in the JSON format. Do not reuse any of the examples . Do not return anything besides the example. Do not return 
'Here are four additional patterns with 5-word lists:' in the response.
"""

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
    st.session_state.word_dict = static_word_dict # word_dict_from_llama(prompt) #
    print(st.session_state.word_dict)
    st.session_state.word, st.session_state.current_state = initialize_game_state(st.session_state.word_dict)
    st.session_state.attempts_left = 6
    st.session_state.failed_attempts = 0
    st.session_state.guesses = []

def wordle_game():
    st.title("Wordle Game")

    # Initialize game if not started
    if 'word_dict' not in st.session_state:
        reset_game()

    col1, col2 = st.columns([3, 1])  # Create columns for layout

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
                    hint_word = word[:-1]  # Provide the word without the last letter
                    st.info(f"Hint: The word is '{hint_word}' followed by one more letter.")

                if failed_attempts >= 2:
                    hint_letter = random.choice([ch for ch in word if ch not in current_state])
                    st.info(f"Hint: One of the letters in the word is '{hint_letter}'.")

                attempts_left -= 1
                st.session_state.attempts_left = attempts_left
                st.session_state.failed_attempts = failed_attempts
                st.session_state.current_state = current_state

                if attempts_left == 0:
                    st.error(f"Game Over! Better luck next time! The word was {word}.")
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

# Start the game
if __name__ == "__main__":
    wordle_game()

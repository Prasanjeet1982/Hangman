import random
from fastapi import FastAPI, HTTPException

app = FastAPI()

# List of words for the game
word_list = ["python", "hangman", "programming", "computer", "developer", "learning"]

def choose_word():
    """Choose a random word from the word list."""
    return random.choice(word_list)

def display_word(word, guessed_letters):
    """Create a formatted string representation of the word, displaying guessed letters."""
    display = "".join([letter if letter in guessed_letters else "_" for letter in word])
    return display

def validate_guess(guess, guessed_letters):
    """Validate the guess, ensuring it is a single letter and hasn't been guessed before."""
    if len(guess) != 1 or not guess.isalpha():
        raise HTTPException(status_code=400, detail="Invalid guess. Please provide a single letter.")
    if guess in guessed_letters:
        raise HTTPException(status_code=400, detail="You already guessed that letter.")

def check_win(word, guessed_letters):
    """Check if the word has been completely guessed."""
    return all(letter in guessed_letters for letter in word)

@app.get("/")
def read_root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to Hangman API!"}

@app.post("/start")
def start_game():
    """Start a new Hangman game."""
    word_to_guess = choose_word()
    return {"message": "Game started! Try to guess the hidden word.", "word_length": len(word_to_guess)}

@app.post("/guess/{word}/{guessed_letters}")
def guess_letter(word: str, guessed_letters: str, guess: str):
    """Make a guess in the Hangman game."""
    guessed_letters = guessed_letters.lower()

    validate_guess(guess, guessed_letters)

    guessed_letters += guess

    if guess not in word:
        return {"message": f"Wrong guess! '{guess}' is not in the word.", "guessed_letters": guessed_letters}

    display = display_word(word, guessed_letters)
    
    if check_win(word, guessed_letters):
        return {"message": f"Congratulations! You guessed the word: {word}", "guessed_letters": guessed_letters}

    return {"message": display, "guessed_letters": guessed_letters}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

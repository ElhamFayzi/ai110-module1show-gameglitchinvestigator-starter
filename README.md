# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.

It's a number guessing game built with Streamlit. The player tries to guess a secret number within a limited number of attempts, using a GUI with an input field, a message area for hints ("go higher"/"go lower"), and "Submit Guess" / "New Game" buttons, plus a "Show hint" checkbox.

- [ ] Detail which bugs you found.

Reversed hints: guessing a number lower than the secret returned "go lower" instead of "go higher," because input was compared as a string rather than an integer.
Broken reset: clicking "New Game" after winning generated a new secret number but didn't reset the game state, so it stayed stuck on "You already won. Start a new game to play again."
Attempts counter: an incorrect first guess didn't decrement the attempts remaining.

- [ ] Explain what fixes you applied.

Fixed the hint logic by converting the guess to an integer so comparisons were numeric, restoring correct "Too Low"/"Too High" direction.
Properly reset the session state on "New Game" so the win flag cleared and new guesses were accepted.
Corrected the attempts counter so it decrements immediately on a wrong guess (verified by test_first_wrong_guess_decrements_attempts_left, watching it drop from 8 to 7). I also extracted the core logic into check_guess so it could be tested in isolation, and confirmed all 8 pytest tests passed.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Open the app. You see the title and a sidebar with Difficulty settings.
2. Pick a difficulty. This sets the number range and attempt limit.
3. A banner shows the range and your current Attempts left.
4. Type a guess and click Submit Guess.
5. Invalid input shows an error and doesn't cost an attempt.
6. A valid guess is counted first, then checked.
7. A hint tells you Too High or Too Low.
8. Guess correctly and you win instantly, and the program display balloons and final score. Game stops.
9. Run out of attempts and the game ends right at zero.
10. Once over, further guesses are ignored.
11. Click New Game to fully reset and start fresh.
12. Expand Developer Debug Info anytime to see the secret and state.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
plugins: anyio-4.14.0
collected 8 items                                                                                                                                                

tests/test_game_logic.py::test_winning_guess PASSED                                                                                                        [ 12%]
tests/test_game_logic.py::test_guess_too_high PASSED                                                                                                       [ 25%]
tests/test_game_logic.py::test_guess_too_low PASSED                                                                                                        [ 37%]
tests/test_game_logic.py::test_first_wrong_guess_decrements_attempts_left PASSED                                                                           [ 50%]
tests/test_game_logic.py::test_attempts_left_is_never_stale PASSED                                                                                         [ 62%]
tests/test_game_logic.py::test_game_ends_exactly_when_attempts_reach_zero PASSED                                                                           [ 75%]
tests/test_game_logic.py::test_no_extra_attempt_after_game_over PASSED                                                                                     [ 87%]
tests/test_game_logic.py::test_game_still_playing_with_one_attempt_left PASSED                                                                             [100%]

======================================================================= 8 passed in 0.02s ========================================================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]

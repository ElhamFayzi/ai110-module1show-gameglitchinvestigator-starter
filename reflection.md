# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
When I first ran the game, the GUI displayed a number guessing interface with an input field for guesses, a message area for hints, and buttons such as “Submit Guess” and “New Game”, and a checkbox "Show hint". The game appeared functional at first glance, but several bugs became apparent during use.
- List at least two concrete bugs you noticed at the start  (for example: "the hints were backwards").
First, the hint system was incorrect—for example, when I guessed a number lower than the secret number, the game sometimes responded with “go lower” instead of “go higher.” Second, after winning and clicking the “New Game” button, the game generated a new secret number but did not properly reset the game state, which prevented further guesses and continued to display the message “You already won. Start a new game to play again.”

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 23 | Should display "go higher" | Displays "go lower" | "go lower" |
| Click "New Game" after winning, then enter a new guess | Game should reset, accept new guesses, and respond based on new secret number  | Game starts a new game, but does not accept guesses and remains in win state | "You already won. Start a new game to play again." |
| An incorrect first guess (e.g., guess 10 when secret is 24) | Attempts remaining should decrease by 1 after the guess (7 - 1 = 6 attempts left) | Attempts do not decrease after an incorrect first guess | Attempts left: 7 |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
One example of an AI suggestion that was correct involved the bug in the hint system. Claude suggested that the comparison logic for the guesses were reversed, and that input was being converted to a string, which would cause the program to perform string comparisons with the secret number instead of integer comparisons. I reviewed the specified portion of the code, and the suggestion appeared to be logical and correct. After applying the fix, the hint system functioned as expected.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
One misleading suggestion involved the fix for the attempts counter bug. Claude suggested updating the “Attempts left” display after the submit logic so it would reflect the most recent guess. While this fixed the first issue, it introduced a new bug where the game-over condition triggered one step late which would allow an extra guess after attempts reached zero. I verified this by testing multiple runs and observing that the game only ended after an additional guess beyond zero attempts.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I decided a bug was fixed by re-running the program and testing the same scenarios that originally caused the issue. If the program consistently produced the expected behavior without introducing new errors, I considered the bug resolved.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
I ran the pytest suite with python -m pytest tests/test_game_logic.py -v, and all 8 tests passed. The most useful one was test_first_wrong_guess_decrements_attempts_left, which simulates a single wrong guess and asserts that "attempts left" drops from 8 to 7 right away. This directly targeted the counter bug I'd logged earlier, where the first wrong guess didn't register. I also ran test_guess_too_low and test_guess_too_high, which verified the hint direction was no longer reversed (guessing 40 against a secret of 50 correctly returns "Too Low").
- Did AI help you design or understand any tests? How?
Yes—Claude helped me design the regression tests by suggesting I extract the pure game logic into check_guess so it could be tested in isolation
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Every time you interact with a Streamlit app—like clicking a button or typing a guess—Streamlit re-runs the entire script from top to bottom, so any normal variable resets to its starting value.
Session state is a special storage box that survives those reruns, which is how the game remembers things like the secret number, score, and attempts left between clicks.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  One strategy I want to reuse is asking AI to explain why its suggested fix works before applying it, since that helped me catch a case where Claude's fix introduced a new bug
- What is one thing you would do differently next time you work with AI on a coding task?
Next time I would test each AI-suggested fix in isolation before moving on, instead of applying several changes at once.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
This project taught me that AI-generated code can look correct and still be wrong, so I now treat every suggestion as a draft to verify and test instead of an answer.

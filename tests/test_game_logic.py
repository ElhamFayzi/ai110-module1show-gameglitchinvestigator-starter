from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# ---------------------------------------------------------------------------
# Regression tests for the two bugs fixed in app.py's submit flow.
#
# That logic lives inline inside the Streamlit script and can't be imported
# without executing the UI, so play_round() below mirrors the *corrected*
# submit flow. These tests pin down the contract the fixes established:
#   Bug 1 - "Attempts left" was rendered before the counter was incremented,
#           so it lagged one guess behind (looked like the guess didn't count).
#   Bug 2 - the game-over screen only halted play on the *next* interaction,
#           so one extra guess was accepted after attempts left hit 0.
# ---------------------------------------------------------------------------

def play_round(attempt_limit, num_wrong_guesses):
    """Replay app.py's fixed submit flow for a run of wrong guesses.

    Returns (displayed_attempts_left, status, guesses_processed) where
    displayed_attempts_left is the value shown to the player after each
    processed guess.
    """
    attempts = 0
    status = "playing"
    displayed_attempts_left = []
    guesses_processed = 0

    for _ in range(num_wrong_guesses):
        # Once the game is over the input is gone, so further submits are
        # ignored rather than counted (Bug 2 fix).
        if status != "playing":
            break

        attempts += 1
        guesses_processed += 1

        # The out-of-attempts check fires on this same guess (Bug 2 fix).
        if attempts >= attempt_limit:
            status = "lost"

        # "Attempts left" is read after the counter is updated (Bug 1 fix).
        displayed_attempts_left.append(attempt_limit - attempts)

    return displayed_attempts_left, status, guesses_processed


def test_attempts_left_updates_on_first_guess():
    # Bug 1: after the very first guess with an 8-attempt limit, the player
    # must see 7 left -- not a stale 8.
    displayed, _, _ = play_round(attempt_limit=8, num_wrong_guesses=1)
    assert displayed[0] == 7


def test_attempts_left_never_lags_behind():
    # Bug 1: the displayed count decreases by exactly one per guess.
    displayed, _, _ = play_round(attempt_limit=8, num_wrong_guesses=4)
    assert displayed == [7, 6, 5, 4]


def test_game_not_over_while_one_attempt_remains():
    # Bug 2: with one attempt left the game is still playable.
    displayed, status, _ = play_round(attempt_limit=5, num_wrong_guesses=4)
    assert status == "playing"
    assert displayed[-1] == 1


def test_game_over_exactly_when_attempts_reach_zero():
    # Bug 2: the game ends on the guess that brings attempts left to 0.
    displayed, status, _ = play_round(attempt_limit=5, num_wrong_guesses=5)
    assert status == "lost"
    assert displayed[-1] == 0


def test_no_extra_attempt_after_game_over():
    # Bug 2: even if the player tries more guesses, only `attempt_limit`
    # guesses are ever processed -- no free extra attempt past 0.
    _, status, guesses_processed = play_round(attempt_limit=5, num_wrong_guesses=10)
    assert status == "lost"
    assert guesses_processed == 5

from logic_utils import check_guess


# check_guess was refactored into logic_utils.py and now returns a
# (outcome, message) tuple, so we unpack the outcome here.
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _message = check_guess(40, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# Regression tests for the two bugs fixed in app.py's game flow.
#
# Both bugs lived in app.py's Streamlit orchestration rather than in a single
# logic_utils function, so we model the *fixed* per-guess rules here and drive
# them with the refactored logic_utils.check_guess. The simulation mirrors the
# corrected app.py: count the attempt first, then derive attempts-left and the
# game-over decision from that updated count.
# ---------------------------------------------------------------------------

def simulate_game(secret, guesses, attempt_limit):
    """Replay a sequence of guesses using the fixed game rules.

    Returns a dict capturing the final state plus the attempts-left value
    recorded immediately after each processed guess.
    """
    attempts = 0
    status = "playing"
    remaining_after_each = []

    for guess in guesses:
        # Once the game is over no further guess may be processed.
        if status != "playing":
            break

        outcome, _message = check_guess(guess, secret)
        attempts += 1  # the guess is counted before we read any counter

        remaining = attempt_limit - attempts
        remaining_after_each.append(remaining)

        if outcome == "Win":
            status = "won"
        elif attempts >= attempt_limit:  # game over the moment 0 remain
            status = "lost"

    return {
        "attempts": attempts,
        "status": status,
        "remaining_after_each": remaining_after_each,
    }


def test_first_wrong_guess_decrements_attempts_left():
    # FIX: the very first wrong guess used to leave "Attempts left"
    # unchanged, as if it never registered. After the fix the first counted
    # guess must immediately drop the remaining count by one.
    result = simulate_game(secret=50, guesses=[10], attempt_limit=8)

    assert result["attempts"] == 1
    # Was 8 (stale) before the fix; must now be 7.
    assert result["remaining_after_each"][0] == 7


def test_attempts_left_is_never_stale():
    # FIX, generalized: after N counted guesses, attempts-left must equal
    # limit - N for every guess, never lagging a step behind.
    limit = 5
    wrong_guesses = [1, 2, 3]  # all below the secret, none win
    result = simulate_game(secret=50, guesses=wrong_guesses, attempt_limit=limit)

    assert result["remaining_after_each"] == [4, 3, 2]


def test_game_ends_exactly_when_attempts_reach_zero():
    # FIX: the game must be over the instant attempts-left hits 0, i.e.
    # after exactly `attempt_limit` wrong guesses -- not one attempt later.
    limit = 5
    wrong_guesses = [1, 2, 3, 4, 6]  # 5 wrong guesses, none equal the secret
    result = simulate_game(secret=50, guesses=wrong_guesses, attempt_limit=limit)

    assert result["attempts"] == limit
    assert result["remaining_after_each"][-1] == 0
    assert result["status"] == "lost"


def test_no_extra_attempt_after_game_over():
    # FIX, the symptom: an extra guess offered past 0 remaining must be
    # ignored. Feeding limit + 1 guesses must still stop at exactly `limit`.
    limit = 5
    six_guesses = [1, 2, 3, 4, 6, 7]
    result = simulate_game(secret=50, guesses=six_guesses, attempt_limit=limit)

    assert result["attempts"] == limit  # the 6th guess never gets counted
    assert result["status"] == "lost"


def test_game_still_playing_with_one_attempt_left():
    # Boundary: with one attempt remaining the game must NOT be over yet.
    limit = 5
    four_guesses = [1, 2, 3, 4]
    result = simulate_game(secret=50, guesses=four_guesses, attempt_limit=limit)

    assert result["status"] == "playing"
    assert result["remaining_after_each"][-1] == 1

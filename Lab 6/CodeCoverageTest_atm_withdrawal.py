import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup

# Example test cases:
def test_simple_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000

def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


# ---------- withdraw ----------
def test_unknown_account():
    with pytest.raises(ValueError):
        withdraw(1000, 100, "fixed", True)

def test_invalid_amount_zero():
    with pytest.raises(ValueError):
        withdraw(1000, 0, "savings", True)

def test_limit_exceeded():
    assert withdraw(100000, 25100, "savings", True) == "limit exceeded"

def test_other_bank_high_fee():
    # fee = 20 + 10 = 30
    assert withdraw(20000, 10100, "savings", False) == 9870

def test_insufficient_funds():
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"


# ---------- pin_check ----------
def test_pin_blocked_after_3_attempts():
    assert pin_check(1111, 1234, 3) == "card blocked"

def test_pin_blocked_on_third_wrong():
    assert pin_check(1111, 1234, 2) == "card blocked"

def test_pin_retry():
    assert pin_check(1111, 1234, 0) == "retry"


# ---------- note_breakup ----------
def test_note_breakup_invalid():
    with pytest.raises(ValueError):
        note_breakup(150)

def test_note_breakup_with_200s():
    assert note_breakup(700) == (1, 1, 0)

def test_note_breakup_without_200s():
    assert note_breakup(600) == (1, 0, 1)
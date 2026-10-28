import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup

# Example test cases:
def test_simple_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000

def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


# ---------- withdraw: validation ----------
def test_unknown_account():
    with pytest.raises(ValueError):
        withdraw(1000, 100, "fixed", True)

def test_amount_zero():
    with pytest.raises(ValueError):
        withdraw(1000, 0, "savings", True)

def test_amount_negative():
    with pytest.raises(ValueError):
        withdraw(1000, -100, "savings", True)

def test_amount_not_multiple_of_100():
    with pytest.raises(ValueError):
        withdraw(1000, 150, "savings", True)


# ---------- withdraw: daily limit ----------
def test_limit_exceeded_savings():
    assert withdraw(100000, 25100, "savings", True) == "limit exceeded"

def test_limit_exceeded_current():
    assert withdraw(100000, 50100, "current", True) == "limit exceeded"

def test_exactly_at_savings_limit():
    assert withdraw(100000, 25000, "savings", True) == 75000

def test_exactly_at_current_limit():
    assert withdraw(100000, 50000, "current", True) == 50000


# ---------- withdraw: fees ----------
def test_own_bank_no_fee():
    assert withdraw(5000, 1000, "savings", True) == 4000

def test_other_bank_low_fee():
    assert withdraw(5000, 1000, "savings", False) == 3980

def test_other_bank_exactly_10000_no_extra_fee():
    assert withdraw(20000, 10000, "savings", False) == 9980

def test_other_bank_high_fee():
    assert withdraw(20000, 10100, "savings", False) == 9870


# ---------- withdraw: balance check ----------
def test_insufficient_funds():
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"

def test_insufficient_due_to_fee():
    assert withdraw(1010, 1000, "savings", False) == "insufficient funds"

def test_balance_exactly_equals_amount_plus_fee():
    assert withdraw(1020, 1000, "savings", False) == 0


# ---------- pin_check ----------
def test_pin_blocked_attempts_3():
    assert pin_check(1111, 1234, 3) == "card blocked"

def test_pin_blocked_attempts_above_3_even_if_correct():
    assert pin_check(1234, 1234, 5) == "card blocked"

def test_pin_ok_on_last_allowed_attempt():
    assert pin_check(1234, 1234, 2) == "ok"

def test_pin_wrong_attempt_2_blocks():
    assert pin_check(1111, 1234, 2) == "card blocked"

def test_pin_wrong_attempt_0_retry():
    assert pin_check(1111, 1234, 0) == "retry"

def test_pin_wrong_attempt_1_retry():
    assert pin_check(1111, 1234, 1) == "retry"


# ---------- note_breakup ----------
def test_note_breakup_invalid():
    with pytest.raises(ValueError):
        note_breakup(150)

def test_note_breakup_zero():
    assert note_breakup(0) == (0, 0, 0)

def test_note_breakup_only_100s():
    assert note_breakup(100) == (0, 0, 1)

def test_note_breakup_remaining_100_no_200s():
    assert note_breakup(600) == (1, 0, 1)

def test_note_breakup_exactly_one_200():
    assert note_breakup(700) == (1, 1, 0)

def test_note_breakup_two_200s():
    assert note_breakup(900) == (1, 2, 0)

def test_note_breakup_200_and_100():
    assert note_breakup(800) == (1, 1, 1)

def test_note_breakup_only_500s():
    assert note_breakup(1000) == (2, 0, 0)
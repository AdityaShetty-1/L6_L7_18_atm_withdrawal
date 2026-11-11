def notes_needed(amount):
    """Return how many 100-notes are needed, or None for invalid input."""
    if not isinstance(amount, str):
        return None
    try:
        value = int(amount.replace(',', '').strip())
    except ValueError:
        return None
    if value < 0:
        return None
    return value // 100


def mask_card(card_number):
    """Mask a 4-group card number, or return None for invalid input."""
    if not isinstance(card_number, str):
        return None
    groups = card_number.split()
    if len(groups) != 4:
        return None
    last = groups[3]
    if len(last) != 4 or not last.isascii() or not last.isdigit():
        return None
    return "XXXX XXXX XXXX " + last


def average_withdrawal(amounts_csv):
    """Return the average of CSV amounts, or None for invalid input."""
    if not isinstance(amounts_csv, str):
        return None
    try:
        amounts = [int(a.strip()) for a in amounts_csv.split(',')]
    except ValueError:
        return None
    if not amounts or any(a < 0 for a in amounts):
        return None
    return sum(amounts) // len(amounts)


def main():
    print("==== Running notes_needed ====")
    user_input = input("Enter an amount (e.g. 2,500): ")
    result = notes_needed(user_input)
    print("Number of 100 Notes:", result if result is not None else "Invalid input")

    print("\n==== Running mask_card ====")
    user_input = input("Enter a card number (e.g. 1234 5678 9012 3456): ")
    result = mask_card(user_input)
    print("Masked Card:", result if result is not None else "Invalid card number")

    print("\n==== Running average_withdrawal ====")
    user_input = input("Enter withdrawals as CSV (e.g. 500,1000,2000): ")
    result = average_withdrawal(user_input)
    print("Average Withdrawal:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()

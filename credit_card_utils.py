import re
from datetime import datetime


def normalize_card_number(card_number: str) -> str:
    return re.sub(r"[\s-]", "", card_number.strip())


def luhn_check(card_number: str) -> bool:
    if not card_number.isdigit():
        return False

    total = 0
    reverse_digits = card_number[::-1]

    for i, digit_char in enumerate(reverse_digits):
        digit = int(digit_char)

        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9

        total += digit

    return total % 10 == 0


def detect_card_type(card_number: str) -> str | None:
    if not card_number.isdigit():
        return None

    # Visa: starts with 4
    if card_number.startswith("4"):
        return "Visa"

    # Mastercard: starts with 51-55 or 2221-2720
    if len(card_number) >= 2:
        first_two = int(card_number[:2])
        if 51 <= first_two <= 55:
            return "Mastercard"

    if len(card_number) >= 4:
        first_four = int(card_number[:4])
        if 2221 <= first_four <= 2720:
            return "Mastercard"

    # American Express: starts with 34 or 37
    if card_number.startswith("34") or card_number.startswith("37"):
        return "American Express"

    return None


def parse_expiration(expiration: str):
    expiration = expiration.strip()

    match_short = re.fullmatch(r"(0[1-9]|1[0-2])/(\d{2})", expiration)
    if match_short:
        month = int(match_short.group(1))
        year = 2000 + int(match_short.group(2))
        return month, year

    match_long = re.fullmatch(r"(0[1-9]|1[0-2])/(\d{4})", expiration)
    if match_long:
        month = int(match_long.group(1))
        year = int(match_long.group(2))
        return month, year

    return None, None


def expiration_not_expired(expiration: str) -> bool:
    month, year = parse_expiration(expiration)
    if month is None or year is None:
        return False

    now = datetime.now()
    current_year = now.year
    current_month = now.month

    return (year > current_year) or (year == current_year and month >= current_month)


def validate_cvc(card_type: str, cvc: str) -> bool:
    cvc = cvc.strip()

    if not cvc.isdigit():
        return False

    if card_type == "American Express":
        return len(cvc) == 4

    if card_type in ("Visa", "Mastercard"):
        return len(cvc) == 3

    return False


def validate_credit_card(cardholder: str, card_number: str, expiration: str, cvc: str):
    """
    Returns:
        (is_valid: bool, message: str, normalized_number: str, card_type: str | None)
    """
    cardholder = cardholder.strip()
    normalized_number = normalize_card_number(card_number)

    if not cardholder:
        return False, "Cardholder name is required.", "", None

    if not normalized_number:
        return False, "Card number is required.", "", None

    if not normalized_number.isdigit():
        return False, "Card number must contain only digits, spaces, or dashes.", "", None

    card_type = detect_card_type(normalized_number)
    if card_type is None:
        return False, "Unsupported or invalid card type/length.", normalized_number, None

    # exact supported lengths
    valid_length = (
        (card_type == "Visa" and len(normalized_number) in (13, 16, 19)) or
        (card_type == "Mastercard" and len(normalized_number) == 16) or
        (card_type == "American Express" and len(normalized_number) == 15)
    )

    if not valid_length:
        return False, "Invalid card number length for detected card type.", normalized_number, card_type

    if not luhn_check(normalized_number):
        return False, "Card number failed validation.", normalized_number, card_type

    month, year = parse_expiration(expiration)
    if month is None:
        return False, "Expiration must be MM/YY or MM/YYYY.", normalized_number, card_type

    if not expiration_not_expired(expiration):
        return False, "Card is expired.", normalized_number, card_type

    if not validate_cvc(card_type, cvc):
        if card_type == "American Express":
            return False, "American Express CVC must be 4 digits.", normalized_number, card_type
        return False, f"{card_type} CVC must be 3 digits.", normalized_number, card_type

    return True, "Valid credit card.", normalized_number, card_type
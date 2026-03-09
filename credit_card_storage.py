import json
import uuid
from pathlib import Path
from encryption import encrypt_password

CREDIT_PLAIN_FILE = Path("credit_cards_plain.json")
CREDIT_ENCRYPTED_FILE = Path("credit_cards_encrypted.json")


def _load_json_file(file_path: Path):
    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def _write_json_file(file_path: Path, data):
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_credit_card_record(cardholder: str, card_type: str, card_number: str, expiration: str, cvc: str):
    """
    Saves or updates a card based on normalized card number.
    Returns:
        ("saved" or "updated", record_id)
    """
    plain_records = _load_json_file(CREDIT_PLAIN_FILE)
    encrypted_records = _load_json_file(CREDIT_ENCRYPTED_FILE)

    normalized_number = card_number.strip()

    existing_id = None

    for record in plain_records:
        if record["card_number"].strip() == normalized_number:
            existing_id = record["id"]
            break

    if existing_id is None:
        existing_id = str(uuid.uuid4())
        action = "saved"
    else:
        action = "updated"

    plain_entry = {
        "id": existing_id,
        "cardholder": cardholder.strip(),
        "card_type": card_type,
        "card_number": normalized_number,
        "expiration": expiration.strip(),
        "cvc": cvc.strip()
    }

    encrypted_entry = {
        "id": existing_id,
        "cardholder": cardholder.strip(),
        "card_type": card_type,
        "card_number": encrypt_password(normalized_number),
        "expiration": encrypt_password(expiration.strip()),
        "cvc": encrypt_password(cvc.strip())
    }

    plain_updated = False
    for i, record in enumerate(plain_records):
        if record["id"] == existing_id:
            plain_records[i] = plain_entry
            plain_updated = True
            break
    if not plain_updated:
        plain_records.append(plain_entry)

    encrypted_updated = False
    for i, record in enumerate(encrypted_records):
        if record["id"] == existing_id:
            encrypted_records[i] = encrypted_entry
            encrypted_updated = True
            break
    if not encrypted_updated:
        encrypted_records.append(encrypted_entry)

    _write_json_file(CREDIT_PLAIN_FILE, plain_records)
    _write_json_file(CREDIT_ENCRYPTED_FILE, encrypted_records)

    return action, existing_id
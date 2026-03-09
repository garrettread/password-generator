import json
from pathlib import Path
from encryption import encrypt_password, decrypt_password

PLAIN_FILE = Path("passwords_plain.json")
ENCRYPTED_FILE = Path("passwords_encrypted.json")


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


def save_password_record(website: str, username: str, password: str):
    plain_records = _load_json_file(PLAIN_FILE)
    encrypted_records = _load_json_file(ENCRYPTED_FILE)

    normalized_website = website.strip().lower()
    normalized_username = username.strip().lower()

    plain_entry = {
        "website": website.strip(),
        "username": username.strip(),
        "password": password
    }

    encrypted_entry = {
        "website": website.strip(),
        "username": username.strip(),
        "password": encrypt_password(password)
    }

    was_updated = False

    for i, record in enumerate(plain_records):
        record_website = record["website"].strip().lower()
        record_username = record["username"].strip().lower()

        if record_website == normalized_website and record_username == normalized_username:
            plain_records[i] = plain_entry
            was_updated = True
            break

    if not was_updated:
        plain_records.append(plain_entry)

    encrypted_updated = False
    for i, record in enumerate(encrypted_records):
        record_website = record["website"].strip().lower()
        record_username = record["username"].strip().lower()

        if record_website == normalized_website and record_username == normalized_username:
            encrypted_records[i] = encrypted_entry
            encrypted_updated = True
            break

    if not encrypted_updated:
        encrypted_records.append(encrypted_entry)

    _write_json_file(PLAIN_FILE, plain_records)
    _write_json_file(ENCRYPTED_FILE, encrypted_records)

    if was_updated:
        return "updated"
    return "saved"

def get_plain_records():
    return _load_json_file(PLAIN_FILE)


def get_encrypted_records():
    return _load_json_file(ENCRYPTED_FILE)


def get_saved_websites():
    records = get_plain_records()
    websites = sorted({record["website"] for record in records})
    return websites


def get_usernames_for_website(website: str):
    records = get_plain_records()
    usernames = sorted(
        record["username"] for record in records if record["website"] == website
    )
    return usernames


def get_decrypted_password(website: str, username: str):
    records = get_encrypted_records()

    for record in records:
        if record["website"] == website and record["username"] == username:
            return decrypt_password(record["password"])

    return None

def get_decrypted_password_match(website: str, username: str):
    website = website.strip().lower()
    username = username.strip().lower()

    records = get_encrypted_records()

    for record in records:
        record_website = record["website"].strip().lower()
        record_username = record["username"].strip().lower()

        if record_website == website and record_username == username:
            return decrypt_password(record["password"])

    return None
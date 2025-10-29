# AuthKit — API & Module Reference

This document describes the modules exposed by the `AuthKit` wrapper and the public classes / functions available in each module. It is intended as a quick reference for developers integrating or extending AuthKit.

> Location: `authkit/` (the wrapper class `AuthKit` in `authkit/__init__.py` exposes the main components).

---

## Table of contents
- `authkit` (wrapper)
- `encryption.py` — Encryption utilities
- `storage.py` — File storage and integrity utilities
- `manager.py` — High-level user management (password register / login)
- `oauth.py` — Simple OAuth helper
- `session.py` — Session management
- `twofa.py` — Two-factor (TOTP) support

Each section lists public classes and methods, short descriptions, usage examples, and important implementation notes.

---

## `authkit` (wrapper) — `authkit/__init__.py`

Class: `AuthKit`
- `__init__(self)`
  - Convenience wrapper that creates instances of the main components and exposes them as attributes:
    - `self.encryption` -> `Encryption()`
    - `self.storage` -> `Storage()`
    - `self.manager` -> `Manager()`
    - `self.oauth_client` -> `OAuthClient()`
    - `self.twofa` -> `TwoFA()`

Usage:
```python
from authkit import AuthKit
auth = AuthKit()
# then: auth.manager, auth.twofa, auth.storage, auth.encryption, auth.oauth_client
```

Note: the wrapper simply wires the classes together for convenience.

---

## `encryption.py`
Class: `Encryption`
Purpose: provide symmetric encryption (Fernet), end-to-end helper functions, and a password-strength evaluator.

Public methods (as implemented):
- `__init__(self, key=None)`
  - Initialize a Fernet instance with `key`. Current implementation expects `key` to be available and does not generate one automatically.
- `encrypt(self, data)`
  - Encrypts `data` (a str). Returns a base64-like encoded string.
- `decrypt(self, key)`
  - Decrypts an encoded string and returns the plaintext.
- `e2e_encrypt(public_key, message)` (module method style)
  - Uses asymmetric public-key encryption (OAEP) to encrypt `message` for an end-to-end scenario.
- `e2e_decryption(private_key, ciphertext)`
  - Uses RSA private key to decrypt ciphertext.
- `get_password_strength(password)`
  - Returns an integer `total_point` score based on length, character classes, entropy and common patterns. The current thresholds used by the code:
    - `total_point <= 1` -> Weak
    - `total_point == 2-3` -> Moderate
    - `total_point >= 4` -> Strong
  - Entropy influences the score (+1 if entropy >= 50 bits, -1 if entropy <= 28 bits).

Usage examples:
```python
enc = Encryption(key=b"...32-byte-fernet-key...")
cipher = enc.encrypt("secret")
plain = enc.decrypt(cipher)
score = enc.get_password_strength("P@ssw0rd123")
```

Important notes / TODOs:
- `Encryption.__init__` currently assumes a valid key; consider generating and persisting keys if `None`.
- Asymmetric methods expect key objects from `cryptography` library. They are helpers, not integrated with `Storage`.

---

## `storage.py`
Class: `Storage`
Purpose: read/write JSON-backed user data and provide simple integrity, token and key-pair helpers.

Public methods:
- `__init__(self, filename="user_data.json")`
  - Ensures the file exists and sets `self.filename`.
- `read(self)` -> dict
  - Load JSON and return a Python dictionary.
- `write(self, data)`
  - Write the `data` dict back to the file (pretty-printed).
- `generate_key_pair(username)`
  - Generate RSA key pair, serialize to PEM, and store them under `data[username]`. Returns the public PEM bytes.
- `calculate_hash(self, data)`
  - Return a SHA-256 hex digest of `data` (JSON serialized with sorted keys).
- `verify_hash(self, data, expected_hash)`
  - Compare the calculated hash to `expected_hash`.
- `generate_reset_token(self, username)`
  - Create a secure token, store it in `data[username]["reset_token"]`, and return it.
- `verify_reset_token(self, username, to_verify)`
  - Verify the token matches the stored one.

Usage example:
```python
storage = Storage()
data = storage.read()
data['alice'] = {'email':'alice@example.com'}
storage.write(data)

hash = storage.calculate_hash(data)
valid = storage.verify_hash(data, hash)
```

Important notes / TODOs:
- Several methods call `Storage.read()` / `Storage.write()` as class-style calls; prefer `self.read()` / `self.write()` for instance methods.
- `calculate_hash` currently serializes data and computes SHA-256; this is useful for integrity checks.

---

## `manager.py`
Class: `Manager`
Purpose: high-level user operations (register user, get password, login). Relies on `Encryption` and `Storage`.

Public methods:
- `__init__(self, key=None, filename="passwords.json")`
  - Creates an `Encryption` and `Storage` instance and an `OAuthClient`.
- `register_user(self, username, password)`
  - Encrypts the provided `password` and writes it into the storage under `data[username]`.
- `get_password(self, username)`
  - Returns decrypted password for `username` (currently returns a set-like container in code — see notes).
- `login(self, username, password)`
  - Compares the provided password with stored password and returns `True` or `False`.

Usage example:
```python
mgr = Manager(key=..., filename="passwords.json")
mgr.register_user('bob', 'S3cret!')

if mgr.login('bob', 'S3cret!'):
    print('ok')
```

Important notes / TODOs:
- There's a circular/self reference in the implementation (`self.manager = Manager(key, filename)`) which creates recursion. Remove this: the `Manager` should not instantiate itself.
- `register_user` stores `encrypted_password.decode()` but `encrypt()` already returns a string in current `Encryption` — ensure consistent types.
- `get_password` returns a Python `set` with one element; it should return a string (the decrypted password) or structured data.
- `login` currently calls `self.manager.get_password` (recursive) and compares wrongly; this needs correction.

---

## `oauth.py`
Class: `OAuthClient`
Purpose: helper utilities for setting up OAuth providers and obtaining auth URLs and tokens.

Public methods:
- `__init__(self)`
  - Initializes a provider registry: `self.OAuth_providers = {}`.
- `add_provider(self, name, client_id, client_secret, auth_url, token_url, redirect_uri)`
  - Register a provider configuration under `name`.
- `get_auth_url(self, provider_name)`
  - Build an authorization URL with a random `state` and returns it.
- `get_token(self, provider_name, code)`
  - Exchange an authorization `code` for tokens by POSTing to the provider's token endpoint and returning `response.json()`.

Usage example:
```python
oauth = OAuthClient()
oauth.add_provider('github', client_id, client_secret, auth_url, token_url, redirect_uri)
url = oauth.get_auth_url('github')
# after callback -> oauth.get_token('github', code)
```

Notes:
- This module is small, straightforward and returns raw token responses. Add error handling and token storage if you want persistent sessions.

---

## `session.py`
Class: `SessionManager`
Purpose: simple session handling backed by user data storage.

Public methods:
- `__init__(self, database_path="user_data.json")`
  - Current implementation opens the file in append mode and stores the file object in `self.database`, which is problematic. The expected design is to load JSON into a dict (via `Storage`) and persist changes.
- `create_session(self, username)`
  - Generate `uuid4()` session id and store it under `user["session_id"]`.
- `session_valid(self, username, session_id)`
  - Validate that the provided session id matches the stored session id.
- `end_session(self, username)`
  - Remove the stored `session_id` for the user.

Usage (recommended after refactor):
```python
from authkit.storage import Storage
storage = Storage()
session = SessionManager()
session.create_session('alice')
```

Important notes / TODOs:
- The module currently treats `self.database` as a file object; it should load a dict with `Storage.read()` and write back with `Storage.write()`.
- Convert session IDs to strings before storing when persisting to JSON.

---

## `twofa.py`
Class: `TwoFA`
Purpose: generate and verify TOTP-based 2FA secrets using `pyotp` and a Base32 secret generator.

Public methods:
- `__init__(self, filename="user_data.json")` — set data filename.
- `generate_twofa_secret(self, username)`
  - Generate a Base32 secret with `bs32.random_base32()` and store it under `data[username]["2fa_secret"]`.
- `get_twofa_secret(self, username)`
  - Read and return stored secret.
- `generate_twofa_token(self, username)`
  - Return current TOTP code for the user's secret.
- `twofa_verified(self, username, token)`
  - Verify a supplied TOTP `token` for that user and return boolean.

Usage example:
```python
twofa = TwoFA()
secret = twofa.generate_twofa_secret('alice')
code = twofa.generate_twofa_token('alice')
valid = twofa.twofa_verified('alice', code)
```

Important notes / TODOs:
- `generate_twofa_secret` currently opens the JSON file in append mode (`"a"`) before loading JSON — this will fail. Use `Storage`'s `read`/`write` or open in read/write mode and handle empty file.
- Consider persisting the 2FA secret encrypted (using `Encryption`) instead of plaintext.

---

## Overall recommendations and known issues
This documentation describes the *current* codebase as found in `authkit/`.

High-priority refactors to make the package robust:
- Fix circular/self-instantiation in `Manager`.
- Standardize `Storage` usage across modules. Replace file-object handling with `Storage.read()`/`Storage.write()` and persist changes.
- Make `Encryption` generate or accept a key consistently and document key management (optionally add `save_key()` / `load_key()` helpers).
- Convert session IDs and other stored values to JSON-serializable types (strings), and write changes back to storage.
- Replace string-return error codes (e.g., "User not found") with exceptions or consistent boolean/None return patterns.
- Improve error handling (I/O, JSON decode errors, network errors in OAuth, crypto exceptions).

---

## Where to go from here
- I can convert this API reference into an in-repo `docs/` folder with per-module Markdown files.
- I can implement the recommended refactors (small PRs) to make the library consistent and testable.

If you'd like, I can now create a `docs/` version of this file, add inline usage examples to each module, or open PR-style patches to fix the priority issues listed above. Which would you like next?
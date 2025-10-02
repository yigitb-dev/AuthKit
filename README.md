# AuthKit

## Overview
**AuthKit** is a lightweight, modular, and extensible Python authentication framework designed to simplify user authentication and security in your applications. It provides robust tools for managing passwords, sessions, OAuth integration, and two-factor authentication (2FA), making it ideal for modern application development.

---

## Features
- **Password Management:**
  - Not so securely store and retrieve encrypted passwords.
  - Password strength validation and history tracking.
  - Password expiration support.

- **Two-Factor Authentication (2FA):**
  - Generate and verify time-based one-time passwords (TOTP).
  - Add 2FA secrets to user data for enhanced security.

- **OAuth Integration:**
  - Seamlessly integrate third-party authentication providers like Google, Facebook, and GitHub.

- **Session Management:**
  - Efficiently manage user sessions with built-in tools.

- **Customizable and Extensible:**
  - Modular architecture allows easy extension for custom authentication methods.

- **Audit Logging:**
  - Track authentication events for security and compliance.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yigitb-dev/AuthKit.git
   cd AuthKit
   pip install -r requirements.txt
   ```

## Usage
 - 1. Password Managment
    ```bash
    from authkit.manager import Manager

    manager = Manager(key="your-encryption-key")

    #Add a password
    manager.add_password("example_service", "username", "secure_password")

    #Retrieve a password
    password_data = manager.get_password("example_service")
    print(password_data)
    ```
 - 2. Two-Factor Authentication (2FA)
    ```bash
    from authkit.twofa import TwoFA

    twofa = TwoFA(filename="user_data.json")

    #Generate a 2FA secret for a user
    secret = twofa.generate_2fa_secret("john_doe")
    print(f"2FA Secret: {secret}")
    ```
 - 3. OAuth Integration
    ```bash
    from authkit.oauth import OAuthClient

    oauth = OAuthClient(client_id="your-client-id", client_secret="your-client-secret")
    auth_url = oauth.get_authorization_url()
    print(f"Authorize your app here: {auth_url}")
    ```




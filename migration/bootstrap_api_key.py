#!/usr/bin/env python3
"""
Bootstrap script to create the first API key for Archon.

This script generates a secure bootstrap secret and creates the first
admin API key via the bootstrap endpoint.

Usage:
    python3 bootstrap_api_key.py

Created: 2025-10-15
"""

import json
import os
import secrets
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


def generate_bootstrap_secret():
    """Generate a secure random bootstrap secret."""
    return secrets.token_urlsafe(32)


def create_first_api_key(server_url: str, bootstrap_secret: str, key_name: str):
    """
    Create the first API key using the bootstrap endpoint.

    Args:
        server_url: Archon server URL
        bootstrap_secret: Bootstrap secret for authentication
        key_name: Name for the API key

    Returns:
        Tuple of (success: bool, result: dict)
    """
    try:
        url = f"{server_url}/api/auth/bootstrap"
        payload = {
            "bootstrap_secret": bootstrap_secret,
            "key_name": key_name
        }

        response = requests.post(url, json=payload, timeout=10)

        if response.status_code == 200:
            return True, response.json()
        else:
            try:
                error_data = response.json()
                return False, error_data
            except:
                return False, {"error": f"HTTP {response.status_code}: {response.text}"}

    except requests.exceptions.ConnectionError:
        return False, {"error": "Could not connect to Archon server. Is it running?"}
    except Exception as e:
        return False, {"error": f"Unexpected error: {str(e)}"}


def main():
    """Main bootstrap process."""
    print("=" * 60)
    print("Archon API Key Bootstrap Script")
    print("=" * 60)
    print()

    # Get server URL
    default_url = os.getenv("ARCHON_SERVER_URL", "http://localhost:8181")
    server_url = input(f"Enter Archon server URL [{default_url}]: ").strip() or default_url

    # Check if bootstrap is available
    try:
        status_response = requests.get(f"{server_url}/api/auth/status", timeout=5)
        if status_response.status_code == 200:
            status_data = status_response.json()
            if not status_data.get("bootstrap_available", False):
                print("\nError: Bootstrap is not available.")
                print("API keys already exist in the database.")
                print("Use the regular API key management endpoints instead.")
                sys.exit(1)
        else:
            print(f"\nWarning: Could not check bootstrap status (HTTP {status_response.status_code})")
            proceed = input("Continue anyway? [y/N]: ").strip().lower()
            if proceed != 'y':
                print("Aborted.")
                sys.exit(1)
    except Exception as e:
        print(f"\nWarning: Could not connect to server: {e}")
        proceed = input("Continue anyway? [y/N]: ").strip().lower()
        if proceed != 'y':
            print("Aborted.")
            sys.exit(1)

    # Generate or get bootstrap secret
    print("\nBootstrap Secret:")
    print("-" * 60)
    print("Option 1: Generate a new random secret")
    print("Option 2: Use existing secret from environment (ARCHON_BOOTSTRAP_SECRET)")
    print()

    existing_secret = os.getenv("ARCHON_BOOTSTRAP_SECRET")
    if existing_secret:
        print(f"Found existing secret in environment: {existing_secret[:10]}...")
        use_existing = input("Use existing secret? [Y/n]: ").strip().lower()
        if use_existing != 'n':
            bootstrap_secret = existing_secret
        else:
            bootstrap_secret = generate_bootstrap_secret()
            print(f"Generated new secret: {bootstrap_secret}")
    else:
        bootstrap_secret = generate_bootstrap_secret()
        print(f"Generated new secret: {bootstrap_secret}")
        print("\nIMPORTANT: Add this to your .env file:")
        print(f"ARCHON_BOOTSTRAP_SECRET={bootstrap_secret}")
        print()

    # Get key name
    default_name = "Production Admin Key"
    key_name = input(f"Enter a name for this API key [{default_name}]: ").strip() or default_name

    # Create the API key
    print("\nCreating API key...")
    success, result = create_first_api_key(server_url, bootstrap_secret, key_name)

    if success:
        print("\n" + "=" * 60)
        print("SUCCESS! API Key Created")
        print("=" * 60)
        print()
        print(f"Key Name: {result.get('key_name')}")
        print(f"Key ID: {result.get('key_id')}")
        print()
        print("=" * 60)
        print("YOUR API KEY (save this securely!):")
        print(result.get('api_key'))
        print("=" * 60)
        print()
        print("WARNING: This is the ONLY time you will see this API key!")
        print("Store it securely in your password manager or .env file.")
        print()
        print("Add to your .env file:")
        print(f"ARCHON_API_KEY={result.get('api_key')}")
        print()
        print("Test your API key:")
        print(f"curl -H \"Authorization: Bearer {result.get('api_key')}\" \\")
        print(f"  {server_url}/api/auth/validate")
        print()
    else:
        print("\n" + "=" * 60)
        print("ERROR: Failed to create API key")
        print("=" * 60)
        print()
        print("Error details:")
        print(json.dumps(result, indent=2))
        print()
        print("Common issues:")
        print("1. Bootstrap secret doesn't match ARCHON_BOOTSTRAP_SECRET in .env")
        print("2. API keys already exist (use regular API key endpoints)")
        print("3. Archon server is not running")
        print("4. Database migration not applied")
        print()
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAborted by user.")
        sys.exit(1)

import secrets
import time

def generate_otp():
    return f"{secrets.randbelow(1_000_000):06d}"

def get_otp_expiry():
    return time.time() + 300
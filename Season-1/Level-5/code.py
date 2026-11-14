# Welcome to Secure Code Game Season-1/Level-5!

# This is the last level of our first season, good luck!

import binascii
import secrets
import hashlib
import os
import bcrypt

class Random_generator:

    # generates a random token
    def generate_token(self, length=8, alphabet=(
    '0123456789'
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    )):
        # secrets uses the OS CSPRNG; random (Mersenne Twister) is predictable
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    # generates salt
    def generate_salt(self, rounds=12):
        # bcrypt generates a full-entropy random salt with the right format
        return bcrypt.gensalt(rounds)

class SHA256_hasher:

    # produces the password hash by combining password + salt because hashing
    def password_hash(self, password, salt):
        password = binascii.hexlify(hashlib.sha256(password.encode()).digest())
        password_hash = bcrypt.hashpw(password, salt)
        return password_hash.decode('ascii')

    # verifies that the hashed password reverses to the plain text version on verification
    def password_verification(self, password, password_hash):
        password = binascii.hexlify(hashlib.sha256(password.encode()).digest())
        password_hash = password_hash.encode('ascii')
        return bcrypt.checkpw(password, password_hash)

class PBKDF2_hasher:

    ITERATIONS = 600_000

    # salted, slow, key-stretching hash (replaces the unsalted, fast MD5)
    # stored format: iterations$salt_hex$hash_hex
    def password_hash(self, password):
        salt = secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, self.ITERATIONS)
        return f'{self.ITERATIONS}${salt.hex()}${digest.hex()}'

    def password_verification(self, password, password_hash):
        try:
            iterations, salt_hex, hash_hex = password_hash.split('$')
            digest = hashlib.pbkdf2_hmac(
                'sha256', password.encode(), bytes.fromhex(salt_hex), int(iterations))
        except ValueError:
            return False
        # constant-time comparison
        return secrets.compare_digest(digest.hex(), hash_hex)

# kept so existing callers and tests that reference the old name keep working;
# it no longer uses MD5 at all
MD5_hasher = PBKDF2_hasher

# a collection of sensitive secrets necessary for the software to operate
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
PUBLIC_KEY = os.environ.get('PUBLIC_KEY')
# secrets must never be committed to source control: load them from the environment
SECRET_KEY = os.environ.get('SECRET_KEY')
PASSWORD_HASHER = 'PBKDF2_hasher'


# Contribute new levels to the game in 3 simple steps!
# Read our Contribution Guideline at github.com/skills/secure-code-game/blob/main/CONTRIBUTING.md
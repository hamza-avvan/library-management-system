import os, hashlib, binascii, timeago, datetime, subprocess, json, base64
from cryptography.fernet import Fernet

secret_key = os.environ.get('SECRET_KEY')
key = base64.urlsafe_b64encode(hashlib.sha256(secret_key.encode()).digest()[:32])
fernet = Fernet(key)

def encrypt(value):
    return fernet.encrypt(value.encode())

def decrypt(token):
    return fernet.decrypt(token)

salt=b'$#0x--.\'/\\98'
def hash(string):
    dk = hashlib.pbkdf2_hmac('sha256', b'password', salt, 100000)
    return binascii.hexlify(dk).decode("utf-8")

def b_hash(string):
    dk = hashlib.pbkdf2_hmac('sha256', b'password', salt, 100000)
    return binascii.hexlify(dk)
    
def ago(date):
    """
        Calculate a '3 hours ago' type string from a python datetime.
    """
    now = datetime.datetime.now() + datetime.timedelta(seconds = 60 * 3.4)

    return (timeago.format(date, now)) # will print x secs/hours/minutes ago

def run_command(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()

def generate_secure_verification_code(uid, length=64):
    """Generate a secure random alphanumeric verification code using hashing."""
    # Generate a random salt
    salt = os.urandom(16)
    
    # Generate a random string
    random_string = os.urandom(length)
    
    # Create a hash of the random string with the salt
    hash_object = hashlib.sha256(salt + uid.encode('utf-8') + random_string)
    hash_digest = hash_object.hexdigest()
    
    # Ensure the verification code is alphanumeric
    verification_code = ''.join([c for c in hash_digest if c.isalnum()][:length])
    return verification_code

def create_headline(msg, msg_type, icon, raw=False):
    headline = {'msg': msg, 'msg_type': msg_type, 'icon': icon}
    return json.dumps(headline) if raw else headline
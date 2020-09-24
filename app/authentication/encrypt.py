import hmac
import hashlib
import base64
from config import Config


def get_secret_hash(username):
    msg = username + Config.APP_CLIENT_ID
    dig = hmac.new(str(Config.APP_CLIENT_SECRET).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2

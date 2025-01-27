import secrets
import socket
import string
import urllib.request
from datetime import datetime


def generate_random_key(length=32) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


def get_ipv4_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipV4 = s.getsockname()[0]
    s.close()
    return ipV4


def datetime_now() -> int:
    return int(datetime.now().timestamp())


def download_model_with_urllib(url, output_path):
    try:
        urllib.request.urlretrieve(url, output_path)
        print(f"Model downloaded successfully and saved to {output_path}")
    except Exception as e:
        print(f"Failed to download the model: {e}")

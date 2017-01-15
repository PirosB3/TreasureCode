import sys
from main import PRIVATES

from Crypto.PublicKey import RSA


def run():
    encrypted_message = sys.argv[1]
    key_index = int(sys.argv[2])

    key = RSA.importKey(PRIVATES[key_index])
    print key.decrypt(encrypted_message.decode('hex'))


if __name__ == '__main__':
    run()

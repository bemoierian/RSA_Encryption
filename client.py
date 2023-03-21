import socketio
from utils import Utils

sio = socketio.Client()
port = 5000

# -----------Parameters-----------
p = 524287
q = 6700417
e = 793
n = p * q
phiN = (p - 1) * (q - 1)
print("n = " + str(n))
print("GCD(e, phiN) = " + str(Utils.gcd(e, phiN)))
d = Utils.modInverse(e, phiN)
print("d = " + str(d))
# --------------------------------

@sio.event
def connect():
    print('Connected to server')
    # --------Read message from terminal--------
    data = input()
    # ------------encode and encrypt------------
    encoddedMsg = Utils.encodeMessage(data)
    encyptedMsg = Utils.encryptMessage(encoddedMsg, e,n)
    print('Cipher: ')
    print(*encyptedMsg)
    # ----------Send encrypted message-----------
    sio.emit('chat message', encyptedMsg)

@sio.on('chat message')
def on_message(msg):
    # ---------Receive encrypted message--------
    print('Received: ')
    print(*msg)
    # ------------decrypt and decode------------
    decyptedMsg = Utils.decryptMessage(msg, d,n)
    decodedMsg = Utils.decodeMessage(decyptedMsg)
    print('Decrypted: ')
    print(decodedMsg)

    # --------Read message from terminal--------
    data = input()
    # ------------encode and encrypt------------
    encoddedMsg = Utils.encodeMessage(data)
    encyptedMsg = Utils.encryptMessage(encoddedMsg, e,n)
    print('Cipher: ')
    print(*encyptedMsg)
    # ----------Send encrypted message-----------
    sio.emit('chat message', encyptedMsg)

sio.connect(f'http://localhost:{port}')

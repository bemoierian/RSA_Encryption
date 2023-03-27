import socketio
from utils import Utils

sio = socketio.Client()
port = 5000

# -----------Parameters-----------
# p = 524287
# q = 6700417
# e = 793
# p1 = 588556073069635651905528453169
# q1 = 666749047938382702503498353041
# e1 = 6454649479
p1 = Utils.generate_big_prime(1024)
q1 = Utils.generate_big_prime(1024)
n1 = p1 * q1
phiN = (p1 - 1) * (q1 - 1)
e1 = Utils.generate_e(phiN)
print("n = " + str(n1))
print("GCD(e, phiN) = " + str(Utils.gcd(e1, phiN)))
d = Utils.modInverse(e1, phiN)
print("d = " + str(d))
# --------------------------------
e2 = 0
n2 = 0
@sio.event
def connect():
    print('Connected to server')
    print('Sending my public key to server...')
    sio.emit('public key', [str(i) for i in [e1, n1]])


@sio.on('public key')
def public_key(data):
    global e2, n2
    data = [int(i) for i in data]
    e2 = data[0]
    n2 = data[1]
    print('Received public key of server: e = ', e2," n = ", n2)
    # --------Read message from terminal--------
    print('Send message to server:')
    msg = input()
    # ------------encode and encrypt------------
    encoddedMsg = Utils.encodeMessage(msg)
    encyptedMsg = Utils.encryptMessage(encoddedMsg, e2,n2)
    print('Cipher: ')
    print(*encyptedMsg)
    # ----------Send encrypted message-----------
    sio.emit('chat message', [str(i) for i in encyptedMsg])

@sio.on('chat message')
def on_message(msg):
    # ---------Receive encrypted message--------
    data = [int(i) for i in data]
    print('Received: ')
    print(*msg)
    # ------------decrypt and decode------------
    decyptedMsg = Utils.decryptMessage(msg, d,n1)
    decodedMsg = Utils.decodeMessage(decyptedMsg)
    print('Decrypted: ')
    print(decodedMsg)

    # --------Read message from terminal--------
    data = input()
    # ------------encode and encrypt------------
    encoddedMsg = Utils.encodeMessage(data)
    encyptedMsg = Utils.encryptMessage(encoddedMsg, e1,n1)
    print('Cipher: ')
    print(*encyptedMsg)
    # ----------Send encrypted message-----------
    sio.emit('chat message', [str(i) for i in encyptedMsg])

sio.connect(f'http://localhost:{port}')

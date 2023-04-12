import socketio
import eventlet
from utils import Utils
sio = socketio.Server()

# -----------Parameters-----------
nbits = 256
p1 = Utils.generate_big_prime(nbits)
q1 = Utils.generate_big_prime(nbits)
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


@sio.on('connect')
def connect(sid, environ):
    print('A user connected')


@sio.on('public key')
def public_key(sid, data):
    global e2, n2
    data = [int(i) for i in data]
    e2 = data[0]
    n2 = data[1]
    print('Received public key of client: e = ', e2, " n = ", n2)
    print('Sending my public key to client...')
    sio.emit('public key', [str(i) for i in [e1, n1]])


@sio.on('chat message')
def chat_message(sid, data):
    # ---------Receive encrypted message--------
    data = [int(i) for i in data]
    print('Received: ')
    print(*data)
    # ------------decrypt and decode------------
    decyptedMsg = Utils.decryptMessage(data, d, n1)
    decodedMsg = Utils.decodeMessage(decyptedMsg)
    print('Decrypted: ')
    print(decodedMsg)

    # --------Read message from terminal--------
    print('Send message to client:')
    msg = input()
    # ------------encode and encrypt------------
    encoddedMsg = Utils.encodeMessage(msg)
    encyptedMsg = Utils.encryptMessage(encoddedMsg, e2, n2)
    print('Ciphertext: ')
    print(*encyptedMsg)
    # ----------Send encrypted message-----------
    sio.emit('chat message', [str(i) for i in encyptedMsg])


@sio.on('disconnect')
def disconnect(sid):
    print('User disconnected')


if __name__ == '__main__':
    app = socketio.WSGIApp(sio)
    port = 5000
    eventlet.wsgi.server(eventlet.listen(('localhost', port)), app)
    print(f'listening on :{port}')

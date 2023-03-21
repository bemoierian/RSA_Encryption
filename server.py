import socketio
import eventlet
from utils import Utils
sio = socketio.Server()


p = 524287
q = 6700417
e = 793
n = p * q
phiN = (p - 1) * (q - 1)
print("n = " + str(n))
print("GCD(e, phiN) = " + str(Utils.gcd(e, phiN)))
d = Utils.modInverse(e, phiN)
print("d = " + str(d))


@sio.on('connect')
def connect(sid, environ):
    print('A user connected')


@sio.on('chat message')
def chat_message(sid, data):
    print('Received: ')
    print(*data)
    decyptedMsg = Utils.decryptMessage(data, d,n)
    decodedMsg = Utils.decodeMessage(decyptedMsg)
    print('Decrypted: ')
    print(decodedMsg)

    data = input()
    encoddedMsg = Utils.encodeMessage(data)
    encyptedMsg = Utils.encryptMessage(encoddedMsg, e,n)
    print('Cipher: ')
    print(*encyptedMsg)
    sio.emit('chat message', encyptedMsg)

@sio.on('disconnect')
def disconnect(sid):
    print('User disconnected')


if __name__ == '__main__':
    app = socketio.WSGIApp(sio)
    port = 5000
    eventlet.wsgi.server(eventlet.listen(('localhost', port)), app)
    print(f'listening on :{port}')

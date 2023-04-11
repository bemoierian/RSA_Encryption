# RSA_Encryption

## How to run

1. Install socketio and eventlet:
pip install eventlet socketio

1. Make sure that port 5000 is not currently in use on your machine.

1. Run the server first:
    1. Open new terminal
    1. Run python server.py

1. Run the client:
    1. Open new terminal
    1. Run python client.py

1. Send a message from client by typing the message in the client terminal

> Message will be encrypted and sent to the server

> Server will decrypt the message and it will be displayed in the server terminal

Now, send a message from the server terminal to the client, and so on.

## Choosing number of bits for the key

Open server.py or client.py, change the value of nbits variable to the desired number of bits for p and q, the resulting n will have 2 * nbits, minimum number for nbits is 14.

## How it works

At the beginning of communication, the client sends his public key (e, n) to the server, and server responds by sending its public key (e, n).

Message sent from client to server is encrypted by the public key of the server and vice-versa.

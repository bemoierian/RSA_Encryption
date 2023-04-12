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

## How does it work

At the beginning of communication, the client sends his public key (e, n) to the server, and server responds by sending its public key (e, n).

Message sent from client to server is encrypted by the public key of the server and vice-versa.

## How to attack

1. Open attack.py in your text editor.
1. Change the value of nBits variable to the desired number of bits of p and q.
1. Change the value of plaintext variable to any desired value.
1. Run the file attack.py.

## How does the attack work

The attack is done using plain-ciphertext pairs, by choosing a plaintext, encoding and encrypting it with the public key to get the corresponding ciphertext, then looping on all possible values of the private key, trying to decrypt and decode the ciphertext till it is equal to the chosen plaintext.

## Attack time graph

To plot the graph between number of bits of key and time of attack:

1. Make sure you have matplotlib installed.
1. Run the file attackGraph.py.

> Values written in this file are calculated from attack.py

## Encryption time graph

To plot the graph between number of bits of key and time of encryption:

1. Make sure you have matplotlib installed.
1. Run the file encryptTime.py.

> This script will calculate the encryption time using key sizes (32 -> 1024 bits) for p and q, and it will plot the graph at the end of execution.

## Limitations

Only 1 server and 1 client are supported.

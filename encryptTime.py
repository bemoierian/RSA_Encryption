# this file is used to plot a graph between number of bits and time taken to encrypt a message
from utils import Utils
import time
import matplotlib.pyplot as plt

x = []
y = []
for i in range(32, 1024, 2):
    # append number of bits to x
    x.append(i)
    nBits = i
    print(f"nbits = {nBits}")
    # -----------Parameters-----------
    p = Utils.generate_big_prime(nBits)
    q = Utils.generate_big_prime(nBits)
    n = p * q
    phiN = (p - 1) * (q - 1)
    e = Utils.generate_e(phiN)
    print("n = " + str(n))
    # --------------------------------
    plaintext = "bemoi"
    start = time.time()
    encoddedMsg = Utils.encodeMessage(plaintext)
    cypherText = Utils.encryptMessage(encoddedMsg, e, n)
    end = time.time()
    # append time taken to y
    y.append(end-start)
    print(f"Time taken to encrypt: {end-start}")
# plot graph between x and y
plt.plot(x, y)
plt.xlabel('Number of bits')
plt.ylabel('Time taken (seconds)')
plt.title('Number of bits vs encryption time')
plt.show()

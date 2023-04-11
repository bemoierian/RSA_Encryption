from utils import Utils
import time
import matplotlib.pyplot as plt

x = []
y = []
for i in range(32, 1024, 2):
    x.append(i)
    nBits = i
    print(f"nbits = {nBits}")
    # cypherText = "871998463 1613204058 1941644450 1399719919 2491211954 1816385893 1831371137".split(" ")
    p = Utils.generate_big_prime(nBits)
    q = Utils.generate_big_prime(nBits)
    n = p * q
    phiN = (p - 1) * (q - 1)
    e = Utils.generate_e(phiN)
    print("n = " + str(n))
    plaintext = "bemoi"
    start = time.time()
    encoddedMsg = Utils.encodeMessage(plaintext)
    cypherText = Utils.encryptMessage(encoddedMsg, e, n)
    end = time.time()
    y.append(end-start)
    print(f"Time taken to encrypt: {end-start}")
plt.plot(x, y)
plt.xlabel('Number of bits')
plt.ylabel('Time taken (seconds)')
plt.title('Number of bits vs encryption time')
plt.show()

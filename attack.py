from utils import Utils
import threading
import time
import multiprocessing


def attack(cypherText, plaintext, n, d, threadIndex, stopValue):
    print(f"Starting process {threadIndex}... start index is {d}")
    # global stop_threads
    decyptedMsg = Utils.decryptMessage(cypherText, d, n)
    decodedMsg = Utils.decodeMessage(decyptedMsg)
    # print(decodedMsg)
    # print("Breaking key...")
    while decodedMsg.strip() != plaintext:
        d = d + 1
        decyptedMsg = Utils.decryptMessage(cypherText, d, n)
        decodedMsg = Utils.decodeMessage(decyptedMsg)
        if d % 1000000 == 0:
            print(f"Process {threadIndex}: d = " + str(d))
        # if stop_threads:
        #     return -1
        if d >= stopValue:
            print(f"Process {threadIndex}: Exiting...")
            return 0
    # stop_threads = True
    print(
        f"Process {threadIndex}: Key broken successfully, d = {d}, plaintext = {decodedMsg}")
    # result[threadIndex] = d
    return d


# stop_threads = False
if __name__ == '__main__':
    print("Starting attack...")
    # ----------number of bits of the prime numbers p and q----------
    nBits = 32
    # ---------------------------------------------------------------
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
    encoddedMsg = Utils.encodeMessage(plaintext)
    cypherText = Utils.encryptMessage(encoddedMsg, e, n)
    reald = Utils.modInverse(e, phiN)
    print("Real d = " + str(reald))
    # -----------------multithreading-----------------
    # threadNum = 6
    # start = time.time()
    # for i in range(threadNum):
    #     print(f"Starting thread {i}... start index is {(i*n)//threadNum}")
    #     t = threading.Thread(target=attack, args=(
    #         cypherText, plaintext, n, (i*n)//threadNum, results, i), name=f"Thread-{i}")
    #     threads[i] = t
    #     t.start()
    # for t in threads:
    #     t.join()
    # end = time.time()
    # for result in results:
    #     if result is not None:
    #         print(f"d = {result}")

    # -----------------multiprocessing-----------------
    processesNum = 6
    start = time.time()
    with multiprocessing.Pool(processes=processesNum) as pool:
        results2 = [pool.apply_async(attack, (cypherText, plaintext, n, i*(n//processesNum),  i, (i+1)*(n//processesNum)))
                    for i in range(processesNum)]
        for r in results2:
            if r.get() != 0:
                print("d = " + str(r.get()))
                pool.terminate()
                break
    end = time.time()
    # -------------------sequential---------------------
    # start = time.time()
    # attack(cypherText, plaintext, n, 0, 0, n)
    # end = time.time()

    # -------------------------------------------------
    timeTaken = end - start
    print(f"{nBits} bits | Time taken: " + str(timeTaken) + " seconds")
    print("Exiting...")

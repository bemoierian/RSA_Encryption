from utils import Utils
import threading
import time
# import matplotlib.pyplot as plt
import multiprocessing

# def attack(cypherText, plaintext, n, d, result, index):
#     # global stop_threads
#     stopValue = (index+1)*(n//threadNum)
#     # d = 0
#     decyptedMsg = Utils.decryptMessage(cypherText, d, n)
#     decodedMsg = Utils.decodeMessage(decyptedMsg)
#     # print(decodedMsg)
#     # print("Breaking key...")
#     while decodedMsg.strip() != plaintext:
#         d = d + 1
#         decyptedMsg = Utils.decryptMessage(cypherText, d, n)
#         decodedMsg = Utils.decodeMessage(decyptedMsg)
#         if d % 100000 == 0:
#             print(f"Process {index}: d = " + str(d))
#         # print(decodedMsg)
#         # if stop_threads:
#         #     return -1
#         if d >= stopValue:
#             print(f"Process {index}: Exiting...")
#             return 0
#     # stop_threads = True
#     print(f"Process {index}: Key broken successfully")
#     result[index] = d
#     return d


def attack(cypherText, plaintext, n, d, threadIndex, stopValue):
    print(f"Starting process {threadIndex}... start index is {d}")
    # global stop_threads
    # stopValue = (threadIndex+1)*(n//threadNum)
    # d = 0
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
        # print(decodedMsg)
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
    nBits = 19
    print(f"nbits = {nBits}")
    # cypherText = "871998463 1613204058 1941644450 1399719919 2491211954 1816385893 1831371137".split(" ")
    p = Utils.generate_big_prime(nBits)
    q = Utils.generate_big_prime(nBits)
    n = p * q
    phiN = (p - 1) * (q - 1)
    e = Utils.generate_e(phiN)
    print("n = " + str(n))
    plaintext = "bemoi"
    encoddedMsg = Utils.encodeMessage(plaintext)
    cypherText = Utils.encryptMessage(encoddedMsg, e, n)
    # threadNum = 6
    processesNum = 6
    reald = Utils.modInverse(e, phiN)
    print("Real d = " + str(reald))
    # -----------------multithreading-----------------
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

    x = [28, 32, 34, 36, 38]
    y = [111, 153, 304, 383, 795]
    # plt.plot(x, y)
    # plt.xlabel('Number of bits')
    # plt.ylabel('Time taken (minutes)')
    # plt.title('Number of bits vs attack time')
    # plt.show()
    print("Exiting...")

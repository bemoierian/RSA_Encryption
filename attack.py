from utils import Utils
import threading
import time
# import matplotlib.pyplot as plt
import multiprocessing


def search_list(value, lst):
    for i in range(len(lst)):
        if lst[i] == value:
            print(
                f"Found {value} at index {i} in {threading.current_thread().name}")
            for t in threading.enumerate():
                if t != threading.current_thread():
                    t.kill()
            return i
    return -1


def attack(cypherText, plaintext, n, d, result, index):
    # global stop_threads
    stopValue = (index+1)*(n//threadNum)
    # d = 0
    decyptedMsg = Utils.decryptMessage(cypherText, d, n)
    decodedMsg = Utils.decodeMessage(decyptedMsg)
    # print(decodedMsg)
    # print("Breaking key...")
    while decodedMsg.strip() != plaintext:
        d = d + 1
        decyptedMsg = Utils.decryptMessage(cypherText, d, n)
        decodedMsg = Utils.decodeMessage(decyptedMsg)
        if d % 100000 == 0:
            print(f"Process {index}: d = " + str(d))
        # print(decodedMsg)
        # if stop_threads:
        #     return -1
        if d >= stopValue:
            print(f"Process {index}: Exiting...")
            return 0
    # stop_threads = True
    print(f"Process {index}: Key broken successfully")
    result[index] = d
    return d


plaintext = "hello world"
# -----------------14 bits-----------------
# cypherText = "20923090 26619114 69194545".split(
#     " ")
# d = 6411641
# n = 189467017
# -----------------16 bits-----------------
cypherText = "741850173 1876460621 725561250".split(
    " ")
# d = 6940807
n = 1880353231
threadNum = 6
results = [None] * threadNum
threads = [None] * threadNum
# stop_threads = False
if __name__ == '__main__':
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
    with multiprocessing.Pool(processes=threadNum) as pool:
        results2 = [pool.apply_async(attack, (cypherText, plaintext, n, i*(n//threadNum), results, i))
                    for i in range(threadNum)]
        for r in results2:
            if r.get() != 0:
                print("d = " + str(r.get()))
                pool.terminate()
                break
    end = time.time()

    # -------------------------------------------------
    timeTaken = end - start
    print("14 bits | Time taken: " + str(timeTaken) + " seconds")

    x = [14, 16, 32, 64, 128, 256, 512, 1024]
    y = [111, 153]
    # plt.plot(x, y)
    # plt.xlabel('Number of bits')
    # plt.ylabel('Time taken (minutes)')
    # plt.title('Number of bits vs attack time')
    # plt.show()
    print("Exiting...")

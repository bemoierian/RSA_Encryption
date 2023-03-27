from utils import Utils
import threading
import time
# import matplotlib.pyplot as plt


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
    global stop_threads
    stopValue = (index+1)*n//threadNum
    # d = 0
    decyptedMsg = Utils.decryptMessage(cypherText, d, n)
    decodedMsg = Utils.decodeMessage(decyptedMsg)
    # print(decodedMsg)
    # print("Breaking key...")
    while decodedMsg.strip() != plaintext:
        decyptedMsg = Utils.decryptMessage(cypherText, d, n)
        decodedMsg = Utils.decodeMessage(decyptedMsg)
        d = d + 1
        if d % 100000 == 0:
            print(f"Thread {index}: d = " + str(d))
        # print(decodedMsg)
        if stop_threads:
            return
        if d >= stopValue:
            print(f"Thread {index}: Exiting...")
            return
    stop_threads = True
    print(f"Thread {index}: Key broken successfully")
    result[index] = d
    # for t in threading.enumerate():
    #     if t != threading.current_thread():
    #         t.kill()
    return


x = [16, 32, 64, 128, 256, 512, 1024]
y = [0] * len(x)
plaintext = "sell my car and send me the money"
cypherText = "68479362 1461920952 188394573 280028037 59633811 482136648 1034574609".split(
    " ")
# d = 711266447
#     737376275
n = 1474752551
threadNum = 12
results = [None] * threadNum
threads = [None] * threadNum
stop_threads = False
start = time.time()
for i in range(threadNum):
    print(f"Starting thread {i}... start index is {(i*n)//threadNum}")
    t = threading.Thread(target=attack, args=(
        cypherText, plaintext, n, (i*n)//threadNum, results, i), name=f"Thread-{i}")
    threads[i] = t
    t.start()
for t in threads:
    t.join()
end = time.time()
timeTaken = end - start
y[0] = timeTaken
print(f"16 bits | Time taken: {timeTaken} seconds")
for result in results:
    if result is not None:
        print(f"d = {result}")
# plt.plot(x, y)
# plt.xlabel('Number of bits')
# plt.ylabel('Time taken (minutes)')
# plt.title('Number of bits vs attack time')
# plt.show()
print("Exiting...")

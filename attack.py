from utils import Utils

plaintext = "sell my car and send me the money"
cypherText = "3017265859387 3417161524766 2145086968952 398386476758 2803886902498 781767734858 3264336417785".split(" ")
p = 524287
q = 6700417
n = p * q
d = 2294703607500
# 2294703617833
decyptedMsg = Utils.decryptMessage(cypherText, 2294703617500,n)
decodedMsg = Utils.decodeMessage(decyptedMsg)
print(decodedMsg)
print("Breaking key...")
while decodedMsg.strip() != plaintext:
    decyptedMsg = Utils.decryptMessage(cypherText, d,n)
    decodedMsg = Utils.decodeMessage(decyptedMsg)
    d = d + 1
    print("d = " + str(d))
    # print(decodedMsg)
print("Key broken successfully")
print("d = " + str(d))
print("Exiting...")
    
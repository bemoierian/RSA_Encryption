import re
class Utils:
    @staticmethod
    def replaceText(text):
        return re.sub(r'[^a-z0-9 ]', ' ', text)
    
    # Split given text to arrays of blocks, each block of size 5
    @staticmethod
    def splitText(text):
        blockSize = 5
        splittedRes = []
        for i in range(0, len(text) - blockSize, blockSize):
            splittedRes.append(text[i:i + blockSize])
        remainingPartSize = len(text) - len(splittedRes) * blockSize
        if remainingPartSize > 0:
            remainingPart = text[-remainingPartSize:]
            remainingPart += " " * (blockSize - remainingPartSize)
            splittedRes.append(remainingPart)
        # print("Text split result: " + str(splittedRes))
        return splittedRes

    # Get character mapping for each character
    # a=10, b=11, etc.
    @staticmethod
    def getCharMapping(char):
        if char == ' ':
            # print("Char mapping result: " + str(36))
            return 36
        mapping = int(char) if char.isdigit() else ord(char) - ord('a') + 10
        # print("Char mapping result: " + str(mapping))
        return mapping
    
    # Encode blocks of 5 character using the equation Σ(Ci*37^i)
    @staticmethod
    def encodeBlock(s):
        n = 37
        sum = 0
        for i in range(len(s)):
            mapping = Utils.getCharMapping(s[i])
            # print(f"{mapping} * (n ** {len(s) - i - 1})")
            sum += mapping * (n ** (len(s) - i - 1))
        # print("Encode block result: " + str(sum))
        return sum
    
    @staticmethod
    def encodeMessage(msg):
        splitted_msg = Utils.splitText(msg)
        encoded_msg = []
        for i in range(len(splitted_msg)):
            encoded_msg.append(Utils.encodeBlock(splitted_msg[i]))
        return encoded_msg

    @staticmethod
    def encrypt(msg, e,n):
        msg = int(msg)
        return pow(msg, e, n)

    @staticmethod
    def encryptMessage(encoded_msg, e, n):
        encrypted_msg = []
        for i in range(len(encoded_msg)):
            encrypted_msg.append(Utils.encrypt(encoded_msg[i], e, n))
        return encrypted_msg

    @staticmethod
    def decrypt(cipher, d,n):
        cipher = int(cipher)
        return pow(cipher, d, n)

    @staticmethod
    def decryptMessage(splitted_cipher, d,n):
        decrypted_msg = []
        for i in range(len(splitted_cipher)):
            decrypted_msg.append(Utils.decrypt(splitted_cipher[i], d,n))
        return decrypted_msg
    # Get character from its mapping
    # 10=a, 11=b, etc.
    @staticmethod
    def restoreChar(mapping):
        mapping = int(mapping)
        if mapping < 10:
            return mapping
        if mapping == 36:
            # print("Restore char result:" + ' ')
            return ' '
        char = chr(mapping + ord('a') - 10)
        # print("Restore char result:" + char)
        return char
    
    @staticmethod
    def decodeBlock(num):
        n = 37
        s = []
        for i in range(5):
            char = num % n
            # print("Decoding before parse: " + str(char))
            # print("Decoding parseint: " + str(int(char)))
            char = Utils.restoreChar(int(char))
            s.append(char)
            num = num // n
        s.reverse()
        try:
            result = ''.join(s)
        except:
            return ""
        # print("Decoding result: " + result)
        return result

    @staticmethod
    def decodeMessage(splittedMsg):
        decodedMsg = []
        for i in range(len(splittedMsg)):
            decodedMsg.append(Utils.decodeBlock(splittedMsg[i]))
        return ''.join(decodedMsg)

    @staticmethod
    def gcd(a, b):
        if b == 0:
            return a
        return Utils.gcd(b, a % b)

    @staticmethod
    def modInverse(a, n):
        t = 0
        newT = 1
        r = n
        newR = a
        while newR != 0:
            quotient = r // newR
            t, newT = newT, t - quotient * newT
            r, newR = newR, r - quotient * newR
        if r > 1:
            raise ValueError(f"{a} is not invertible modulo {n}")
        if t < 0:
            t += n
        return t
# this file contains all the utility functions that are used for RSA encryption and decryption
import re
import random


class Utils:
    # replace all non-alphanumeric characters with space
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

    # uses the above function to encode a given text
    @staticmethod
    def encodeMessage(msg):
        splitted_msg = Utils.splitText(msg)
        encoded_msg = []
        for i in range(len(splitted_msg)):
            encoded_msg.append(Utils.encodeBlock(splitted_msg[i]))
        return encoded_msg

    # encrypts a given block using the equation c = m^e mod n
    @staticmethod
    def encrypt(msg, e, n):
        msg = int(msg)
        return pow(msg, e, n)
    
    # encrypts a given message using the above function
    @staticmethod
    def encryptMessage(encoded_msg, e, n):
        encrypted_msg = []
        for i in range(len(encoded_msg)):
            encrypted_msg.append(Utils.encrypt(encoded_msg[i], e, n))
        return encrypted_msg

    # decrypts a given block using the equation m = c^d mod n
    @staticmethod
    def decrypt(cipher, d, n):
        cipher = int(cipher)
        return pow(cipher, d, n)
    
    # decrypts a given message using the above function
    @staticmethod
    def decryptMessage(splitted_cipher, d, n):
        decrypted_msg = []
        for i in range(len(splitted_cipher)):
            decrypted_msg.append(Utils.decrypt(splitted_cipher[i], d, n))
        return decrypted_msg
    
    # Get character from its mapping
    # 10=a, 11=b, etc.
    @staticmethod
    def restoreChar(mapping):
        mapping = int(mapping)
        if mapping < 10:
            return chr(ord('0') + mapping)
        if mapping == 36:
            # print("Restore char result:" + ' ')
            return ' '
        char = chr(mapping + ord('a') - 10)
        # print("Restore char result:" + char)
        return char

    # Decode blocks of 5 character to their original form
    # this is the inverse of the function encodeBlock
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

    # uses the above function to decode a given text
    @staticmethod
    def decodeMessage(splittedMsg):
        decodedMsg = []
        for i in range(len(splittedMsg)):
            decodedMsg.append(Utils.decodeBlock(splittedMsg[i]))
        return ''.join(decodedMsg)
    
    # calculate the gcd of a and b using Euclid's algorithm
    @staticmethod
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a
    
    # calculate the multiplicative inverse of a modulo n using the extended Euclidean algorithm
    @staticmethod
    def modInverse(a, n):
        x = 0
        y = 1
        r = n
        newR = a
        while newR != 0:
            quotient = r // newR
            x, y = y, x - quotient * y
            r, newR = newR, r - quotient * newR
        if r > 1:
            raise ValueError(f"{a} is not invertible modulo {n}")
        if x < 0:
            x += n
        return x

    # generate a random prime number of [size] bits
    @staticmethod
    def generate_big_prime(size):
        p = random.randrange(2 ** (size - 1), 2 ** size - 1)
        while not Utils.is_prime(p):
            p = random.randrange(2 ** (size - 1), 2 ** size - 1)
        return p

    # generate a random e between 0 and phiN such that gcd(e, phiN) = 1
    @staticmethod
    def generate_e(phiN):
        e = random.randrange(0, phiN)
        while not Utils.gcd(e, phiN) == 1:
            e = random.randrange(0, phiN)
        return e

    # check if a number is prime using the Miller-Rabin primality test
    @staticmethod
    def is_prime(n, k=128):
        if n == 2 or n == 3:
            return True
        if n <= 1 or n % 2 == 0:
            return False

        s = 0
        r = n - 1
        while r & 1 == 0:
            s += 1
            r //= 2

        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, r, n)
            if x != 1 and x != n - 1:
                j = 1
                while j < s and x != n - 1:
                    x = pow(x, 2, n)
                    if x == 1:
                        return False
                    j += 1
                if x != n - 1:
                    return False
        return True

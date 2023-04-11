import matplotlib.pyplot as plt
x = [28,   32,  34,  36,  38, 40,  44]
y = [111, 153, 304, 383, 795, 1458, 1967]
plt.plot(x, y)
plt.xlabel('Number of bits')
plt.ylabel('Time taken (seconds)')
plt.title('Number of bits vs attack time')
plt.show()

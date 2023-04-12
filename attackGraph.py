# this script is used to plot a graph between the number of bits of n and
# the time taken from running the attack
import matplotlib.pyplot as plt
# these values were obtained from running the attack.py script
x = [28,   32,  34,  36,  38, 40,  44]
y = [111, 153, 304, 383, 795, 1458, 1967]
# plot graph between number of bits and time taken
plt.plot(x, y)
plt.xlabel('Number of bits of n')
plt.ylabel('Time taken (seconds)')
plt.title('Number of bits vs attack time')
plt.show()

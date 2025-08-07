import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

df = pd.read_csv('label_distribution.csv', sep = ';')
frequencies = df['frequency'].tolist()
print(frequencies)
#y = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]

plt.plot(frequencies, 'o-r')
plt.show()

counted_frequencies = Counter(frequencies)
print(counted_frequencies)



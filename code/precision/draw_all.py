import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import random

exec(open("algorithms.py").read())

fig=plt.figure(figsize=(8,8))

plt.title("Plot of difference in Brier scores for different levels of noise")
plt.xlabel("Noise (bits)")
plt.ylabel("Difference in Brier score")

plt.plot(example1[0], example1[1], linestyle='-', color='red')
plt.plot(example2[0], example2[1], linestyle='-', color='blue')
plt.plot(example3[0], example3[1], linestyle='-', color='green')

plt.savefig("toy_elbow.png")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import random

exec(open("algorithms.py").read())

fig=plt.figure(figsize=(8,8))

plt.xscale('log')

plt.title("Plot of difference in Brier scores for different levels of noise")
plt.xlabel("Noise (bits)")
plt.ylabel("Difference in Brier score")

plt.plot(lo_round_scores_1[0], lo_round_scores_1[1], linestyle=':', color='red')
plt.plot(lo_round_scores_2[0], lo_round_scores_2[1], linestyle=':', color='blue')
plt.plot(lo_round_scores_3[0], lo_round_scores_3[1], linestyle=':', color='green')
plt.plot(lo_round_scores_4[0], lo_round_scores_4[1], linestyle=':', color='orange')
plt.plot(lo_round_scores_5[0], lo_round_scores_5[1], linestyle=':', color='brown')
plt.plot(lo_round_scores_6[0], lo_round_scores_6[1], linestyle=':', color='purple')

plt.plot(lo_pert_scores_1[0], lo_pert_scores_1[1], linestyle='-', color='red')
plt.plot(lo_pert_scores_2[0], lo_pert_scores_2[1], linestyle='-', color='blue')
plt.plot(lo_pert_scores_3[0], lo_pert_scores_3[1], linestyle='-', color='green')
plt.plot(lo_pert_scores_4[0], lo_pert_scores_4[1], linestyle='-', color='orange')
plt.plot(lo_pert_scores_5[0], lo_pert_scores_5[1], linestyle='-', color='brown')
plt.plot(lo_pert_scores_6[0], lo_pert_scores_6[1], linestyle='-', color='purple')

plt.savefig("comparison.png")

fig=plt.figure(figsize=(8,8))

plt.xscale('log')

plt.title("Plot of difference in Brier scores for different levels of noise")
plt.xlabel("Noise (bits)")
plt.ylabel("Difference in Brier score")

plt.plot(lo_round_scores_6[0], lo_round_scores_6[1], linestyle=':', color='purple')

plt.plot(lo_pert_scores_6[0], lo_pert_scores_6[1], linestyle='-', color='purple')

plt.savefig("bigger_comparison.png")

fig=plt.figure(figsize=(8,8))

xlt.xscale('log')

plt.title("Plot of difference in Brier scores for different levels of noise")
plt.xlabel("Noise (probability)")
plt.ylabel("Difference in Brier score")

plt.plot(p_round_scores_1[0], p_round_scores_1[1], linestyle='-', color='red')
plt.plot(p_round_scores_2[0], p_round_scores_2[1], linestyle='-', color='blue')
plt.plot(p_round_scores_3[0], p_round_scores_3[1], linestyle='-', color='green')
plt.plot(p_round_scores_4[0], p_round_scores_4[1], linestyle='-', color='orange')
plt.plot(p_round_scores_5[0], p_round_scores_5[1], linestyle='-', color='brown')
plt.plot(p_round_scores_6[0], p_round_scores_6[1], linestyle='-', color='purple')

plt.savefig("prob_rounding.png")

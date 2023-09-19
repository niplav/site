import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import random

exec(open('algorithms.py').read())

fig=plt.figure(figsize=(8,8))

plt.xscale('log')

plt.title('Plot log scores for different levels of perturbation')
plt.xlabel('Noise (bits)')
plt.ylabel('Log score')

plt.plot(metaculus_scores[0], metaculus_scores[1], linestyle='-', color='red', label='GJP Surveys')
plt.plot(gjpsurvey_scores[0], gjpsurvey_scores[1], linestyle='-', color='blue', label='GJP Markets')
plt.plot(gjpmarket_scores[0], gjpmarket_scores[1], linestyle='-', color='green', label='Metaculus')
plt.plot(predictionbook_scores[0], predictionbook_scores[1], linestyle='-', color='purple', label='PredictionBook')

plt.bar(1.1941179809570313, -1.2, width=0.02, color='red')
plt.bar(1.5017044067382812, -1.2, width=0.02, color='blue')
plt.bar(1.279558654785156, -1.2, width=0.02, color='green')
plt.bar(1.3198378295898436, -1.2, width=0.02, color='purple')

plt.legend()

plt.savefig('platforms.png')

fig=plt.figure(figsize=(8,8))

plt.xscale('log')

plt.title('Plot log scores for different levels of perturbation')
plt.xlabel('Noise (bits)')
plt.ylabel('Log score')

plt.plot(lo_pert_scores_1[0], lo_pert_scores_1[1], linestyle='-', color='red', label='n=4')
plt.plot(lo_pert_scores_2[0], lo_pert_scores_2[1], linestyle='-', color='blue', label='n=4')
plt.plot(lo_pert_scores_3[0], lo_pert_scores_3[1], linestyle='-', color='green', label='n=4')
plt.plot(lo_pert_scores_4[0], lo_pert_scores_4[1], linestyle='-', color='orange', label='n=100')
plt.plot(lo_pert_scores_5[0], lo_pert_scores_5[1], linestyle='-', color='brown', label='n=100')
plt.plot(lo_pert_scores_6[0], lo_pert_scores_6[1], linestyle='-', color='purple', label='n=2000')

plt.legend()

plt.savefig('noised.png')

fig=plt.figure(figsize=(8,8))

plt.xscale('log')

plt.title('Plot of log scores for different levels of perturbation')
plt.xlabel('Noise (bits)')
plt.ylabel('Log score')

plt.plot(lo_round_scores_1[0], lo_round_scores_1[1], linestyle='-', color='red', label='n=4')
plt.plot(lo_round_scores_2[0], lo_round_scores_2[1], linestyle='-', color='blue', label='n=4')
plt.plot(lo_round_scores_3[0], lo_round_scores_3[1], linestyle='-', color='green', label='n=4')
plt.plot(lo_round_scores_4[0], lo_round_scores_4[1], linestyle='-', color='orange', label='n=100')
plt.plot(lo_round_scores_5[0], lo_round_scores_5[1], linestyle='-', color='brown', label='n=100')
plt.plot(lo_round_scores_6[0], lo_round_scores_6[1], linestyle='-', color='purple', label='n=2000')

plt.legend()

plt.savefig('lo_rounded.png')

fig=plt.figure(figsize=(8,8))

plt.xscale('log')

plt.title('Plot of log scores for different levels of perturbation')
plt.xlabel('Noise (bits)')
plt.ylabel('Log score')

plt.plot(lo_round_scores_6[0], lo_round_scores_6[1], linestyle=':', color='purple')

plt.plot(lo_pert_scores_6[0], lo_pert_scores_6[1], linestyle='-', color='purple')

plt.legend()

plt.savefig('comparison.png')

fig=plt.figure(figsize=(8,8))

plt.xscale('log')

plt.title('Plot of log scores for different levels of perturbation')
plt.xlabel('Noise (probability)')
plt.ylabel('Log score')

plt.plot(p_round_scores_1[0], p_round_scores_1[1], linestyle='-', color='red')
plt.plot(p_round_scores_2[0], p_round_scores_2[1], linestyle='-', color='blue')
plt.plot(p_round_scores_3[0], p_round_scores_3[1], linestyle='-', color='green')
plt.plot(p_round_scores_4[0], p_round_scores_4[1], linestyle='-', color='orange')
plt.plot(p_round_scores_5[0], p_round_scores_5[1], linestyle='-', color='brown')
plt.plot(p_round_scores_6[0], p_round_scores_6[1], linestyle='-', color='purple')

plt.savefig('prob_rounding.png')

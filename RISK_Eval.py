import math
import numpy as np
import matplotlib.pyplot as plt
import RISK_FB_probs as calc_probs
import RISK_SIM_probs as sim_probs
from enum import Enum

# Evaluation and visualization of probs

class Modes(Enum):
  MARKOV_MC = 1
  MULTI_MARKOV = 2


# INT = number of battle simulations for monte carlo
NUM_OF_BATTLE_SIMS = 10000
# INT = number of monte_carlo simulations
NUM_OF_MC_SIMS = 5
# INT = different evaulation modes
MODE = Modes.MARKOV_MC

if MODE == Modes.MARKOV_MC:
  attack_troops = 2
  defend_troops = 1
  y = True
  while y == True:
    attack_troops = input("How many troops in attacking territory? (n >= 2)\n")
    try:
      attack_troops = int(attack_troops)
      y = False
      if attack_troops < 2:
        print("Not enough attacking troops, please try again.")
        y = True
    except:
      print("Please enter an integer.")

  y = True
  while y == True:
    defend_troops = input("How many troops in defending territory? (n >= 1)\n")
    try:
      defend_troops = int(defend_troops)
      y = False
      if defend_troops < 1:
        print("Not enough attacking troops, please try again.")
        y = True
    except:
      print("Please enter an integer.")

  attack_troops -= 1 # one attacking troop must stay behind

  # get probablities
  calculated_probs = calc_probs.calc_probs(attack_troops, defend_troops)
  simulated_probs_set = [sim_probs.do_monte_carlo(attack_troops, defend_troops, NUM_OF_BATTLE_SIMS) for i in range(NUM_OF_MC_SIMS)]

  # create bar chart
  # clean up and create formated data
  catagories = ["Calc"] + [("Sim " + str(i)) for i in range(1, NUM_OF_MC_SIMS + 1)]
  attack_probs = [calculated_probs[0]] + [simulated_probs_set[i][0] for i in range(NUM_OF_MC_SIMS)]
  defend_probs = [calculated_probs[1]] + [simulated_probs_set[i][1] for i in range(NUM_OF_MC_SIMS)]

  w = 0.6
  x = np.arange(len(catagories))

  fig, ax = plt.subplots()
  ax.bar(x, defend_probs, width=w, label='Defended')
  ax.bar(x, attack_probs, bottom=defend_probs, width=w, label='Conquered')

  for i, val in enumerate(defend_probs):
      plt.text(i, val, str(math.trunc(val*1000)/1000), ha='center', va='bottom')

  ax.set_xticks(x)
  ax.set_xticklabels(catagories)
  ax.set_ylabel('Probs')
  ax.set_title('RISK Battle probabilities')

  # Get the current legend handles and labels
  handles, labels = plt.gca().get_legend_handles_labels()

  # Reverse the order of handles and labels
  plt.legend(handles[::-1], labels[::-1])

  # Add troop info
  plt.figtext(0.1, 0.95, "Attack Troops = " + str(attack_troops))
  plt.figtext(0.1, 0.90, "Defend Troops = " + str(defend_troops))

  plt.show()

# also create heatmap of many different amounts of attack/defend troops
if MODE == Modes.MULTI_MARKOV:
  fig, ax = plt.subplots()
  # create data
  data = []
  col_labels = [str(i) for i in range(1,11)]
  row_labels = [" " + str(i) + " " for i in range(1,11)]
  for a_t in range(1,11):
    row = []
    for d_t in range (1,11):
      row.append(math.trunc(calc_probs.calc_probs(a_t, d_t)[0]*100)/100)
    data.append(row)

  # create table
  im = ax.imshow(data)

  # Show all ticks and label them with the respective list entries
  ax.set_xticks(range(len(col_labels)), labels=col_labels,
              rotation=45, ha="right", rotation_mode="anchor")
  ax.set_yticks(range(len(row_labels)), labels=row_labels)

  # Loop over data dimensions and create text annotations.
  for i in range(len(row_labels)):
    for j in range(len(col_labels)):
      text = ax.text(j, i, data[i][j],
        ha="center", va="center", color="w")

  # add labels
  ax.set_title('Probabilities of Conquering Territory')
  ax.set_ylabel("Attack Troops")
  ax.set_xlabel("Defend Troops")

  plt.show()


  
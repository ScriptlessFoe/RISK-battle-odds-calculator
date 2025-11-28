import math
import numpy as np
import RISK_1B_probs as probs
from queue import PriorityQueue
import matplotlib.pyplot as plt

# Full Battle Probabilities

# TRUE = this file runs the program by itself
# FALSE = this file does not run anything and only contains the functions
INDEPENDENT_RUN = False
# TRUE = print all info
# FALSE = no printing output
PRINT_MODE = False

if not INDEPENDENT_RUN:
   PRINT_MODE = False

# returns 2 element list with calculated probabilities of victory
# index: 0 - conquer odds, 1 - defend odds 
def calc_probs(attack_troops, defend_troops):
  # Get probabilities from single battles
  #     if (small_battle):
  #       # Index:
  #       #   0 => attacker lost 1 troop
  #       #   1 => defender lost 1 troop
  #         battle_results = [0, 0]
  #     else:
  #       # Index:
  #       #   0 => attacker lost 2 troops
  #       #   1 => both sides lost 1 troop
  #       #   2 => defender lost 2 troops
  #         battle_results = [0, 0, 0]
  all_probs = probs.get_all_probs()
  #print(all_probs)

  # Map possible states to an index - iterative, in order from greatest to least min
  state_to_index = {}
  index_to_state = {}
  pq = PriorityQueue()
  pq.put((-min(attack_troops, defend_troops), (attack_troops, defend_troops))) # negative priorites for max pq
  while not pq.empty():
    neg_priority, item = pq.get()
    a, d = item
    if (state_to_index.get((a,d)) != None):
      continue
    state_to_index[(a,d)] = len(state_to_index)
    index_to_state[len(index_to_state)] = (a,d)
    if a == 0 or d == 0:
      continue
    if a == 1 or d == 1:
      pq.put((-min(a-1, d), (a-1, d)))
      pq.put((-min(a, d-1), (a, d-1)))
      continue
    pq.put((-min(a-2, d), (a-2, d)))
    pq.put((-min(a-1, d-1), (a-1, d-1)))
    pq.put((-min(a, d-2), (a, d-2)))

  # print(state_to_index)

  # preperation for getting steady state probabilites
  t_states = 0 # transient

  # Map the state space in a transition matrix
  side_size = len(state_to_index)
  transition_matrix = np.zeros((side_size, side_size))
  for index in range(side_size):
      a, d = index_to_state[index]
      if a == 0 or d == 0:
        transition_matrix[index][index] = 1
        continue
      t_states += 1
      battle_prob = all_probs[min(a-1, 2)][min(d-1, 1)]
      if len(battle_prob) == 3:
          transition_matrix[index][state_to_index[(a-2, d)]] = battle_prob[0]
          transition_matrix[index][state_to_index[(a-1, d-1)]] = battle_prob[1]
          transition_matrix[index][state_to_index[(a, d-2)]] = battle_prob[2]
      else:
          transition_matrix[index][state_to_index[(a-1, d)]] = battle_prob[0]
          transition_matrix[index][state_to_index[(a, d-1)]] = battle_prob[1]

  # np.set_printoptions(threshold=transition_matrix.size)
  # print(transition_matrix)

  # find the steady state probabilities of the transition matrix of an absorbing Markov chain
  # Matrix names are pulled from https://en.wikipedia.org/wiki/Absorbing_Markov_chain
  Q = transition_matrix[:t_states, :t_states]
  I_t = np.identity(t_states)
  N = np.linalg.inv(I_t - Q)
  R = transition_matrix[:t_states, t_states:]
  B = np.dot(N, R)

  # first row always contains resulting probs for inital troop count
  steady_state_probs = B[0] 

  # Print
  if PRINT_MODE:
    print("----------------------")
    print("Total battle probabilities:")
    print("  Number of Attacking Troops:", attack_troops)
    print("  Number of Defending Troops:", defend_troops)
    print("----------------------")
    print("Possible Battle Results:")

  # calculate total odds of victory
  victory_probs = [0,0] # Index: 0 - chance of conquer, 1 - chance of defense
  for i in range(len(steady_state_probs)):
      index = i + t_states
      troop_count = index_to_state[index]
      if (troop_count[0] == 0): # territory defended
          victory_probs[1] += steady_state_probs[i]
          if PRINT_MODE:
            print("  Territory Defended, ", troop_count[1], "Remaining Defend Troops, Probability:", steady_state_probs[i])
      else: # territory conquered
          victory_probs[0] += steady_state_probs[i]
          if PRINT_MODE:
            print("  Territory Conquered,", troop_count[0], "Remaining Attack Troops, Probability:", steady_state_probs[i])
  
  # validate odds
  if (not math.isclose(sum(victory_probs), 1)):
      print("Probabilities don't sum to 1.\n")
      quit
  
  if PRINT_MODE:
    print("----------------------")
    print("Total Victory Odds:")
    print("  Territory Conquered:", victory_probs[0])
    print("  Territory Defended: ", victory_probs[1])
    print("----------------------")
  
  return victory_probs

# Main function
# Input validation
if INDEPENDENT_RUN:
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

  calc_probs(attack_troops, defend_troops)
  
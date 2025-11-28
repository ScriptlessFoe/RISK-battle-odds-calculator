import math
import random

# Full Battle Simulation

# TRUE = this file runs the program by itself
# FALSE = this file does not run anything and only contains the functions
INDEPENDENT_RUN = False
# TRUE = performs many simulations to determine probabilites (implies print_mode = false)
# FALSE = performs a single simulation
MONTE_CARLO_MODE = True
# INT = number of battle simulations for monte carlo
NUM_OF_SIMS = 10000
# TRUE = prints single battle simulation result
# FALSE = no printing single battle simulation result
SINGLE_PRINT_MODE = True
# TRUE = prints simulation result
# FALSE = no printing output
PRINT_MODE = True

if MONTE_CARLO_MODE or not INDEPENDENT_RUN:
  PRINT_MODE = False
if not PRINT_MODE:
  SINGLE_PRINT_MODE = False


dice = [1, 2, 3, 4, 5, 6]

# Start single simulation
# Return: true if territory conquered, false if defended
def do_single_sim(attack_troops, defend_troops):
  # Print
  if not MONTE_CARLO_MODE:
    print("----------------------")
    print("Single battle simulation:")
    print("----------------------")

  # main loop
  roll_number = 0
  while attack_troops > 0 and defend_troops > 0:
    roll_number += 1
    attack_dice = 0
    defend_dice = 0

    # max attacking dice
    if attack_troops <= 3:
      attack_dice = attack_troops
    else:
      attack_dice = 3
    # max defending dice
    if defend_troops <= 2:
      defend_dice = defend_troops
    else:
      defend_dice = 2

    # generate rolls and sort
    attack_rolls = random.choices(dice, k=attack_dice)
    defend_rolls = random.choices(dice, k=defend_dice)
    attack_rolls.sort()
    defend_rolls.sort()

    # calculate troop loss
    attack_losses = 0
    defend_losses = 0
    small_battle = False
    if (min(attack_dice, defend_dice) == 1):
      small_battle = True

    if attack_rolls[-1] > defend_rolls[-1]:
      defend_losses += 1
    else:
      attack_losses += 1
    if not small_battle:
      if attack_rolls[-2] > defend_rolls[-2]:
        defend_losses += 1
      else:
        attack_losses += 1

    # printing
    if SINGLE_PRINT_MODE:
      print("----------------------")
      print("Roll Number:", roll_number)
      print("----------------------")
      print("  Number of Attacking Troops:", attack_troops)
      print("  Number of Defending Troops:", defend_troops)
      print("----------------------")
      print("Rolls:")
      print("  Attack Rolls:", attack_rolls)
      print("  Defend Rolls:", defend_rolls)
      print("----------------------")
      print("Losses:")
      print("  Attack Losses:", attack_losses)
      print("  Defend Losses:", defend_losses)
      print("----------------------")
    
    # clean up
    attack_troops -= attack_losses
    defend_troops -= defend_losses

  # Single Battle Result:
  if not MONTE_CARLO_MODE:
    print("----------------------")
    print("Battle result:")
    if attack_troops == 0:
      print("  Territory Defended,", defend_troops, "Remaining Defend Troops")
    else:
      print("  Territory Conquered,", attack_troops, "Remaining Attack Troops")
    print("----------------------")
  
  # return result if doing monte carlo
  if MONTE_CARLO_MODE:
    if attack_troops == 0:
      return False
    else:
      return True

# returns 2 element list with simulated probabilities of victory
# index: 0 - conquer odds, 1 - defend odds 
def do_monte_carlo(attack_troops, defend_troops, sims):
  attack_wins = 0
  defend_wins = 0
  for i in range(sims):
    territory_conquered = do_single_sim(attack_troops, defend_troops)
    if territory_conquered:
      attack_wins += 1
    else:
      defend_wins += 1
  
  victory_probs = [attack_wins/sims, defend_wins/sims]
  
  # print stuff
  if INDEPENDENT_RUN:
    print("----------------------")
    print("Full battle simulation:")
    print("----------------------")
    print("Number of simulations:", sims)
    print("----------------------")
    print("Results:")
    print("  Attacker Wins:", attack_wins)
    print("  Defender Wins:", defend_wins)
    print("----------------------")
    print("Probabilities:")
    print("  Territory Conquered:", victory_probs[0])
    print("  Territory Defended: ", victory_probs[1])
    print("----------------------")

  return victory_probs

# Main function
# Input validation
if(INDEPENDENT_RUN):
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

  if not MONTE_CARLO_MODE:
    do_single_sim(attack_troops, defend_troops)
  else: 
    do_monte_carlo(attack_troops, defend_troops, NUM_OF_SIMS)

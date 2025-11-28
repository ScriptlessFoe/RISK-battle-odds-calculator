from itertools import product

# Single Battle Probabilities

# TRUE = this file runs the program by itself
# FALSE = this file does not run anything and only contains the functions
INDEPENDENT_RUN = False
# TRUE = one combination of dice counts determined by user input
# FALSE = all valid combinations of dice counts
MANUAL_MODE = False
# TRUE = print each combination
# FALSE = no printing output
PRINT_MODE = True

if not INDEPENDENT_RUN:
   MANUAL_MODE = False
   PRINT_MODE = False

dice = [1, 2, 3, 4, 5, 6]

# function for calculating battles
def get_single_prob(attack_dice, defend_dice):
    attack_results = list(product(dice, repeat=attack_dice))
    defend_results = list(product(dice, repeat=defend_dice))

    total_results = len(attack_results) * len(defend_results)

    small_battle = False
    if (min(attack_dice, defend_dice) == 1):
        small_battle = True

    battle_results = None
    if (small_battle):
      # Index:
      #   0 => attacker lost 1 troop
      #   1 => defender lost 1 troop
        battle_results = [0, 0]
    else:
      # Index:
      #   0 => attacker lost 2 troops
      #   1 => both sides lost 1 troop
      #   2 => defender lost 2 troops
        battle_results = [0, 0, 0]

    for attack_roll in attack_results:
        for defend_roll in defend_results:
            attack_roll = sorted(attack_roll)
            defend_roll = sorted(defend_roll)
            index = 0
            if attack_roll[-1] > defend_roll[-1]:
                index += 1
            if (not small_battle and attack_roll[-2] > defend_roll[-2]):
                index += 1
            battle_results[index] += 1

    battle_probs = [x/total_results for x in battle_results]

    if (PRINT_MODE):
      print("----------------------")
      print("Single battle probabilities:")
      print("  Number of Attacking Dice:", attack_dice)
      print("  Number of Defending Dice:", defend_dice)
      print("----------------------")
      print("Total outcomes:", total_results)
      if (small_battle):
        print("Possible outcomes:")
        print("  Attacker -1 troop:", battle_results[0])
        print("  Defender -1 troop:", battle_results[1])
        print("----------------------")
        print("Probailities:")
        print("  Attacker -1 troop:", battle_probs[0])
        print("  Defender -1 troop:", battle_probs[1])
      else:
        print("Possible outcomes:")
        print("  Attacker -2 troops:", battle_results[0])
        print("  Both -1 troop:     ", battle_results[1])
        print("  Defender -2 troops:", battle_results[2])
        print("----------------------")
        print("Probailities:")
        print("  Attacker -2 troops:", battle_probs[0])
        print("  Both -1 troop:     ", battle_probs[1])
        print("  Defender -2 troops:", battle_probs[2])
      print("----------------------\n")

    return battle_probs


def get_all_probs():
    dice_combs = list(product(range(1,4), range(1,3)))
    all_probs = [[[],[]],
                 [[],[]],
                 [[],[]]]
    for dice_comb in dice_combs:
       all_probs[dice_comb[0]-1][dice_comb[1]-1] = (get_single_prob(dice_comb[0], dice_comb[1]))
    if(PRINT_MODE):
      print(all_probs)
    return all_probs

# Handle input
if(INDEPENDENT_RUN):
  if(MANUAL_MODE):
      # get number of dice on each side
      attack_dice = 3
      defend_dice = 2
      y = True
      while y == True:
        attack_dice = input("How many attack dice? (1, 2 or 3)\n")
        try:
          attack_dice = int(attack_dice)
          y = False
          if attack_dice < 1 or attack_dice > 3:
            print("Not enough attacking troops, please try again.")
        except:
          print("Please enter an integer.")

      y = True
      while y == True:
        defend_dice = input("How many defend dice? (1 or 2)\n")
        try:
          defend_dice = int(defend_dice)
          y = False
          if defend_dice < 1 or defend_dice > 2:
            print("Not enough attacking troops, please try again.")
        except:
          print("Please enter an integer.")
      get_single_prob(attack_dice, defend_dice)
  else:
      get_all_probs()

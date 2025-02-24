import codegen


requirements = """
Simulate a game of texas holdem. 
create objects to represent each player. 
each player should have some simple strategy and aggression level. 
give each player 1000 chips to start. 
Give a chip count at the beginning and end of each hand.
give detailed action for each round of betting and as each card is flipped over I want a full hand history for each hand that's played with every player's actions during the hand history, show what each player is dealt. 
also announce the winning hand at showdown. 
"""

codegen.write_review_and_run_code(requirements)

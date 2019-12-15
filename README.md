# A Combined Network Approach to Texas Hold’em
## Running the Project
First install the requirements. \
<code>
pip install -r requirements.txt
</code>
\
Next simply run Game.py \
<code>
python Game.py
</code>

To play against a different model open the Game.py file and change the model = "/params/model" to some other model.

## How it works 
The system uses a combined approach feeding a the result of a bayesian opponenet modeling algorithm into a neural network. The Bayesian portion works by first modeling the probability of each possible hand given that the player bet and then using these probabilities to calculate that a given player has a better hand than the AI given that they didn't fold. 
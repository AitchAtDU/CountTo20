import random
import requests

# Change the contents of KEY to the key for your model.
#########################################################

global KEY
KEY = ''

#########################################################


# Defining needed variables
#########################################################
PLAYER = True
COMPUTER = False

moves = {
    PLAYER:[],
    COMPUTER:[]
}

states = {
    PLAYER:[],
    COMPUTER:[]
}

turn = random.choice((PLAYER, COMPUTER))
running = True
current_state = 0

#########################################################


# Machine learning functions
#########################################################
def classify(state):

    if KEY:

        url = "https://machinelearningforkids.co.uk/api/scratch/"+ KEY + "/classify"

        response = requests.get(url, params={"data" : state})

        if response.ok:
            responseData = response.json()
            return int(responseData[0])
        else:
            response.raise_for_status()

    return random.randint(1,3)


def learn_from_this(statehistory, winningmoves):

    print("Maybe the computer could learn from the winner of the game?")

    for idx in range(len(winningmoves)):
        add_to_train(statehistory[idx], winningmoves[idx])
    train_new_model()


def add_to_train(state, move):

    print("Adding the move +{move} to {state} to the training data")

    url = "https://machinelearningforkids.co.uk/api/scratch/"+ KEY + "/train"

    response = requests.post(url, json={
        "data" : state,
        "label" : move
    })

    if response.ok:
        pass
    else:
        print(response.json())
        response.raise_for_status()


def train_new_model():
    print ("Training a new machine learning model")

    url = "https://machinelearningforkids.co.uk/api/scratch/"+ KEY + "/models"
    response = requests.post(url)

    if response.ok:
        print('Finished training')
    else:
        response.raise_for_status()


#########################################################


# Game Logic Functions
#########################################################
def player_move():

    move = input('Enter the 1, 2 or 3 to make your move\n')

    while move not in ('1', '2', '3'):

        move = input(f'Error - {move} is not a valid input.\n' + \
                     'Please enter 1, 2 or 3.\n')

    return int(move)


def on_win(turn):
    if turn:
        print('You win! Congratulations you seem to have a winning strategy')
    else:
        print('The computer has beat you. Maybe it\' learned too much...')

#########################################################


# Main Game loop
#########################################################

while running:

    if turn:
        print(f'The current total is {current_state}. How much do you want to add?')
        current_move = player_move()
    else:
        print(f'The current total is {current_state}. The computer is deciding what to add...')
        current_move = classify(current_state)

    current_state += current_move
    moves[turn].append(current_move)
    states[turn].append(current_state)

    if current_state >= 20:
        on_win(turn)
        running = False
        # learn_from_this(states[turn], moves[turn])

    turn = not turn

#########################################################

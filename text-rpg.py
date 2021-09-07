import cmd
import textwrap
import sys
import os
import time
import random

### global variables ###

SCREEN_WIDTH = 100

### player setup ###

class player:
    def __init__(self):
        self.name = ''
        self.role = ''
        self.hp = 0
        self.mana = 0
        self.inventory = []
        self.location = 'b2'
        self.game_over = False


myPlayer = player()


def choose_selection(input):
    if input.lower() == 'play':
        start_game()
    elif input.lower() == 'help':
        help_menu()
    elif input.lower() == 'quit':
        sys.exit()

### title screen ###
def title_screen_selections():
    option = input('> ')
    choose_selection(option)
    
    while option.lower() not in ['play', 'help', 'quit']:
        print('please enter a valid command')
        option = input('> ')
        choose_selection()

def title_screen():
    os.system('clear')
    print('###############################')
    print('### Welcome to the Text RPG ###')
    print('###############################')
    print('           - Play -            ')
    print('           - Help -            ')
    print('           - Quit -            ')
    print('    - lachancedevelopment -    ')
    print('###############################')
    title_screen_selections()


def help_menu():
    os.system('clear')
    print('###############################')
    print('### Welcome to the Text RPG ###')
    print('###############################')
    print('   Type to control your hero   ')
    print('  Up, down, left, right: move  ')
    print(' look, pickup: for interaction ')
    print('       - Play - | - Quit-      ')
    print('###############################')
    title_screen_selections()


### MAP ###
## Home is b2
# ----------------
# | a1 | a2 | a3 |
# ----------------
# | b1 | b2 | b3 |
# ----------------
# | c1 | c2 | c3 |
# ----------------


ZONENAME = ''
DESCRIPTION = 'description'
EXAMINATION = 'examine'
SOLVED = False
UP = 'up, north'
DOWN = 'down, south'
LEFT = 'left, west'
RIGHT = 'right, east'


solved_places = { 'a1': False, 'a2': False, 'a3': False,
                  'b1': False, 'b2': False, 'b3': False, 
                  'c1': False, 'c2': False, 'c3': False, 
}

zonemap = {
    'a1': {
        ZONENAME: 'Town Shop',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        SOLVED: False,
        UP: 'up, north',
        DOWN: 'b1',
        LEFT: '',
        RIGHT: 'a2',
    },
    'a2': {
        ZONENAME: 'Town Hall',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        SOLVED: False,
        UP: '',
        DOWN: 'b2',
        LEFT: 'a1',
        RIGHT: 'a3',
    },
    'a3': {
        ZONENAME: 'Town Pub',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        SOLVED: False,
        UP: '',
        DOWN: 'b3',
        LEFT: 'a2',
        RIGHT: '',
    },
    'b1': {
        ZONENAME: '',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        SOLVED: False,
        UP: 'a1',
        DOWN: 'c1',
        LEFT: '',
        RIGHT: 'b2',
    },
    'b2': {
        ZONENAME: 'Home',
        DESCRIPTION: 'This is your home.',
        EXAMINATION: 'Nothing has changed here in many years..',
        SOLVED: False,
        UP: 'a2',
        DOWN: 'c2',
        LEFT: 'b1',
        RIGHT: 'b3',
    },
    'b3': {
        ZONENAME: '',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        SOLVED: False,
        UP: 'a3',
        DOWN: 'c3',
        LEFT: 'b2',
        RIGHT: '',
    },
    'c1': {
        ZONENAME: '',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        SOLVED: False,
        UP: 'b1',
        DOWN: '',
        LEFT: '',
        RIGHT: 'c2',
    },
    'c2': {
        ZONENAME: '',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        SOLVED: False,
        UP: 'b2',
        DOWN: '',
        LEFT: 'c1',
        RIGHT: 'c3',
    },
    'c3': {
        ZONENAME: '',
        DESCRIPTION: 'description',
        EXAMINATION: 'examine',
        SOLVED: False,
        UP: 'b3',
        DOWN: '',
        LEFT: 'c2',
        RIGHT: '',
    },
}

### game interactivity ###
def print_location():
    print('\n' + ('#' * (4 + len(myPlayer.location))))
    print('# ' + myPlayer.location + ' #')
    print('# ' + zonemap[myPlayer.location][DESCRIPTION] + ' #')
    print('\n' + ('#' * (4 + len(myPlayer.location))))

def prompt():
    print('\n' + '===========')
    print('What would you like to do?')
    action = input('> ')
    acceptable_actions = ['move', 'go', 'travel', 'walk', 'quit', 'examine', 'inspect', 'look', 'location']
    while action.lower() not in acceptable_actions:
        print('Unknown action, try again. \n')
        action = input('> ')
    if action.lower() == 'quit':
        sys.exit()
    elif action.lower() in ['move', 'go', 'travel', 'walk']:
        player_move(action.lower())
    elif action.lower() in ['examine', 'inspect', 'look']:
        player_examine(action.lower())
    elif action.lower() in ['location']:
        print_location()
            
def player_move(my_action):
    ask = 'Where would you like to move to?'
    dest = input(ask)
    if dest in ['up', 'north']:
        destination = zonemap[myPlayer.location][UP]
        movement_handler(destination)
    elif dest in ['left', 'west']:
        destination = zonemap[myPlayer.location][LEFT]
        movement_handler(destination)
    elif dest in ['down', 'south']:
        destination = zonemap[myPlayer.location][DOWN]
        movement_handler(destination)
    elif dest in ['right', 'east']:
        destination = zonemap[myPlayer.location][RIGHT]
        movement_handler(destination)

def movement_handler(destination):
    print('\n' + 'You have moved to {}'.format(destination))
    myPlayer.location = destination
    print_location()

def player_examine(action):
    if zonemap[myPlayer.location][SOLVED]:
        print('You have already solved this zone')
    else:
        print('puzzle is now triggered')

### game functionality ###
def start_game():
    create_character()

def main_game_loop():
    while myPlayer.game_over is False:
        prompt()

def create_character():
    os.system('clear')

    ### players name
    question1 = 'Hello, what is your name??'
    for character in question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input('> ')
    myPlayer.name = player_name

    ### players role
    question2 = 'What role have you been training to become??\n'
    question2added = 'A warrior, mage, or a thief?'
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in question2added:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)
    player_role = input('> ')

    valid_roles = ['warrior', 'mage', 'thief']
    if player_role.lower() in valid_roles:
        myPlayer.role = player_role
        print('Ah yes, you are a {}\n'.format(player_role))
    else:
        while player_role.lower() not in valid_roles:
            print('please select a valid role\n')
            player_role = input('> ')
            if player_role.lower() in valid_roles:
                myPlayer.role = player_role
                print('Ah yes, you are a {}\n'.format(player_role))


    if myPlayer.role is 'warrior':
        myPlayer.hp = 120
        myPlayer.mana = 20
    elif myPlayer.role is 'mage':
        myPlayer.hp = 80
        myPlayer.mana = 120
    elif myPlayer.role is 'thief':
        myPlayer.hp = 100
        myPlayer.mana = 60

    
    ## introduction to the game
    question3 = 'Welcome {} the {}, to the land of Text RPG\n'.format(myPlayer.name, myPlayer.role)
    for character in question3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    
    speech1 = 'You have been away for quite sometime.\n'
    speech2 =  'I hope your training has served you well...\n'
    speech3 = 'you are going to need it..\n'

    for character in speech1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.06)
    for character in speech3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.08)
    
    os.system('clear')
    print('###############################')
    print('###      Let us begin.      ###')
    print('###############################')
    main_game_loop()

title_screen()

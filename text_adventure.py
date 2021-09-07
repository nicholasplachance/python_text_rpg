import os
import sys
import time
import random
import textwrap
import cmd


SCREEN_WIDTH = 100

class player:
    def __init__(self):
        self.name = ''
        self.role = ''
        self.hp = 0
        self.mana = 0
        self.location = 'b2'
        self.inventory = []
        self.game_over = False
    
myPlayer = player()

### title screen ###

def choose_selection(input):
    if input.lower() == 'play':
        start_game()
    if input.lower() == 'help':
        help_menu()
    if input.lower() == 'title':
        title_screen()
    if input.lower() == 'quit':
        sys.exit()

def title_screen_selections():
    option = input("> ")
    choose_selection(option)

    while option not in ['play', 'help', 'quit']:
        print('please choose a valid command')
        option = input('> ')
        choose_selection(option)

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
    print('     - Play - Title - Quit-    ')
    print('###############################')
    title_screen_selections()

### MAP ###

## Home is b2
# -----Town-----
# | a1 | a2 | a3 |
# -----Houses-----
# | b1 | b2 | b3 |
# ----------------
# | c1 | c2 | c3 |
# -----Outside-----

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
        DESCRIPTION: 'You can buy things here',
        EXAMINATION: 'The stock maybe limited, but this is the only shop in town.',
        SOLVED: False,
        UP: '',
        DOWN: 'b1',
        LEFT: '',
        RIGHT: 'a2',
    },
    'a2': {
        ZONENAME: 'Town Hall',
        DESCRIPTION: 'This is where meetings occur',
        EXAMINATION: 'A rather large building, for big gatherings',
        SOLVED: False,
        UP: '',
        DOWN: 'b2',
        LEFT: 'a1',
        RIGHT: 'a3',
    },
    'a3': {
        ZONENAME: 'Town Pub',
        DESCRIPTION: 'Here you can find beverages',
        EXAMINATION: 'What else is there to do in a small town, but drink?',
        SOLVED: False,
        UP: '',
        DOWN: 'b3',
        LEFT: 'a2',
        RIGHT: '',
    },
    'b1': {
        ZONENAME: 'Abandoned House',
        DESCRIPTION: 'The Abandoned House of the town',
        EXAMINATION: 'Some suggest this place is haunted, others claim it is just another abandoned house',
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
        ZONENAME: "Your Neighbor's Home",
        DESCRIPTION: 'Your neighbor for many years',
        EXAMINATION: 'Although many do not know their name, you call them Hulk Hogan.',
        SOLVED: False,
        UP: 'a3',
        DOWN: 'c3',
        LEFT: 'b2',
        RIGHT: '',
    },
    'c1': {
        ZONENAME: 'The Forest',
        DESCRIPTION: 'A spooky and creepy place when it is night time',
        EXAMINATION: 'Most will never enter the forest, only brave souls.',
        SOLVED: False,
        UP: 'b1',
        DOWN: '',
        LEFT: '',
        RIGHT: 'c2',
    },
    'c2': {
        ZONENAME: 'The Mountian',
        DESCRIPTION: 'A rather large obstacle for travel',
        EXAMINATION: 'The mountian helps keep intruders from enter the town',
        SOLVED: False,
        UP: 'b2',
        DOWN: '',
        LEFT: 'c1',
        RIGHT: 'c3',
    },
    'c3': {
        ZONENAME: 'The Ocean',
        DESCRIPTION: 'A rather calm and cool beach.',
        EXAMINATION: 'This is a town favorite, considering it is the least spooky place outside the town.',
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
    print('# ' + zonemap[myPlayer.location][EXAMINATION] + ' #')
    print('\n' + ('#' * (4 + len(myPlayer.location))))

def print_map():
    os.system('clear')
    print('------Town------')
    print('| a1 | a2 | a3 |')
    print('-----Houses-----')
    print('| b1 | b2 | b3 |')
    print('----------------')
    print('| c1 | c2 | c3 |')
    print('-----Outside----')

def prompt():
    print('\n' + ("*" * 31))
    print('What would you like to do?')
    action = input('> ')
    acceptable_actions = ['move', 'go', 'travel', 'walk', 'quit', 'examine', 'inspect', 'look', 'location', 'map']
    while action.lower() not in acceptable_actions:
        print('Unknown action, try again. \n')
        print("Acceptable actions are: " + acceptable_actions)
        action = input('> ')
    if action.lower() == 'quit':
        sys.exit()
    elif action.lower() in ['move', 'go', 'travel', 'walk']:
        player_move(action.lower())
    elif action.lower() in ['examine', 'inspect', 'look']:
        player_examine(action.lower())
    elif action.lower() in ['location']:
        print_location()
    elif action.lower() in ['map']:
        print_map()
    
def player_move(destination):
    ask = 'Where would you like to move to?\n> '
    dest = input(ask)
    if dest in ['up', 'north']:
        destination = zonemap[myPlayer.location][UP]
        movement_handler(destination)
    elif dest in ['right', 'east']:
        destination = zonemap[myPlayer.location][RIGHT]
        movement_handler(destination)
    elif dest in ['down', 'south']:
        destination = zonemap[myPlayer.location][DOWN]
        movement_handler(destination)
    elif dest in ['left', 'west']:
        destination = zonemap[myPlayer.location][LEFT]
        movement_handler(destination)

def movement_handler(destination):
    print('\n You have moved to {}'.format(destination))
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
    players_name()
    player_role()
    introduction()
    main_game_loop()

def players_name():
    os.system('clear')
    ### players name
    question1 = 'Hello, what is your name??\n'
    for character in question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input('> ')
    myPlayer.name = player_name

roles = [
    {
        'name': 'warrior',
        'hp': 120,
        'mana': 40
    },
    {
        'name': 'mage',
        'hp': 80,
        'mana': 120
    },
    {
        'name': 'paladin',
        'hp': 100,
        'mana': 80
    }
]

def player_role():
    os.system('clear')
    ### players role
    question2 = 'What role have you been training to become??\n'
    question2added = 'A warrior, mage, or a paladin?'
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in question2added:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)

    
    for role in roles:
        print('\n' + ('#' * (14 + len(role['name']))))
        print('# ' + 'NAME: ' + role['name'] + ' #')
        print('# ' + 'HP: '  + str(role['hp']) + ' #')
        print('# ' + 'MANA: '  + str(role['mana']) + ' #')
        print(('#' * (14 + len(role['name']))))

    print('Scroll up to look at the role stats')

    
    player_role = input('> ')

    valid_roles = ['warrior', 'mage', 'paladin']
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
        myPlayer.hp = roles[0].hp
        myPlayer.mana = roles[0].mana
    elif myPlayer.role is 'mage':
        myPlayer.hp = roles[1].hp
        myPlayer.mana = roles[1].mana
    elif myPlayer.role is 'paladin':
        myPlayer.hp = roles[2].hp
        myPlayer.mana = roles[2].mana

def introduction():
    os.system('clear')
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


title_screen()


#TODO:
"""
1. Implement Inventory
1a. Open and view inventory
1b. Add items to inventory
1c. Take things out of inventory
1d. Give inventory limited space

2. Add enemy / Combat system ( maybe )
2a. Trigger when entering specific areas
2b. Create simple combat
2c. Enemies can deal damage and receive damage

3. Add SFX ( maybe )
3a. Get sfxs

4. Add leveling system
4a. Choose what stats to increase upon leveling ( maybe )
4b. Add xp gained from certain activies

5. CREATE AN OBJECTIVE
5a. We need a way to be able to beat or lose the game
5b. Without this the game is rather pointless
5c. Create puzzles to complete in order to beat the game
5d. 6 total puzzles - complete 4 to complete the game

6. NOT AS IMPORTANT - Create lore / story
6a. On introduction make it less generic
6b. Create an overall theme to implement an atmosphere


"""

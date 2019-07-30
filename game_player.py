import random
import os
import json

# import my own modules
import m_file

# Are we in debug mode?
# debug = False

# Set up the field
Field = dict()
Field['OZ'] = [(  0,  0),(  25, 45)] # Own Zone
Field['L1'] = [( 25, 30),(  55, 45)] # Left Zones
Field['L2'] = [( 55, 30),(  85, 45)]
Field['L3'] = [( 85, 30),( 115, 45)]
Field['C1'] = [( 25, 15),(  55, 30)] # Center Zones
Field['C2'] = [( 55, 15),(  85, 30)]
Field['C3'] = [( 85, 15),( 115, 30)]
Field['R1'] = [( 25,  0),(  55, 15)] # Right Zones
Field['R2'] = [( 55,  0),(  85, 15)]
Field['R3'] = [( 85,  0),( 115, 15)]
Field['EZ'] = [(115,  0),( 140, 45)] # End Zone

# Set up Player Positions
player_positions = ['Left', 'Center', 'Right']

# Set up Teams
Teams = ['Home', 'Away']

# Set up Rosters
Roster = dict()
for team in Teams:
    Roster[team] = player_positions

# Set up game stats. These will be tracked for teams and maybe for individual players as well.
Stats = ['Goals', 'Completions', 'Interceptions', 'Incomplete_passes']

# Set up Scoreboard
Scoreboard = dict()
for team in Teams:
    for stat in Stats:
        key = team + '_' + stat
        Scoreboard[key] = 0

# Set up overall game status.
Status = dict()
Status['Time'] = 0 # Game time, meaning a count of plays
Status['Posession'] = ['Home', 'Center'] # the Home Center starts with the disc, and kicks off to the Away team.

# Set up starting (kickoff) player locations
Player_location = dict()
Player_location['Home_Left']   = (  0, 35)
Player_location['Home_Center'] = (  0, 22)
Player_location['Home_Right']  = (  0, 10)
Player_location['Away_Left']   = (115, 10)
Player_location['Away_Center'] = (115, 22)
Player_location['Away_Right']  = (115, 35)

# Load the home and away team genomes. In the future this should be
# done creating the team pairngs for a round-robin, but for
# now we are just making them by hand.
generation = 'TEST2'
Path = '/Users/testuser/Projects/ultimater/data/teams/test'
os.chdir(Path)
Teamlist = m_file.read('GEN-' + generation + '_teamlist')
home_team_name = Teamlist['Teams'][0]
away_team_name = Teamlist['Teams'][1]
home_genes = m_file.read(home_team_name)
away_genes = m_file.read(away_team_name)
# print('Home team: {} Away team: {}'.format(home_team_name, away_team_name))

# Define the Team and Player classes
class Team:
    player = dict()
    def __init__(self, name, generation, genes):
        self.name = name
        self.generation = generation
        self.genes = genes
    def description(self):
        return 'Team {} is from generation {}'.format(self.name, self.generation)

class Player:
    location = (0,0)
    has_disc = False

    steps = 0
    throws = 0
    completed_throws = 0
    intercepted_throws = 0
    turnovers = 0
    thrown_goals = 0
    caught_goals = 0
    
    def __init__(self, name, team, position):
        self.name = name
        self.team = team
        self.position = position
    def description(self):
        return 'Player {} is on team {}'.format(self.name, self.team.name)

# Instantiate the home and away teams
home = Team(home_team_name, generation, home_genes)
away = Team(away_team_name, generation, away_genes)
print(home.description())
# print(home.genes)

# Instantiate the players
home_left = Player('home_left', home, 'left')
home_center = Player('home_center', home, 'center')
home_right = Player('home_right', home, 'right')
away_left = Player('away_left', away, 'left')
away_center = Player('away_center', away, 'center')
away_right = Player('away_right', away, 'right')

print(home_left.description())
print(home_left.team.genes['Threshhold']['Throw'])



    







# Debug actions
#if debug:
#    print('----- Field Debug -----\n')
#    print('the field is:\n', Field)
#    print('here is the whole field:\n')
#    for zone in Field:
#        print(zone, ': ', Field[zone])
#
#    print('\n----- Scoreboard Debug -----')
#    print('the Scoreboard is:\n', Scoreboard)
#    print('\nhere is the whole Scoreboard:')
#    for key in Scoreboard:
#        print(key, ': ', Scoreboard[key])
#
#    print('\n----- Roster Debug -----')
#    print('the Roster is:\n', Roster)
#    print('\nhere is the whole Roster:')
#    for key in Roster:
#        print(key, ': ', Roster[key])
#    
#    print('\n----- Status Debug -----')
#    print('the Status is:\n', Status)
#    print('\nhere is the whole Status:')
#    for key in Status:
#        print(key, ': ', Status[key])
#    print('\nHomeGenes:', HomeGenes)
# done.


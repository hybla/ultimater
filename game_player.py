import random
import os
import json

# import my own modules
import m_file

# Set up the field
field = dict()
field['OZ'] = [(  0,  0),(  25, 45)] # Own Zone
field['L1'] = [( 25, 30),(  55, 45)] # Left Zones
field['L2'] = [( 55, 30),(  85, 45)]
field['L3'] = [( 85, 30),( 115, 45)]
field['C1'] = [( 25, 15),(  55, 30)] # Center Zones
field['C2'] = [( 55, 15),(  85, 30)]
field['C3'] = [( 85, 15),( 115, 30)]
field['R1'] = [( 25,  0),(  55, 15)] # Right Zones
field['R2'] = [( 55,  0),(  85, 15)]
field['R3'] = [( 85,  0),( 115, 15)]
field['EZ'] = [(115,  0),( 140, 45)] # End Zone

# function that finds which zone a point is in
def zone_finder(point):
    current_zone = 'OFF_FIELD'
    for z in field:
        #assign values to variables
        x1,y1=field[z][0][0],field[z][0][1]
        x2,y2=field[z][1][0],field[z][1][1]
        x,y=point[0],point[1]
        # is our point between the x and y corners of the zone?
        if (x >= x1 and x <= x2 and y >= y1 and y <= y2) :
            current_zone = z
            break
    return current_zone

# a tester for zone_finder()
def zone__finder_TESTER():
    for x in range(142):
        for y in range(47):
            print ('Point ({}, {}) is in Zone: {}'.format(x, y, zone((x,y))))


# Set up starting (kickoff) player locations
starting_location = dict()
starting_location['home_left']   = (  0, 35)
starting_location['home_center'] = (  0, 22)
starting_location['home_right']  = (  0, 10)
starting_location['away_left']   = (115, 10)
starting_location['away_center'] = (115, 22)
starting_location['away_right']  = (115, 35)

# Define the Team and Player classes
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
    
    def __init__(self, name, position):
        self.name = name
        self.position = position
    def description(self):
        msg = (
            'Details for player named {0}:\n'
            '  Location: {1[0]:d}, {1[1]:d}\n  Has disc: {2}\n'
            '  Steps Taken: {3}\n  Throws Made: {4}\n  Throws Completed: {5}\n'
            '  Throws Intercepted: {6}\n  Turnovers: {7}\n  Thrown Goals: {8}\n'
            '  Caught Goals: {9}\n'.format(self.name, self.location, self.has_disc,
               self.steps, self.throws, self.completed_throws,
               self.intercepted_throws, self.turnovers, self.thrown_goals,
               self.caught_goals))
        return msg 

class Team:
    left = Player('left', 'left')
    center = Player('center', 'center')
    right = Player('right', 'right')
    
    def __init__(self, name, generation, genes, home_team):
        self.name = name
        self.generation = generation
        self.genes = genes
        self.home_team = home_team # am I the home team? Boolean.
    def description(self):
        team_msg = (
            'Details for team {} from generation {}:\n'
            'Home team: {}\n'.format(self.name, self.generation, self.home_team))
        left_msg = self.left.description()
        center_msg = self.center.description()
        right_msg = self.right.description()
        return team_msg + left_msg + center_msg + right_msg

# Load the home and away team genomes. In the future this should be
# done creating the team pairngs for a round-robin, but for
# now we are just selecting two teams by hand.
generation = 'TEST2'
Path = '/Users/testuser/Projects/ultimater/data/teams/test'
os.chdir(Path)
Teamlist = m_file.read('GEN-' + generation + '_teamlist')
home_team_name = Teamlist['Teams'][3]
away_team_name = Teamlist['Teams'][22]
home_genes = m_file.read(home_team_name)
away_genes = m_file.read(away_team_name)

# Instantiate the home and away teams
home = Team(home_team_name, generation, home_genes, True)
away = Team(away_team_name, generation, away_genes, False)

# Put the players on the field and give the home center the disc
home.left.location = starting_location['home_left']
home.center.location = starting_location['home_center']
home.right.location = starting_location['home_right']
away.left.location = starting_location['away_left']
away.center.location = starting_location['away_center']
away.right.location = starting_location['away_right']
home.center.has_disc = True

# testing stuff
print(home.left.description())
print('home team throw threshold: ', home.genes['Threshhold']['Throw'])
print(home.description())
print(away.description())
print('home left zone = {}'.format(zone_finder(home.left.location)))



